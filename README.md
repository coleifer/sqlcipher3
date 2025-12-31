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

Building SQLCipher
------------------

To build `sqlcipher3` with SQLCipher embedded using the vendored sources:

```
$ python setup.py build
```

Building with System SQLCipher
------------------------------

To build `sqlcipher3` using a system-installed `libsqlcipher` (versions of
SQLCipher prior to 4.7.x):

```
$ python setup.py build_system
```

Using the binary package
------------------------

A binary package (wheel) is available for linux with a completely
self-contained  `sqlcipher3`, statically-linked against the most recent release
of sqlcipher.

```
$ pip install sqlcipher3-binary
```

