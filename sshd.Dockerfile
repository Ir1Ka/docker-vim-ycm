FROM irikaq/vim-ycm

ARG DEBIAN_FRONTEND=noninteractive

# Install openssh server
RUN apt-get update                                                  \
    && apt-get install -y --no-install-recommends                   \
        openssh-server                                              \
# clean
    && apt-get clean                                                \
    && (rm -rf /var/lib/apt/lists/*                                 \
        /var/tmp/* /var/tmp/.[!.]*                                  \
        /tmp/* /tmp/.[!.]* || true)                                 \
    && mkdir -p /run/sshd

EXPOSE 22

CMD ["-p", "--", "/bin/sh", "-c", "exec /sbin/sshd -D $SSHD_OPTS" ]
