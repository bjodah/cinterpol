.PHONY: tests

tests: test_newton_interval test_poly_eval test_PiecewisePolynomial.py test_finitediff.py
	@./test_newton_interval
	@./test_poly_eval
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_PiecewisePolynomial.py
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_finitediff.py

test_newton_interval: ../newton_interval.h ../newton_interval.c test_newton_interval.c unittest.c unittest.h
	gcc -g -o $@ ../newton_interval.c unittest.c test_newton_interval.c -lm

test_poly_eval: ../newton_interval.h ../newton_interval.c ../poly_eval.h ../poly_eval.c test_poly_eval.c unittest.c unittest.h
	gcc -g -std=c99 -fopenmp -o $@ ../newton_interval.c ../poly_eval.c unittest.c test_poly_eval.c -lm
