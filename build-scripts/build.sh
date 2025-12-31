#!/bin/bash

set -e -x

# Grab the sqlcipher3 source code.
if [[ ! -d "./sqlcipher3" ]]; then
  git clone git@github.com:coleifer/sqlcipher3
fi

# Create the wheels and strip symbols to produce manylinux wheels.
docker run -it -v $(pwd):/io quay.io/pypa/manylinux2014_x86_64 /io/_build_wheels.sh

sudo rm ./wheelhouse/*-linux_*
