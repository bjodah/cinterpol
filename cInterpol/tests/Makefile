.PHONY: tests

tests: test_newton_interval test_evalpoly test_PiecewisePolynomial.py test_finitediff.py
	@./test_newton_interval
	@./test_evalpoly
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_PiecewisePolynomial.py
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_finitediff.py

test_newton_interval: ../newton_interval.h ../newton_interval.c test_newton_interval.c unittest.c unittest.h
	gcc -g -o $@ ../newton_interval.c unittest.c test_newton_interval.c -lm

test_evalpoly: ../newton_interval.h ../newton_interval.c ../evalpoly.h ../evalpoly.c test_evalpoly.c unittest.c unittest.h
	gcc -g -std=c99 -fopenmp -o $@ ../newton_interval.c ../evalpoly.c unittest.c test_evalpoly.c -lm
