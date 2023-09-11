#!/bin/bash

exec docker run -d                          \
                --restart unless-stopped    \
                --init                      \
                --env TERM=xterm-color      \
                --volume "${HOME}":/work:rw \
                --name vim-ycm              \
            irika/vim-ycm:latest tail -f /dev/null
