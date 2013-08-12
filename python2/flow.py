from curses.ascii import isdigit

import operator
import vimpy
import nltk


cmu = nltk.corpus.cmudict.dict()


class memoize(object):
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        if not args in self.memo:
            self.memo[args] = self.f(*args)

        return self.memo[args]


@memoize
def get_phoneme(word):
    result = cmu[word.lower()]

    # TODO: Support multiple pronounciations
    return result[0]


class Syllabalize(object):
    """ Counts the syllables in words, lines, and phrases. """

    def line(self, line):
        tokenizer = nltk.tokenize.WordPunctTokenizer()
        tokenizer.PUNCTUATION = (';', ':', ',', '.', '!', '?')

        total = 0

        for word in tokenizer.tokenize(line):
            if word in tokenizer.PUNCTUATION:
                continue

            count = self.word(word)

            if count:
                total += count

        return total

    def phrase(self, phrase, total=True):
        results = []

        for line in phrase.split():
            results.append(self.line(line))

        if total is True:
            results = sum(results)

        return results

    def word(self, word):
        phonemes = get_phoneme(word.lower())

        result = [len(list(y for y in x if isdigit(y[-1]))) for x in phonemes]

        if len(result):
            return result[0]

        return None


class Rhyme(object):
    """ Class for finding a specific rhyming pattern. """

    vowels = [
        'AA', 'AE', 'AH', 'AO', 'AW', 'AY',
        'EH', 'ER', 'EY',
        'IH', 'IY',
        'OW', 'OY',
        'UH', 'UW',
        'Y',
    ]

    def __init__(self,
            subject, limit=float('inf'), slant=False,
            min_score=3, min_score_acceptance_ratio=0.25,
            distance_factor=0.8):

        self.subject = subject
        self.slant = slant
        self.limit = limit
        self.min_score = min_score
        self.distance_factor = distance_factor
        self.min_score_acceptance_ratio = min_score_acceptance_ratio

    def split_by_vowels(self, subject):
        parts = []
        current_part = ''

        for part in subject:
            found_vowel = False

            # TODO: Consider slant variations
            if part[-1].isdigit():
                part = part[:-1]

            if part in self.vowels:
                found_vowel = True

                if current_part != '':
                    parts.append(current_part)

                current_part = part

            else:
                current_part = current_part + part

        if current_part != '':
            parts.append(current_part)

        return parts

    def get_score(self, subject, prospect):
        score = 0

        subject = self.split_by_vowels(subject)
        prospect = self.split_by_vowels(prospect)

        if self.slant is False and subject[-1] != prospect[-1]:
            return score

        subject_length = len(subject)
        prospect_length = len(prospect)

        if subject_length < prospect_length:
            distance_offset = (prospect_length - subject_length)
            related_length = subject_length
        else:
            distance_offset = (subject_length - prospect_length)
            related_length = prospect_length

        # Prefer words with closer lengths
        score = score - (distance_offset * self.distance_factor)

        for index in xrange(related_length):
            offset = index * -1

            if subject[offset] == prospect[offset]:
                score = score + 1

        return score

    def __iter__(self):
        # TODO: Can this possibly be more generator-like?

        count = 0

        if not self.subject in cmu:
            raise StopIteration('Subject not found in dictionary.')

        # TODO: Support multiple pronounciations
        subject = cmu[self.subject][0]

        result = []
        count = 0

        # Allow for some type of result when min_score is greater than the
        # possible score for a given subject.
        acceptance = len(subject) * self.min_score_acceptance_ratio

        if self.min_score > acceptance:
            min_score = acceptance
        else:
            min_score = self.min_score

        for item in cmu:
            if item == self.subject:
                continue

            prospect = get_phoneme(item)

            if item == 'defrost':
                self.hehe = True
            else:
                self.hehe = False

            score = self.get_score(subject, prospect)

            if score >= min_score:
                result.append({
                    "prospect": item,
                    "score": score
                })

        result = sorted(result, key=operator.itemgetter('score'))

        for item in result:
            if count < self.limit:
                yield item['prospect']
                count = count + 1

            else:
                raise StopIteration('Maximum rhyme limit exceeded.')

