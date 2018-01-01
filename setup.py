from distutils.core import setup, Extension

setup(
    ext_modules=[ Extension("_readcount", ["_readcount.c", "readcount.c"], libraries=['wiringPi']) ]
)
