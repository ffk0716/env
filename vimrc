set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Plugin 'Chiel92/vim-autoformat'
Plugin 'scrooloose/nerdtree'
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


syntax on
let &t_Co=256
colorscheme molokai
"let g:molokai_original = 1

set cursorline
highlight CursorLine cterm=none ctermbg=236 ctermfg=none
set hlsearch


set shiftwidth=4 
set tabstop=4
set expandtab

set smartindent 
set number
set autoindent
set clipboard=unnamed

let mapleader=','
set diffopt+=iwhite
map <Leader>w :w!<CR>
map <Leader>q :qa!<CR>
map <Leader>vi :tabnew ~/.vim/vimrc<CR>
map <Leader>s :source ~/.vim/vimrc<CR>

map <silent> <F4> :q<CR>
map <silent> <F6> :NERDTreeToggle<CR>
map <silent> <F7> :set wrap!<CR>
map <silent> <F8> :set number!<CR>
map <silent> <F9> :vertical resize -5<CR>
map <silent> <F10> :vertical resize +5<CR>


map H <c-w>h
map L <c-w>l

map <c-h> :tabp<CR>
map <c-l> :tabn<CR>
map <c-j> 6<c-e>
map <c-k> 6<c-y>
