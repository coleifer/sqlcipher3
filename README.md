sqlcipher3
==========
(forked from https://github.com/coleifer/sqlcipher3)

To install, run 
```
pip install.
```


## Dependencies
1. [SQLCipher](https://github.com/sqlcipher/sqlcipher)
2. OpenSSL

For example, Mac Users should run
```
brew install sqlcipher
brew install openssl@3
```


## What has changed compared to original?
Static library are linked via `sqlite3.c` and `sqlite3.h`. These 2 files are obtained by running
```
git clone https://github.com/sqlcipher/sqlcipher
cd sqlcipher/
./configure
make sqlite3.c
```

Other changes, see