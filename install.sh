#!/bin/bash -e
git submodule update --init --recursive
vim +PluginInstall +qall
ln -fs $PWD/vim ~/.vim
ln -fs $PWD/.tmux.conf ~/.
echo source $PWD/bashrc.private >> ~/.bashrc
