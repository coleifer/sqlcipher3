#!/bin/bash

# manylinux uses ancient Centos 5, which ships openssl 0.9.8. We need to build
# our own in order to then build sqlcipher. The SSL headers will be installed
# to /usr/local/.
#
# The code for installing Perl and OpenSSL is derived from the psycopg2-binary
# build scripts.
yum install -y zlib-devel openssl-devel

# Volume (cwd of build script) is mounted at /io.
# A checkout of sqlcipher3 is cloned beforehand by the build.sh script.
cd /io/sqlcipher3

sed -i "s|name='sqlcipher3-binary'|name=PACKAGE_NAME|g" setup.py

export CFLAGS="-I/usr/local/include -L/usr/local/lib"

#PY36="/opt/python/cp36-cp36m/bin"
#"${PY36}/python" setup.py build_static
#
#PY37="/opt/python/cp37-cp37m/bin"
#"${PY37}/python" setup.py build_static

PY38="/opt/python/cp38-cp38/bin"
"${PY38}/pip" install setuptools
"${PY38}/python" setup.py build_static

PY39="/opt/python/cp39-cp39/bin"
"${PY39}/pip" install setuptools
"${PY39}/python" setup.py build_static

PY310="/opt/python/cp310-cp310/bin"
"${PY310}/pip" install setuptools
"${PY310}/python" setup.py build_static

PY311="/opt/python/cp311-cp311/bin"
"${PY311}/pip" install setuptools
"${PY311}/python" setup.py build_static

PY312="/opt/python/cp312-cp312/bin"
"${PY312}/pip" install setuptools
"${PY312}/python" setup.py build_static

PY313="/opt/python/cp313-cp313/bin"
"${PY313}/pip" install setuptools
"${PY313}/python" setup.py build_static

PY314="/opt/python/cp314-cp314/bin"
"${PY314}/pip" install setuptools
"${PY314}/python" setup.py build_static

# Replace the package name defined in setup.py so we can push this to PyPI
# without stomping on the source dist.
sed -i "s|name=PACKAGE_NAME,|name='sqlcipher3-binary',|g" setup.py

#"${PY36}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
#"${PY37}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY38}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY39}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY310}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY311}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY312}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY313}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse
"${PY314}/pip" wheel /io/sqlcipher3 -w /io/wheelhouse

for whl in /io/wheelhouse/*.whl; do
  auditwheel repair "$whl" -w /io/wheelhouse/
done
