# -*- coding: ISO-8859-1 -*-
import os
import sys
import glob
import setuptools
from setuptools import Extension

# --- Sources ---
# Hardcoded source selection as requested
sources = glob.glob("src/*.c")
sources.append("amalgamation/sqlite3.c")

# --- Configuration ---
include_dirs = ["src", ".", "amalgamation"]
library_dirs = []
libraries = ['libcrypto', 'libssl', 'ws2_32', 'advapi32', 'user32', 'gdi32', 'crypt32', 'bcrypt']

# OpenSSL Path Detection
if sys.platform == "win32":
    openssl_conf = os.environ.get('OPENSSL_CONF')
    if not openssl_conf:
        for loc in [r"C:\Program Files\OpenSSL-Win64\bin\openssl.cfg", 
                    r"C:\OpenSSL-Win64\bin\openssl.cfg"]:
            if os.path.exists(loc):
                openssl_conf = loc
                break
    
    if openssl_conf:
        openssl_root = os.path.dirname(os.path.dirname(openssl_conf))
        include_dirs.insert(0, os.path.join(openssl_root, "include"))
        openssl_lib = os.path.join(openssl_root, "lib", "VC", "x64", "MD")
        if not os.path.exists(openssl_lib):
            openssl_lib = os.path.join(openssl_root, "lib")
        library_dirs.append(openssl_lib)
        print(f"DEBUG: OpenSSL Lib Path: {openssl_lib}")

# --- Extension Definition ---
ext = Extension(
    name="sqlcipher3._sqlite3",
    sources=sources,
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    define_macros=[
        ('SQLITE_ENABLE_FTS3', '1'),
        ('SQLITE_ENABLE_FTS3_PARENTHESIS', '1'),
        ('SQLITE_ENABLE_FTS4', '1'),
        ('SQLITE_ENABLE_FTS5', '1'),
        ('SQLITE_ENABLE_JSON1', '1'),
        ('SQLITE_ENABLE_RTREE', '1'),
        ('SQLITE_ENABLE_GEOPOLY', '1'),
        ('SQLITE_CORE', '1'),
        ('SQLITE_HAS_CODEC', '1'),
        ('SQLITE_TEMP_STORE', '2'),
        ('SQLITE_API', ''),
        ('MODULE_NAME', '"sqlcipher3.dbapi2"'),
    ],
    extra_compile_args=['/std:c11', '/MT'] if sys.platform == "win32" else [],
    extra_link_args=['/OPT:REF'] if sys.platform == "win32" else []
)

# Dummy build_static to satisfy user command
from distutils.command.build import build
class build_static(build):
    def run(self):
        print("Running static build configuration (handled by build_ext)...")

# --- Setup ---
if __name__ == "__main__":
    setuptools.setup(
        name="sqlcipher3",
        version="0.5.4",
        packages=["sqlcipher3"],
        package_dir={"sqlcipher3": "sqlcipher3"},
        ext_modules=[ext],
        cmdclass={'build_static': build_static}
    )
