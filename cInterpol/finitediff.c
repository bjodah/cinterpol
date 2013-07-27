#include <stdlib.h> // malloc, free
#include "newton_interval.h" // get_interval

/*
Algorithm from:
Generation of Finite Difference Formulas on Arbitrarily Spaced Grids, Bengt Fornberg
Mathematics of compuation, 51, 184, 1988, 699-706

The notation below closely corresponds that used in the paper.
*/

inline double min(double a, double b){
  return a < b ? a : b;
}

double * _get_delta(int M, int nx, const double * x_list, double x0){
  // M is order
  // allocs delta and returns a pointer to it.
  int N = nx - 1;
  int nm_min_p1;
  double c1 = 1.0;
  double c2, c3;
  int s0 = N+1;
  int s1 = (N+1)*(N+1);
  double * delta = malloc(sizeof(double)*(M+1)*(N+1)*(N+1));
  delta[0] = 1.0;
  for (int n=1; n<N+1; ++n){
    c2 = 1.0;
    for (int nu=0; nu<n; ++nu){
      c3 = x_list[n]-x_list[nu];
      c2 = c2 * c3;
      if (n <= M)
	delta[n*s1+(n-1)*s0+nu] = 0.0;
      nm_min_p1 = min(n,M)+1;
      for (int m=0; m<nm_min_p1; ++m){
	delta[m*s1+n*s0+nu] = ((x_list[n]-x0)*delta[m*s1+(n-1)*s0+nu] -
			       m*delta[(m-1)*s1+(n-1)*s0+nu])/c3;
      }
    }
    for (int m=0; m<nm_min_p1; ++m){
      delta[m*s1+n*s0+n] = c1/c2*(m*delta[(m-1)*s1+(n-1)*s0+n-1]
				  - (x_list[n-1]-x0)*delta[m*s1+(n-1)*s0+n-1]);
    }
    c1 = c2;
  }
  return delta;
}

double apply_finite_difference_at_point(int order, int nx,
					const double * xarr, 
					const double * yarr,
					double x0){
  double result = 0.0;
  int N = nx - 1;
  int s0 = N+1;
  int s1 = (N+1)*(N+1);
  
  double * delta = _get_delta(order, nx, xarr, x0);
  for (int nu=0; nu < nx; ++nu){
    result = result + delta[order*s1+N*s0+nu]*yarr[nu];
  }
  free(delta);
  return result;
}

int apply_finite_difference_over_array(
        int nx, const double * xarr, const double * yarr,
	int nreq, const double * xreq, int order, int ntail,
	int nhead, double * yout) {
  double curx;
  int curi;
  if (ntail+nhead > nx)
    return 1;
  for (int i=0; i<nreq; ++i){
    curx = xreq[i];
    curi = get_interval(xarr, nx, curx);
    if (curi < ntail-1)
      curi = ntail-1;
    if (nx-curi < nhead+ntail)
      curi = nx-nhead-ntail-1;
    yout[i] = apply_finite_difference_at_point(
        order, ntail+nhead, &xarr[curi-ntail+1],
	&yarr[curi-ntail+1], curx);
  }
  return 0;
}

