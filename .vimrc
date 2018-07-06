set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required

Plugin 'VundleVim/Vundle.vim'

Plugin 'kien/ctrlp.vim'
Plugin 'Vimjas/vim-python-pep8-indent'
Plugin 'ervandew/supertab'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo

Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub

"Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)

"Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.

"Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required

set tabstop=4
set shiftwidth=4
set expandtab
set encoding=utf-8
set incsearch
set hlsearch
set tags=./tags;
set number " show line numbers in vim
set pastetoggle=<F2>
" Make it so we can use system clipboard like a normal text editor
set clipboard=unnamed
nnoremap <F3> :set invnumber<Enter><F2>
" Run the file in python's interactive mode, importing it as a module
nnoremap <F4> :!cd $(dirname "%:p"); python3.5 -i -c 'from %:t:r import *'<Enter>
" Run the file, assuming it's executable.
nnoremap <F5> :!cd $(dirname "%:p"); python -m %:t:r<Enter>
" Use this version for ANY executable:
" nnoremap <F5> :!cd $(dirname "%:p");"%:p"<Enter>
" Run the file assuming it's a bunch of unittests
nnoremap <F6> :!python3.5 -m unittest discover -v -s "%:p:h" -p "%:t"<Enter><Enter>
nnoremap <F7> :make
" Run flake8 check on the file.
nnoremap <F8> :!cd $(dirname "%:p");flake8 $(basename "%:p")<Enter>
nnoremap <F9> :!pytest %:p<Enter>
nnoremap <F10> :!cd $(dirname "%:p"); python3.5 -c 'import %:t:r; help(%:t:r)'<Enter><Enter>
nnoremap <C-l> $
nnoremap <C-h> ^

" ,e to fast find files
nmap <leader>e :e **/
map <ScrollWheelDown> :undo<CR>
map <ScrollWheelUp> :redo<CR>
"set t_Co=256
"set t_ut=
"colorscheme molokai
colorscheme darkblue