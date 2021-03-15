#! /usr/bin/env bash

DIR="$(dirname "$0")"

if [ $# -eq 0 ]; then
    tag=latest
else
    tag=$1
fi

exec docker build -t irika/vim-ycm:$tag "$DIR"
