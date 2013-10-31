#!/bin/bash
# TODO: make setup.py do this
for f in {piecewise.c, fornberg_wrapper.c}
do
    rm ${f}
    cython piecewise.pyx
    gcc -fpreprocessed -dD -E ${f} | bzip2 > ${f}.bz2
done
