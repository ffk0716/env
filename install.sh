#!/bin/bash -e
cd $( dirname ${BASH_SOURCE[0]} )

echo install dot files
pushd dotfiles > /dev/null
    for file in *
    do
        if [ -f ~/.$file ]; then
            if ! cmp -s $PWD/$file ~/.$file ; then
                if [ -f ~/.$file.bk ]; then
                    echo "sorry, ~/.$file.bk exist, can't backup"
                    exit 1
                fi 
                mv ~/.$file ~/.$file.bk
            fi
        fi 
        ln -fs $PWD/$file ~/.$file
    done
popd > /dev/null

echo setup vim
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
vim +PlugInstall +qall

echo setup shell
rm -f ~/.bashrc.sel
echo add \"source $PWD/shell/bashrc.ubuntu\" in .bashrc

