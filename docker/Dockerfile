FROM archlinux:latest

ENV WORKSPACE="/github/workspace"
ENV WWW_DIR="/github/workspace/www"

RUN pacman -Syu --noconfirm &&\
    pacman -Sy --noconfirm base-devel git python3 python-pip gobject-introspection \
                           zsh neovim sudo curl \
                           hugo kicad kicad-library
RUN python3 -m pip install git+https://github.com/spielhuus/nukleus.git
RUN python3 -m pip install sconstool-nbconvert jupyterlab schemdraw sympy
RUN mkdir -p /usr/local/share/fonts/TT/ &&\
    curl -L "https://github.com/hikikomori82/osifont/blob/master/osifont-lgpl3fe.ttf?raw=true" -o /usr/local/share/fonts/TT/osifont.ttf

# Setup an entrypoint script
COPY entrypoint.sh /entrypoint.sh
COPY entrypoint-user.sh /entrypoint-user.sh

RUN chmod 755 /entrypoint.sh
RUN chmod 755 /entrypoint-user.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/zsh"]
