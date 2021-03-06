Usage on Debian 9
=================

A terminal session of the following procedure and a short test drive of fabrictest can be seen here:

[![asciicast](https://asciinema.org/a/191023.png)](https://asciinema.org/a/191023)

Upgrade system and install dependencies

```
apt-get update
apt-get upgrade
apt-get install git autoconf automake cmake libtool make \
  libreadline-dev texinfo libjson-c-dev libpcre3-dev pkg-config bison flex \
  python-pip libc-ares-dev python3-dev python-pytest python3-sphinx \
  install-info
```

Prepare for building FRR

```
addgroup --system --gid 92 frr
addgroup --system --gid 85 frrvty
adduser --system \
        --ingroup frr \
        --home /var/opt/frr/ \
        --gecos "FRR suite" \
        --shell /bin/false \
        frr
usermod -a -G frrvty frr
gpasswd -a root frrvty
```

Build libyang

```
git clone https://github.com/opensourcerouting/libyang
cd libyang
git checkout -b tmp origin/tmp
mkdir build; cd build
cmake -DENABLE_LYD_PRIV=ON ..
make
sudo make install
```

Clone, configure and build FRR

```
git clone https://github.com/FRRouting/frr.git
cd frr
./bootstrap.sh
./configure \
    --enable-exampledir=/usr/share/doc/frr/examples/ \
    --localstatedir=/var/opt/frr \
    --sbindir=/usr/lib/frr \
    --sysconfdir=/etc/frr \
    --enable-vtysh \
    --enable-isisd \
    --enable-pimd \
    --enable-watchfrr \
    --enable-ospfclient=yes \
    --enable-ospfapi=yes \
    --enable-multipath=64 \
    --enable-user=frr \
    --enable-group=frr \
    --enable-vty-group=frrvty \
    --enable-configfile-mask=0640 \
    --enable-logfile-mask=0640 \
    --enable-rtadv \
    --enable-fpm \
    --enable-ldpd \
    --enable-sharpd \
    --with-pkg-git-version
make -j$(grep 'processor\s*:' /proc/cpuinfo | wc -l)
make check
make install
```

Clone and configure fabrictest

```
git clone https://github.com/cfra/fabrictest.git
cd fabrictest
apt-get install python3-pip
pip3 install -r requirements.txt
cp config.py.example config.py
```

Run fabrictest
```
./start.py
```
