FROM debian:stretch

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y dist-upgrade && DEBIAN_FRONTEND=noninteractive apt-get install -y multistrap nano git apt-utils \
		     dialog lsb-release binutils wget ca-certificates pv bc lzop zip binfmt-support build-essential ccache unzip \
	             parted pkg-config libncurses5-dev whiptail debian-keyring debian-archive-keyring f2fs-tools libfile-fcntllock-perl rsync libssl-dev \
	             btrfs-tools ncurses-term p7zip-full kmod dosfstools libc6-dev-armhf-cross fakeroot systemd-container udev distcc \
	             libc6-i386 lib32ncurses5 lib32tinfo5 locales ncurses-base zlib1g aptly pixz libelf-dev python swig python-dev nsis nuitka qemu-utils python-pip
RUN pip install configparser
WORKDIR /root/edubian
USER root
COPY edubian /root/
COPY src /root/
ADD output /root/

ENTRYPOINT [ "/bin/bash", "python /root/edubian/__init__.py" ]
