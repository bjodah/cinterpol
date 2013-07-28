#include <stdlib.h> // malloc, free
#include "newton_interval.h" // get_interval

/*
Algorithm from:
Generation of Finite Difference Formulas on Arbitrarily Spaced Grids;
Bengt Fornberg; Mathematics of compuation, 51, 184, 1988, 699-706

The notation below closely corresponds that used in the paper.

Implemented by Björn Dahlgren (c) 2013, released as opensource
under the 2 clause BSD license
*/

inline double min(double a, double b){
  return a < b ? a : b;
}

void _populate_delta(int M, int nx, const double * restrict x_list,
		     double x0, double * restrict delta){
  // M is order
  // allocs delta and returns a pointer to it.
  int N = nx - 1;
  int nm_min_p1;
  double c1 = 1.0;
  double c2, c3;
  int s0 = N+1;
  int s1 = (N+1)*(N+1);
  delta[0] = 1.0;
  for (int n=1; n<N+1; ++n){
    nm_min_p1 = min(n,M)+1;
    c2 = 1.0;
    for (int nu=0; nu<n; ++nu){
      c3 = x_list[n]-x_list[nu];
      c2 = c2 * c3;
      if (n <= M)
	delta[n*s1+(n-1)*s0+nu] = 0.0;
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
}


double _apply_finite_difference_at_point(int order, int nx,
					const double * xarr, 
					const double * yarr,
					double x0, double * delta){
  double result = 0.0;
  int N = nx - 1;
  int s0 = N+1;
  int s1 = (N+1)*(N+1);
  int alloc_delta = 0;
  if (delta == NULL){
    alloc_delta = 1;
    delta = malloc(sizeof(double)*(order+1)*(N+1)*(N+1));
    for (int i = 0; i < (order+1)*(N+1)*(N+1); ++i)
      {
	delta[i] = 0.0;
      }
  }
  _populate_delta(order, nx, xarr, x0, delta);
  for (int nu=0; nu < nx; ++nu){
    result = result + delta[order*s1+N*s0+nu]*yarr[nu];
  }
  if (alloc_delta) 
    free(delta);
  return result;
}

double apply_finite_difference_at_point(int order, int nx,
					const double * xarr, 
					const double * yarr,
					double x0){
  return _apply_finite_difference_at_point(
     order, nx, xarr, yarr, x0, NULL);
}


int apply_finite_difference_over_array(
        int nx, const double * xarr, const double * yarr,
	int nreq, const double * xreq, int order, int ntail,
	int nhead, double * yout) {
  double curx;
  int curi;
  int N;
  double * delta;
  N = ntail+nhead;
  if (N > nx)
    return 1;
  delta = malloc(sizeof(double)*(order+1)*(N+1)*(N+1));
  for (int i = 0; i < (order+1)*(N+1)*(N+1); ++i){
      delta[i] = 0.0;
    }
  for (int i=0; i<nreq; ++i){
    curx = xreq[i];
    curi = get_interval(xarr, nx, curx);
    if (curi < ntail-1)
      curi = ntail-1;
    if (nx-curi < N)
      curi = nx-N-1;
    yout[i] = _apply_finite_difference_at_point(
        order, N, &xarr[curi-ntail+1],
	&yarr[curi-ntail+1], curx, delta);
  }
  free(delta);
  return 0;
}

