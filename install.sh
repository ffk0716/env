#!/bin/bash -e
cd $( dirname ${BASH_SOURCE[0]} )

echo install dot files
pushd dotfiles > /dev/null
    for file in *
    do
        if [ -f ~/.$file ]; then
            if cmp -s $PWD/$file ~/.$file ; then
                echo $file: skipped
            else
                if [ -f ~/.$file.bk ]; then
                    echo "$file: sorry, ~/.$file.bk exist, can't backup"
                    exit 1
                else
                    echo $file: backuped, installed
                    mv ~/.$file ~/.$file.bk
                    ln -fs $PWD/$file ~/.$file
                fi 
            fi
        else
            echo $file: installed
            ln -fs $PWD/$file ~/.$file
        fi 
    done
popd > /dev/null

echo
echo setup vim
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
vim +PluginInstall +qall


