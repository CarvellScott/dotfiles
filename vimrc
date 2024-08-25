" Function to source only if file exists
function! SourceIfExists(file)
  if filereadable(expand(a:file))
    exe 'source' a:file
  endif
endfunction
call SourceIfExists("~/dotfiles/vundle_boilerplate.vimrc")
" Use the iMproved version of vi. We're not in the 70s anymore.
set nocompatible
" General opinionated imiprovements
set tabstop=4
set shiftwidth=4
set expandtab
set encoding=utf-8
set incsearch
set hlsearch
set tags=./tags;
set pastetoggle=<F2>
" show line numbers
set number 
" Make it so we can use system clipboard like a normal text editor
set clipboard=unnamedplus
" Make vertical splits look good at least
set fillchars+=vert:│
set wildignore+=*.pyc
hi VertSplit cterm=none ctermfg=none ctermbg=none

let python_highlight_all=1
syntax on
au BufNewFile,BufRead *.py set tabstop=4
au BufNewFile,BufRead *.py set softtabstop=4
au BufNewFile,BufRead *.py set shiftwidth=4
au BufNewFile,BufRead *.py set textwidth=79
au BufNewFile,BufRead *.py set expandtab
au BufNewFile,BufRead *.py set autoindent
au BufNewFile,BufRead *.py set fileformat=unix
au BufNewFile,BufRead tags set fileencoding=utf-8
au BufNewFile,BufRead *.py set foldmethod=indent
au BufNewFile,BufRead *.py set foldlevel=99
au BufNewFile,BufRead *.py set keywordprg=/usr/bin/env\ -S\ python3\ -m\ pydoc
au BufNewFile,BufRead *.py set makeef=/dev/null

au BufNewFile *.py 0r ~/.vim/templates/skeleton.py
au BufNewFile,BufRead *.mcmeta set filetype=json
au BufNewFile pyproject.toml 0r ~/.vim/templates/skeleton.pyproject.toml
au BufWritePost *.vimrc :so %
au BufNewFile,BufRead *.dockerfile set filetype=dockerfile
"""""""""" KEYBINDS """"""""""
nnoremap <F3> :set invnumber<Enter><F2>
" Run the file in python's interactive mode, importing it as a module
nnoremap <F4> :!cd $(dirname "%:p"); python3 -i -c 'from %:t:r import *'<Enter>
" Run the file, assuming it's executable. Try running it in python otherwise.
" nnoremap <F5> :!cd $(dirname "%:p"); python3 -m %:t:r<Enter>
" Use this version for ANY executable:
nnoremap <silent> <F5> :w<CR>:!clear; %:p<Enter>
inoremap <F5> <Esc>:w<CR>:!clear; %:p<Enter>
" Run the file assuming it's a bunch of unittests
nnoremap <F6> :!python3 -m unittest discover -v -s "%:p:h" -p "%:t"<Enter>
nnoremap <F7> :!clear; python3 -m doctest "%:p" && %:p<Enter>
" Run flake8 check on the file.
nnoremap <F8> :!cd $(dirname "%:p");autopep8 -d $(basename "%:p")<Enter>
" Clean and pretty-print JSON
nnoremap <F9> :%!python3 -m json.tool --sort-keys<Enter>"
nnoremap <C-K> :!cat % \| xclip -i -selection clipboard<Enter><Enter>
" Make ctags auto-prompt for duplicate tags
nnoremap <C-]> :execute 'tj' expand('<cword>')<CR>zv

" I realized my chromebook doesn't have F1-F12. Unfortunate.
" \e to edit whatever file is found via recursive search in current directory
nmap <leader>e :e **/
"\p to toggle paste mode
nnoremap <leader>p :set invnumber<Enter><F2>
" \i to run a python file interactively
nnoremap <leader>i :!cd $(dirname "%:p"); python3 -i -c 'from %:t:r import *'<Enter>
" \x to just save and execute a file
nnoremap <silent> <leader>x :w<CR>:!clear; %:p<Enter>
" \u To run python unittests for the current file
nnoremap <leader>u :!python3 -m unittest discover -v -s "%:p:h" -p "%:t"<Enter>
" \d To run doctests on the current python file
nnoremap <leader>d :!clear; python3 -m doctest "%:p" && %:p<Enter>
" \j To pretty-print whatever JSON data is open
nnoremap <leader>j :%!python3 -m json.tool --sort-keys<Enter>"
" \l To fly between buffers.
nnoremap <leader>l :ls<CR>:b<space>
" \c To fly between quickfix list entries
nnoremap <leader>c :clist<CR>:cc<space>
map z1 :set foldlevel=0<CR><Esc>
map z2 :set foldlevel=1<CR><Esc>
map z3 :set foldlevel=2<CR><Esc>
map z4 :set foldlevel=3<CR><Esc>
map z5 :set foldlevel=4<CR><Esc>
map z6 :set foldlevel=5<CR><Esc>
map z7 :set foldlevel=6<CR><Esc>
map z8 :set foldlevel=7<CR><Esc>
map z9 :set foldlevel=8<CR><Esc>
map z0 :set foldlevel=9<CR><Esc>

" NOTE: This doesn't actually seem to work
map <ScrollWheelDown> :undo<CR>
map <ScrollWheelUp> :redo<CR>


"""""""""" ABBREVIATIONS """"""""""
iabbrev bashcomp if "COMP_LINE" in os.environ:<Enter>command, curr_word, prev_word = sys.argv[1:]<Enter>

"""""""""" COMMANDS """"""""""
command RUN :w !python3
command! -range=% RUNLINES :<line1>,<line2>!python3
command EVIMRC :e $HOME/.vimrc
command SOVIMRC :so $HOME/.vimrc
command! -range=% JSONTIDY :<line1>,<line2>!python3 -m json.tool --sort-keys
" Render a .dot file. Requires graphviz
command DotRender !dot -Tpng % > %:r.png
" Convert a .csv to a .sql dump. Requires sqlite3
command CSV2SQL :%!sqlite3 -csv ':memory:' '.import /dev/stdin %:t:r' '.mode column' '.dump'
"colorscheme default
set visualbell

if &diff
    syntax off
    hi DiffAdd      cterm=none ctermfg=2 ctermbg=none
    hi DiffDelete   cterm=none ctermfg=1 ctermbg=none
    hi DiffText     cterm=none ctermfg=3 ctermbg=none
    hi DiffChange   cterm=bold ctermfg=3 ctermbg=none
endif
" Allow gx to open links in browser
let g:netrw_browsex_viewer='firefox'
set vb t_vb=     " no visual bell & flash
let g:markdown_fenced_languages = ['diff', 'html', 'json', 'python']

autocmd BufNewFile,BufRead *.png set filetype=hex_highlight
call SourceIfExists("~/.vimrc.local")

