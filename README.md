sqlcipher3
==========

This library takes [pysqlite3](https://github.com/coleifer/pysqlite3) and makes
some small modifications so it is suitable for use with
[sqlcipher](https://github.com/sqlcipher/sqlcipher) (sqlite with encryption).

Additional features:

* User-defined window functions (requires SQLite >= 3.25)
* Flags and VFS an be specified when opening connection
* Incremental BLOB I/O, [bpo-24905](https://github.com/python/cpython/pull/271)
* Improved error messages, [bpo-16379](https://github.com/python/cpython/pull/1108)
* Simplified detection of DML statements via `sqlite3_stmt_readonly`.
* Sqlite native backup API (also present in standard library 3.7 and newer).

A completely self-contained binary package (wheel) is available for versions
0.4.0 and newer as `sqlcipher3-binary`. This package contains the latest
release of sqlcipher compiled with numerous extensions, and requires no
external dependencies.

Building with System SQLCipher
------------------------------

To build `sqlcipher3` linked against the system SQLCipher, run:

```
$ python setup.py build
```

Building a statically-linked library
------------------------------------

To build `sqlcipher3` statically-linked against a particular version of
SQLCipher, you need to obtain the SQLCipher source code and copy `sqlite3.c`
and `sqlite3.h` into the source tree.

```
# Download the latest version of SQLCipher source code and build the source
# amalgamation files (sqlite3.c and sqlite3.h).
$ git clone https://github.com/sqlcipher/sqlcipher
$ cd sqlcipher/
$ ./configure
$ make sqlite3.c

# Copy the sqlcipher amalgamation files into the root of the sqlcipher3
# checkout and run build_static + build:
$ cp sqlcipher/sqlite3.[ch] sqlcipher3/
$ cd sqlcipher3
$ python setup.py build_static build
```

You now have a statically-linked, completely self-contained `sqlcipher3`.

Using the binary package
------------------------

A binary package (wheel) is available for linux with a completely
self-contained  `sqlcipher3`, statically-linked against the most recent release
of sqlcipher.

```
$ pip install sqlcipher3-binary
```

