FROM archlinux:latest

RUN pacman -Syy &&\
    pacman -Sy --noconfirm base-devel git python3 python-pip gobject-introspection \
                           kicad kicad-library
RUN python3 -m pip install git+https://github.com/spielhuus/nukleus.git

#RUN apt-get update && apt-get upgrade -y &&\
#    apt-get install -y build-essential unzip wget git python3 python3-pip python3-dev \
#    python3-distutils locales kicad \
#    imagemagick librsvg2-bin &&\
#    python3 -m pip install git+https://github.com/spielhuus/nukleus.git &&\
#    python3 -m pip install scons junit_xml &&\
#    rm -rf /usr/share/doc &&\
#    wget https://github.com/spielhuus/sconstool-kicad/archive/refs/heads/main.zip &&\
#    unzip main.zip &&\
#    rm main.zip &&\
#    mkdir -p /usr/share/scons/site_scons/site_tools &&\
#    mv sconstool-kicad-main/kicad /usr/share/scons/site_scons/site_tools &&\
#    rm -rf sconstool-kicad-main &&\
#    apt-get purge -y build-essential unzip wget python3-pip python3-dev &&\
#    apt-get autoremove -y &&\
#    apt-get clean && rm -rf /var/lib/apt/lists/*
#
## set locale
#RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
#ENV LANG="en_US.UTF-8" LANGUAGE="en_US:en" LC_ALL="en_US.UTF-8"

CMD ["/bin/bash"]
