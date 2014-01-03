CC=gcc
CFLAGS=-std=c99
NEWTON_SRC=../newton_interval/src
NEWTON_INC=../newton_interval/include
.PHONY: tests

tests: test_eval test_PiecewisePolynomial.py
	@./test_eval
	@env PYTHONPATH=${CURDIR}/../..:${PYTHONPATH} python test_PiecewisePolynomial.py

test_eval: $(NEWTON_INC)/newton_interval.h $(NEWTON_SRC)/newton_interval.c ../eval.c test_eval.c unittest.c unittest.h
	$(CC) $(CFLAGS) -I$(NEWTON_INC) -g -fopenmp -o $@ $(NEWTON_SRC)/newton_interval.c unittest.c test_eval.c -lm
