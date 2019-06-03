pysqlcipherX
============

This library takes [pysqlite3](https://github.com/coleifer/pysqlite3) and makes
some small modifications so it is suitable for use with
[sqlcipher](https://github.com/sqlcipher/sqlcipher) (sqlite with encryption).

Additional features:

* Support for user-defined window functions (requires SQLite >= 3.25)
* Support specifying flags when opening connection
* Support specifying VFS when opening connection

Building with System SQLCipher
------------------------------

To build `pysqlcipherx` linked against the system SQLCipher, run:

```
$ python setup.py build
```

Building a statically-linked library
------------------------------------

To build `pysqlcipherx` statically-linked against a particular version of
SQLCipher, you need to obtain the SQLCipher source code and copy `sqlite3.c`
and `sqlite3.h` into the source tree.

```
# Download the latest version of SQLCipher source code and build the source
# amalgamation files (sqlite3.c and sqlite3.h).
$ git clone https://github.com/sqlcipher/sqlcipher
$ cd sqlcipher/
$ ./configure
$ make sqlite3.c

# Copy the sqlcipher amalgamation files into the root of the pysqlcipherx
# checkout and run build_static + build:
$ cp sqlcipher/sqlite3.[ch] pysqlcipherx/
$ cd pysqlcipherx
$ python setup.py build_static build
```

You now have a statically-linked, completely self-contained `pysqlcipherx`.

<small>Original code (c) Gerhard Häring</small>
