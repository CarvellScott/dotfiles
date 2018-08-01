#!/bin/bash

# sudo apt install python3
# sudo apt install git
# sudo apt install tmux

# curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
# sudo python3 -m get-pip

# Install Vundle for vim
if ! test -d ~/.vim/bundle; then
    git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
fi

if test -d $HOME; then
    echo "This should run in WSL"
    # You know, I should probably use that option for ln that's all "make it anyway"
    # I should probably just iterate through a list of filenames here too.
    ln -s -T "$HOME/dotfiles/.profile" ~/.profile
    ln -s -T "$HOME/dotfiles/.bash_aliases" ~/.bash_aliases
    ln -s -T "$HOME/dotfiles/.gitconfig" ~/.gitconfig
    ln -s -T "$HOME/dotfiles/.tmux.conf" ~/.tmux.conf
    ln -s -T "$HOME/dotfiles/.vimrc" ~/.vimrc
    ln -s -T "$HOME/dotfiles/.dircolors" ~/.dircolors
else
    echo "This should run in a VM or native linux"
    # Copy actual dotfiles
    #cp ./.bash_aliases ~/.bash_aliases
    #cp ./.gitconfig ~/.gitconfig
    #cp ./.profile ~/.profile
    #cp ./.tmux.conf ~/.tmux.conf
    #cp ./.vimrc ~/.vimrc
fi
