#!/bin/bash 
set -exu

rm -fr ./ssh
cp -r ~/.ssh ./ssh
docker build -t my/ubuntu .
