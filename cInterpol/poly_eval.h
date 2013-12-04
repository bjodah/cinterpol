#ifndef _POLY_EVAL_H_
#define _POLY_EVAL_H_
#define SIZE_T int // 32bit signed integer is ~2e9

int
poly_eval(const SIZE_T nt,
	  const int order,
	  const double * const restrict t,
	  const double * const restrict c,
	  const SIZE_T nout,
	  const double * const restrict tout, 
	  double * restrict yout,
	  int derivative
	  );
#endif /* _POLY_EVAL_H_ */
