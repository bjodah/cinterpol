CC=gcc
CFLAGS=-std=c99
FC=gfortran
FFLAGS=-std=f2008
.PHONY: tests

tests: test_newton_interval test_poly_eval test_PiecewisePolynomial.py test_finitediff.py test_fornberg
	@./test_newton_interval
	@./test_poly_eval
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_PiecewisePolynomial.py
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_finitediff.py
	@./test_fornberg

test_newton_interval: ../newton_interval.h ../newton_interval.c test_newton_interval.c unittest.c unittest.h
	$(CC) $(CFLAGS) -g -o $@ ../newton_interval.c unittest.c test_newton_interval.c -lm

test_poly_eval: ../newton_interval.h ../newton_interval.c ../poly_eval.h ../poly_eval.c test_poly_eval.c unittest.c unittest.h
	$(CC) $(CFLAGS) -g -std=c99 -fopenmp -o $@ ../newton_interval.c ../poly_eval.c unittest.c test_poly_eval.c -lm

test_fornberg: ../fornberg.f90 test_fornberg.f90
	$(FC) $(FFLAGS) -o $@ $^
