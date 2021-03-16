#!/bin/bash 
cd "$(dirname "$0")"
set -exu

rsync -avP --delete ~/.ssh ./ssh
docker build -t my/ubuntu .
