#!/bin/bash

set -e -x

# Fetch the source code for SQLCipher.
if [[ ! -d "sqlcipher" ]]; then
  git clone --depth=1 git@github.com:sqlcipher/sqlcipher
  cd sqlcipher/
  ./configure --disable-tcl --enable-tempstore=yes LDFLAGS="-lcrypto -lm"
  make sqlite3.c
  cd ../
fi

# Grab the sqlcipher3 source code.
if [[ ! -d "./sqlcipher3" ]]; then
  git clone git@github.com:coleifer/sqlcipher3
fi

# Copy the sqlcipher source amalgamation into the pysqlite3 directory so we can
# create a self-contained extension module.
cp "sqlcipher/sqlite3.c" sqlcipher3/
cp "sqlcipher/sqlite3.h" sqlcipher3/

# Create the wheels and strip symbols to produce manylinux wheels.
docker run -it -v $(pwd):/io quay.io/pypa/manylinux2014_x86_64 /io/_build_wheels.sh

sudo rm ./wheelhouse/*-linux_*
