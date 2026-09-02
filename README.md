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

A completely self-contained binary package (wheel) is available starting with
version 0.6.2. This package contains the latest release of SQLCipher compiled
with numerous extensions, and requires no external dependencies.

If you prefer to build yourself, a source distribution is available on PyPI.
Note that since SQLCipher 4.7.0 the build system for SQLCipher has changed
substantially and it no longer provides a `libsqlcipher` but is intended to
overwrite the system libsqlite3.

Differences from the standard library sqlite3 module
-----------------------------------------------------

sqlcipher3 mirrors the `sqlite3` API, but the two modules have separate type
objects. Code migrated from `sqlite3` by changing only the import keeps
referring to the standard library's types, and those references quietly stop
working:

* The exceptions are not shared. `sqlcipher3.IntegrityError` is not
  `sqlite3.IntegrityError`, nor a subclass of it, and the same holds for every
  DB-API exception up to and including the base `Error`. A leftover
  `except sqlite3.IntegrityError:` -- or even `except sqlite3.Error:` -- no
  longer catches anything, so a handled duplicate-key error becomes an
  unhandled exception. This is permitted by PEP 249, since each module defines
  its own exceptions, but it is easy to miss: nothing fails at import time, and
  tests that never provoke a database error stay green.
* `sqlite3.Row` cannot be used as a `row_factory`. It requires a
  `sqlite3.Cursor` and raises `TypeError: Row() argument 1 must be
  sqlite3.Cursor, not sqlcipher3.dbapi2.Cursor`. Use `sqlcipher3.Row`, which
  behaves identically.

The simplest way to avoid both is to not import `sqlite3` alongside
`sqlcipher3`: have one module in your application re-export the driver's
exception types and `Row`, and import them from there.

sqlcipher3 with statically-linked sqlcipher
-------------------------------------------

Install a wheel using `pip`:

```
$ pip install sqlcipher3
```

Because SQLCipher 4.7.0 and newer no longer provide a system libsqlcipher,
there is no great way to link against a system library. The best route if you
wish to use a different version of SQLCipher than the one bundled is to
check-out the source code and replace the vendored sources with your own
desired SQLCipher amalgamation.

```
# Copy your specific sqlcipher amalgamations into the vendor/ directory at the
# root of the sqlcipher3 checkout:
$ cp sqlite3.[ch] vendor/

# Build your library.
$ pip install .

# Or alternately,
$ python setup.py build
```

>Nor aught availed him now to have built in heaven high towers; nor did he
>scrape by all his engines, but was headlong sent with his industrious crew
>to build in hell.

Beware to those who would build their own wheels! See what has been wrought and
tremble.
