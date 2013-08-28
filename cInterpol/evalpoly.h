#ifndef _EVALPOLY_H_
#define _EVALPOLY_H_
#define SIZE_T int // 32bit signed integer is ~2e9

double power(double num, int exp);

int
partfact(int order, int deriv);

int
evalpoly(const SIZE_T nt,
	 const int order,
	 const double * const restrict t,
	 const double * const restrict c,
	 const SIZE_T nout,
	 const double * const restrict tout, 
	 double * restrict yout,
	 int derivative
	 );
#endif /* _EVALPOLY_H_ */
