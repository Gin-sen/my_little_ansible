#!/usr/bin/env bash

# Python dependencies
apt update && apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
  libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev python3-distutils

# Get python
wget https://www.python.org/ftp/python/3.10.8/Python-3.10.8.tgz
tar -xvf Python-3.10.8.tgz

# Compile Python 3.10
cd Python-3.10.8
./configure --enable-optimizations
make -j $(nproc)
make install
cd ..

