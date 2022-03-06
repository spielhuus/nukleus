FROM archlinux:latest

ENV WORKSPACE="/github/workspace"
ENV WWW_DIR="/github/workspace/www"

RUN pacman -Syu --noconfirm &&\
    pacman -Sy --noconfirm base-devel git python3 python-pip gobject-introspection \
                           zsh neovim sudo \
                           hugo kicad kicad-library
RUN python3 -m pip install git+https://github.com/spielhuus/nukleus.git
RUN python3 -m pip install sconstool-nbconvert jupyterlab schemdraw sympy

# Setup an entrypoint script
COPY entrypoint.sh /entrypoint.sh
COPY entrypoint-user.sh /entrypoint-user.sh

RUN chmod 755 /entrypoint.sh
RUN chmod 755 /entrypoint-user.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/zsh"]
