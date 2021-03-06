vim-flow
========

Creative writing in Vim!

Install
-------

If you want the autocompletion for rhymes, install nltk:

    easy_install nltk

Run the nltk downloader (if anyone knows a better way, let me know):

    python -c 'import nltk; nltk.download()'

Under the "Corpa" section, download the module called `cmudict`. After it is
done downloading, you can close the downloader.

Vim-flow requires [Vimpy][vi]. If it isn't installed yet, you should install
it. Vimpy makes writing Python plugins in Vim super simple, and there are
plugins that you'll find using it. For instance, this one.

You can install both Vimpy and vim-flow as you normally would. Either by
manually placing the files in your Vim runtime path (IE, ~/.vim) or by adding
it to your bundles directory. [Vundle][vu] users can install them by appending
the following Bundle statements to your vimrc:

    Bundle "LimpidTech/Vimpy"
    Bundle "monokrome/vim-flow"

After adding the bundles, you can run `:BundleInstall` to install the new
bundles.

[NeoBundle][nb] users can install them with a similar vimrc:

    NeoBundle "LimpidTech/Vimpy"
    NeoBundle "monokrome/vim-flow"

followed by running `:NeoBundleInstall` to install the bundles.

[vi]: http://github.com/LimpidTech/vimpy "Vimpy - Pythonic Vim"
[vu]: https://github.com/gmarik/vundle "Vundle - Vim Package Manager"
[nb]: https://github.com/Shougo/neobundle.vim "NeoBundle - Vim Package Manager"
