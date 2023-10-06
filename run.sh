#!/bin/bash

docker rm --force vim-ycm 2>/dev/null
exec docker run -d                          \
                --restart unless-stopped    \
                --init                      \
                --env TERM=xterm-color      \
                --volume "${HOME}":/work:rw \
                --name vim-ycm              \
            irika/vim-ycm:latest tail -f /dev/null
