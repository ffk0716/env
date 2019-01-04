#!/bin/bash
set -eux

sudo apt-get install dh-autoreconf libcurl4-gnutls-dev libexpat1-dev gettext libz-dev libssl-dev
sudo apt-get install asciidoc xmlto docbook2x
sudo apt-get install install-info
sudo apt-get install libz-dev gettext

wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.20.1.tar.gz
tar -xf git-2.20.1.tar.gz
pushd git-2.20.1
make -j$(nproc)
make -j8
sudo make install
popd
