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
Plugin 'calviken/vim-gdscript3'
Plugin 'metakirby5/codi.vim'

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
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

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

" ,e to fast find files
nmap <leader>e :e **/
map <ScrollWheelDown> :undo<CR>
map <ScrollWheelUp> :redo<CR>

"""""""""" ABBREVIATIONS """"""""""
iabbrev pyinvocation #!/usr/bin/env python3
iabbrev bashcomp if "COMP_LINE" in os.environ:<Enter>command, curr_word, prev_word = sys.argv[1:]<Enter>
iabbrev pymain def main():<Enter>pass<Enter><Enter>if __name__ == "__main__":<Enter>main()<Esc>

"""""""""" COMMANDS """"""""""
command OScopy !cat % | xclip
colorscheme zellner
set visualbell

if &diff
    syntax off
    hi DiffAdd      cterm=none ctermfg=2 ctermbg=none
    hi DiffDelete   cterm=none ctermfg=1 ctermbg=none
    hi DiffText     cterm=none ctermfg=3 ctermbg=none
    hi DiffChange   cterm=bold ctermfg=3 ctermbg=none
endif
