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
au BufNewFile,BufRead *.py set keywordprg=pydoc3
au BufNewFile *.py 0r ~/.vim/templates/skeleton.py
au BufNewFile,BufRead *.mcmeta set filetype=json
au BufWritePost *.vimrc :so %
"""""""""" KEYBINDS """"""""""
nnoremap <F3> :set invnumber<Enter><F2>
" Run the file in python's interactive mode, importing it as a module
nnoremap <F4> :!cd $(dirname "%:p"); python3 -i -c 'from %:t:r import *'<Enter>
" Run the file, assuming it's executable. Try running it in python otherwise.
" nnoremap <F5> :!cd $(dirname "%:p"); python3 -m %:t:r<Enter>
" Use this version for ANY executable:
nnoremap <F5> :!cd $(dirname "%:p");"%:p"<Enter>
" Run the file assuming it's a bunch of unittests
nnoremap <F6> :!python3 -m unittest discover -v -s "%:p:h" -p "%:t"<Enter>
nnoremap <F7> :!python3 -m doctest "%:p" <Enter>
" Run flake8 check on the file.
nnoremap <F8> :!cd $(dirname "%:p");autopep8 -d $(basename "%:p")<Enter>
" Clean and pretty-print JSON
nnoremap <F9> :%!python3 -m json.tool --sort-keys<Enter>"
nnoremap <C-K> :!cat % \| xclip -i -selection clipboard<Enter><Enter>
" Make ctags auto-prompt for duplicate tags
nnoremap <C-]> :execute 'tj' expand('<cword>')<CR>zv

"imap <C-l> OC
"imap <C-h> OD
"imap <C-j> OB
"imap <C-k> OA

"\e to edit whatever file is found via recursive search in current directory
nmap <leader>e :e **/
map <ScrollWheelDown> :undo<CR>
map <ScrollWheelUp> :redo<CR>

"""""""""" ABBREVIATIONS """"""""""
iabbrev bashcomp if "COMP_LINE" in os.environ:<Enter>command, curr_word, prev_word = sys.argv[1:]<Enter>

"""""""""" COMMANDS """"""""""
command OScopy !cat % | xclip
command RUN :w !python3
command! -range=% RUNLINES :<line1>,<line2>!python3
command EVIMRC :e $HOME/.vimrc
command SOVIMRC :so $HOME/.vimrc
command! -range=% JSONTIDY :<line1>,<line2>!python3 -m json.tool --sort-keys
" Requires sudo apt install graphviz
command DotRender !dot -Tpng % > %:r.png
colorscheme zellner
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

call SourceIfExists("~/.vimrc.local")
