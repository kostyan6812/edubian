FROM debian:stretch

MAINTAINER Konstantin Kryazhenkov <konstantin@mirea.ru>

ENV TZ=Europe/Moscow
ENV TERM=$TERM
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade && DEBIAN_FRONTEND=noninteractive apt-get install -y multistrap nano git apt-utils \
		     dialog lsb-release binutils wget ca-certificates pv bc lzop zip binfmt-support build-essential ccache unzip \
	             parted pkg-config libncurses5-dev whiptail debian-keyring debian-archive-keyring f2fs-tools libfile-fcntllock-perl rsync libssl-dev \
	             btrfs-progs ncurses-term p7zip-full kmod dosfstools libc6-dev-armhf-cross fakeroot systemd-container udev distcc \
	             libc6-i386 lib32ncurses5-dev libncurses5 libtinfo5 locales ncurses-base zlib1g aptly pixz libelf-dev python swig python-dev nsis qemu-utils python-pip \
		     bison flex
RUN pip install configparser
RUN pip install pexpect
USER root
RUN mkdir /root/edubian/
RUN mkdir /root/src/
RUN mkdir /root/output/
COPY edubian/ /root/edubian/
RUN wget http://nsis.sourceforge.net/mediawiki/images/c/c9/Inetc.zip
RUN unzip -d /usr/share/nsis/ Inetc.zip
RUN cp /usr/share/nsis/Plugins/x86-unicode/INetC.dll /usr/share/nsis/Plugins/
RUN rm -rf /usr/share/nsis/Plugins/x86-unicode/
RUN rm -rf /usr/share/nsis/Plugins/x86-ansi/
RUN rm -rf /usr/share/nsis/Plugins/amd64-unicode/
RUN rm Inetc.zip
WORKDIR /root/edubian


ENTRYPOINT ["python", "__init__.py"]
