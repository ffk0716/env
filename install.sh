#!/bin/bash -ex
cd $( dirname ${BASH_SOURCE[0]} )

# install dot files
pushd dotfiles
    for file in *
    do
        if [ -f ~/.$file ]; then
            mv ~/.$file ~/.$file.bk
        fi 
        ln -fs $PWD/$file ~/.$file
    done
popd

# setup vim
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
vim +PlugInstall +qall

# setup shell
echo add \"source $PWD/shell/bashrc.ubuntu\" in .bashrc

