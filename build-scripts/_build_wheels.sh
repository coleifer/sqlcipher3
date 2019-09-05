#!/bin/bash

# manylinux uses ancient Centos 5, which ships openssl 0.9.8. We need to build
# our own in order to then build sqlcipher. The SSL headers will be installed
# to /usr/local/.
#
# The code for installing Perl and OpenSSL is derived from the psycopg2-binary
# build scripts.
yum install -y zlib-devel

OPENSSL_VERSION="1.1.1b"
OPENSSL_TAG="OpenSSL_${OPENSSL_VERSION//./_}"

cd /io

if [ ! -d "openssl-${OPENSSL_TAG}/" ]; then
  # Building openssl 1.1 requires perl 5.10 or newer.
  curl -L https://install.perlbrew.pl | bash
  source ~/perl5/perlbrew/etc/bashrc
  perlbrew install --notest perl-5.16.0
  perlbrew switch perl-5.16.0

  curl -sL https://github.com/openssl/openssl/archive/${OPENSSL_TAG}.tar.gz \
    | tar xzf -

  cd "openssl-${OPENSSL_TAG}"

  # Expose the lib version number in the .so file name.
  sed -i "s/SHLIB_VERSION_NUMBER\s\+\".*\"/SHLIB_VERSION_NUMBER \"${OPENSSL_VERSION}\"/" \
      ./include/openssl/opensslv.h
  sed -i "s|if (\$shlib_version_number =~ /(^\[0-9\]\*)\\\.(\[0-9\\\.\]\*)/)|if (\$shlib_version_number =~ /(^[0-9]*)\.([0-9\.]*[a-z]?)/)|" \
      ./Configure

  ./config --prefix=/usr/local/ --openssldir=/usr/local/ zlib -fPIC shared
  make depend && make && make install
fi

# Volume (cwd of build script) is mounted at /io.
# A checkout of sqlcipher3 is cloned beforehand by the build.sh script.
cd /io/sqlcipher3

sed -i "s|name='sqlcipher3-binary'|name=PACKAGE_NAME|g" setup.py

export CFLAGS="-I/usr/local/include -L/usr/local/lib"

PY36="/opt/python/cp36-cp36m/bin"
"${PY36}/python" setup.py build_static

PY37="/opt/python/cp37-cp37m/bin"
"${PY37}/python" setup.py build_static

# Replace the package name defined in setup.py so we can push this to PyPI
# without stomping on the source dist.
sed -i "s|name=PACKAGE_NAME,|name='sqlcipher3-binary',|g" setup.py

"${PY36}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY37}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse

for whl in /io/wheelhouse/*.whl; do
  auditwheel repair "$whl" -w /io/wheelhouse/
done
