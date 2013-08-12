if (exists("g:loaded_flow"))
    finish
endif

let g:loaded_flow=1

if !has('python')
    finish
endif

au BufNewFile,BufRead *.flow set filetype=flow
