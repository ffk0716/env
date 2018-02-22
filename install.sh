#!/bin/bash -e
git submodule update --init --recursive
ln -fs $PWD/vim ~/.vim
ln -fs $PWD/.tmux.conf ~/.
