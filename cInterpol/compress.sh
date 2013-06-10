#!/bin/bash
# TODO: make setup.py do this
rm core.c
cython core.pyx
gcc -fpreprocessed -dD -E core.c | bzip2 > core.c.bz2
