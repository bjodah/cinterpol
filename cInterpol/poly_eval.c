#include <math.h>
/* #include <stdio.h> */
#include "newton_interval.h"
#include "poly_eval.h"

// poly_eval.h defines a SIZE_T (now: int - 32bit signed integer => max ~= 2e9)

double power(double num, int exp) {
  // Only valid for positive exp
  // should be fast!
  double result;
  switch (exp){
  case 0:
    return 1.0;
  case 1:
    return num;
  default:
    result = power(num, exp/2);
    result *= result;
    if ((exp%2) == 1) result *= num;
    return result;
  }
}


int partfact(int order, int deriv){
  // Example partfact(3,0) == 1
  //         partfact(3,1) == 3
  //         partfact(3,2) == 3*2
  //         partfact(3,3) == 0
  //         partfact(5,3) == 5*4*3
  if (deriv == 0){
    return 1;
  }
  else if (deriv >= order){
    return 0;
  }
  else {
    int tmp = 1;
    for (int i=order; i > order-deriv; i--)
      tmp *= i;
    return tmp;
  }
}

int poly_eval(const SIZE_T nt,
	      const int order,
	      const double * const restrict t,
	      const double * const restrict c,
	      const SIZE_T nout,
	      const double * const restrict tout, 
	      double * restrict yout,
	      int derivative
	      ){
  // derivative = 0 evaluates function value, 1 evaluates first
  // derivative and so on..
  int j;
  SIZE_T ti = nt/2; // max: nt-1, nt considered "uninitialized"
  SIZE_T oi; // iterators for t, tout and chunk

  if (derivative > order) return 1; // One probably does not want to do that.

#pragma omp parallel for private(j) firstprivate(ti) schedule(static)
  for (oi=0; oi<nout; ++oi){
    /* printf ("(About to call get_interval_from_guess)\n"); */
    /* printf ("with nt=%d tout[%d]=%5.2f ti=%d\n", nt, oi, tout[oi], ti); fflush(stdout); */
    ti = get_interval_from_guess(t, nt, tout[oi], ti);
    /* printf ("Back from get_interval_from_guess\n"); fflush(stdout); */
    if (ti == -1)
      ti = 0;

    // Calculate value of yout[oi] at tout[oi]
    yout[oi] = 0.0;
    for (j=derivative; j<order+1; ++j){
      /* printf ("j=%d, order=%d\n",j,order); fflush(stdout); */
      yout[oi] += partfact(j, derivative) * \
	power(tout[oi] - t[ti], j-derivative) * \
	c[ti*(order+1)+j];
    }
  }
  /* printf ("returning from poly_eval\n"); */
  return 0; // All went well
}
