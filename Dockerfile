FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# unminimize for support man-db
RUN bash -c 'yes | unminimize'                                      \
# add i386 support
    && dpkg --add-architecture i386                                 \
    && apt-get update                                               \
    && apt-get install -y --no-install-recommends                   \
# apt utils and man-db
        apt-utils man-db                                            \
    && apt-get install -y --no-install-recommends                   \
# vim and ycm's dependency library
        build-essential cmake vim-nox python3-dev                   \
        mono-complete golang nodejs default-jdk npm                 \
# develop
        ninja-build bison autoconf automake libtool gdb gettext     \
        gnu-standards autopoint                                     \
# cross aarch64/arm64
        gcc-aarch64-linux-gnu g++-aarch64-linux-gnu                 \
# cross arm
        gcc-arm-linux-gnueabi g++-arm-linux-gnueabi                 \
# cross armhf
        gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf             \
# cross mips64
        gcc-mips64-linux-gnuabi64 g++-mips64-linux-gnuabi64         \
# tools
        bash-completion iproute2 iputils-ping                       \
        git subversion git-svn git-cvs exuberant-ctags cscope       \
        coreutils curl wget less file tree                          \
        gawk libncurses-dev flex                                    \
        dos2unix                                                    \
        gnupg zip unzip ssh-client                                  \
        lrzsz                                                       \
# i386 runtime
        libc6:i386 libstdc++6:i386 zlib1g:i386                      \
# clean
    && apt-get clean                                                \
    && (rm -rf /var/lib/apt/lists/*                                 \
        /var/tmp/* /var/tmp/.[!.]*                                  \
        /tmp/* /tmp/.[!.]* || true)                                 \
# restore bash completion for apt
    && (dir=/etc/apt/apt.conf.d;                                    \
     [ -d $dir ] && sed -i 's/[[:space:]]*Dir::Cache::\(src\)\?pkgcache "";[[:space:]]*//g' $dir/*) \
# do not clean APT cache
    && (f=/etc/apt/apt.conf.d/docker-clean;                         \
        [ -f $f ] && sed -i 's? /var/cache/apt/\*\.bin??g' $f)

# vim configuration
COPY .vimrc /root/.vimrc
# install vim plugin and compile ycm
RUN git clone https://github.com/VundleVim/Vundle.vim.git           \
        ~/.vim/bundle/Vundle.vim                                    \
    && echo "Vundle plugin installing ..."                          \
    && echo | vim +PluginInstall +qall >/dev/null 2>&1              \
    && (cd ~/.vim/bundle/YouCompleteMe; python3 install.py --all)   \
    && rm -rf ~/.cache

# environments
COPY home-cfg /root
RUN bash -xec '                                                     \
    for f in $(ls -d ~/.*-append); do                               \
        _f=${f%-append};                                            \
        if [[ -f "$f" && -r "$f" ]]; then                           \
            if [[ -f "$_f" && -w "$_f" ]]; then                     \
                cat "$f" >> "$_f";                                  \
            elif [[ ! -e "$_f" && -w "$(dirname "$_f")" ]]; then    \
                cp "$f" "$_f";                                      \
            fi;                                                     \
        fi;                                                         \
    done'                                                           \
    && mkdir -p /work
WORKDIR /work

COPY my_init /
ENTRYPOINT [ "/my_init" ]
