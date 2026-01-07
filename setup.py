# -*- coding: ISO-8859-1 -*-
# setup.py: the distutils script
#

# MANY THANKS to @laggykiller for implementing all of this so we can enjoy
# wheels (within wheels, within wheels).
import glob
import json
import os
import platform
import subprocess
import sys

from setuptools import setup, Extension


PACKAGE_NAME = 'sqlcipher3'
VERSION = '0.6.2'

CONAN_ARCHS = {
    'x86_64': ['amd64', 'x86_64', 'x64'],
    'x86': ['i386', 'i686', 'x86'],
    'armv8': ['arm64', 'aarch64', 'aarch64_be', 'armv8b', 'armv8l'],
}

# define sqlite sources
sources = glob.glob('src/*.c') + ['vendor/sqlite3.c']
library_dirs = []
include_dirs = ['./src']

def get_native_arch():
    arch = platform.machine().lower()
    for k, v in CONAN_ARCHS.items():
        if arch in v:
            return k
    return arch

def get_arch():
    arch_env = os.getenv('SQLCIPHER3_COMPILE_TARGET')
    if isinstance(arch_env, str):
        return arch_env

    return get_native_arch()

def install_openssl(arch):
    settings: list[str] = []
    options: list[str] = []

    if platform.system() == 'Windows':
        settings.append('os=Windows')
    elif platform.system() == 'Darwin':
        settings.append('os=Macos')
        if arch == 'x86_64':
            settings.append('os.version=10.9')
        else:
            settings.append('os.version=11.0')
        settings.append('compiler=apple-clang')
        settings.append('compiler.libcxx=libc++')
    elif platform.system() == 'Linux':
        settings.append('os=Linux')

    settings.append('arch=%s' % arch)
    options.append('openssl/*:no_zlib=True')

    build = ['missing']

    # Need to compile openssl if musllinux.
    if os.path.isdir('/lib') and any(e.startswith('libc.musl') for e in os.listdir('/lib')):
        build.append('openssl*')

    subprocess.run(['conan', 'profile', 'detect', '-f'])
    # Latest openssl need center2.conan.io instead of center.conan.io
    subprocess.run(['conan', 'remote', 'update', 'conancenter', '--url=https://center2.conan.io'])

    conan_output = os.path.join('conan_output', arch)
    result = subprocess.run([
        'conan', 'install',
        *[x for s in settings for x in ('-s', s)],
        *[x for b in build for x in ('-b', b)],
        *[x for o in options for x in ('-o', o)],
        '-of', conan_output, '--deployer=direct_deploy', '--format=json', '.'
        ], stdout=subprocess.PIPE).stdout.decode()

    conan_info = json.loads(result)

    return conan_info


def add_deps(conan_info):
    library_dirs = []
    include_dirs = []
    for dep in conan_info['graph']['nodes'].values():
        package_folder = dep.get('package_folder')
        if package_folder is None:
            continue

        library_dirs.append(os.path.join(package_folder, 'lib'))
        include_dirs.append(os.path.join(package_folder, 'include'))

    return library_dirs, include_dirs

def quote_argument(arg: str) -> str:
    is_cibuildwheel = os.environ.get('CIBUILDWHEEL', '0') == '1'

    if sys.platform == 'win32' and (
        (is_cibuildwheel and sys.version_info < (3, 7))
        or (not is_cibuildwheel and sys.version_info < (3, 9))
    ):
        q = '\\"'
    else:
        q = '"'

    return q + arg + q

if __name__ == '__main__':
    define_macros = [
        ('MODULE_NAME', quote_argument('sqlcipher3.dbapi2')),
        ('SQLITE_ENABLE_FTS3', '1'),
        ('SQLITE_ENABLE_FTS3_PARENTHESIS', '1'),
        ('SQLITE_ENABLE_FTS4', '1'),
        ('SQLITE_ENABLE_FTS5', '1'),
        ('SQLITE_ENABLE_JSON1', '1'),
        ('SQLITE_ENABLE_LOAD_EXTENSION', '1'),
        ('SQLITE_ENABLE_RTREE', '1'),
        ('SQLITE_ENABLE_STAT4', '1'),
        ('SQLITE_ENABLE_UPDATE_DELETE_LIMIT', '1'),
        ('SQLITE_SOUNDEX', '1'),
        ('SQLITE_USE_URI', '1'),
        # Required for SQLCipher.
        ('SQLITE_HAS_CODEC', '1'),
        ('SQLITE_TEMP_STORE', '2'),
        ('SQLITE_THREADSAFE', '1'),
        ('SQLITE_EXTRA_INIT', 'sqlcipher_extra_init'),
        ('SQLITE_EXTRA_SHUTDOWN', 'sqlcipher_extra_shutdown'),
        ('HAVE_STDINT_H', '1'),
        # Increase the maximum number of "host parameters".
        ('SQLITE_MAX_VARIABLE_NUMBER', '250000'),
        # Additional nice-to-have.
        ('SQLITE_DEFAULT_PAGE_SIZE', '4096'),
        ('SQLITE_DEFAULT_CACHE_SIZE', '-8000'),
        ('inline', '__inline'),
    ]

    try:
        import conan
    except ImportError:
        library_dirs = include_dirs = []
    else:
        # Configure the compiler
        arch = get_arch()
        if arch == "universal2":
            # https://docs.conan.io/2/reference/tools/cmake/cmaketoolchain.html#conan-tools-cmaketoolchain-universal-binaries
            conan_info = install_openssl("armv8|x86_64")
        else:
            conan_info = install_openssl(arch)
        library_dirs, include_dirs = add_deps(conan_info)

    extra_compile_args = ['-Qunused-arguments'] if sys.platform == 'darwin' else []

    # Configure the linker
    extra_link_args = []
    if sys.platform == 'win32':
        # https://github.com/openssl/openssl/blob/master/NOTES-WINDOWS.md#linking-native-applications
        extra_link_args.append('WS2_32.LIB')
        extra_link_args.append('GDI32.LIB')
        extra_link_args.append('ADVAPI32.LIB')
        extra_link_args.append('CRYPT32.LIB')
        extra_link_args.append('USER32.LIB')
        extra_link_args.append('libcrypto.lib')
    else:
        # Include math library, required for fts5, and crypto.
        extra_link_args.extend(['-lm', '-lcrypto'])

    module = Extension(
        name='sqlcipher3._sqlite3',
        sources=sources,
        define_macros=define_macros,
        library_dirs=library_dirs,
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
        language='c')

    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        package_dir={PACKAGE_NAME: PACKAGE_NAME},
        packages=[PACKAGE_NAME],
        ext_modules=[module])
