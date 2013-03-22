#include "newton_interval.h"
/* #include <stdio.h> */

size_t get_interval(const double arr[], const size_t N, const double t){
  /*
    get_interval locates the index `i` for which  is
      t > arr[i] and arr[i+1] > t
  */
  double t0 = arr[0];
  double tend = arr[N-1];
  size_t sqrt_nt = (size_t)sqrt((double)N); /* Delta i for estimated derivative */
  size_t i = (size_t)((t - t0)/(tend - t0) * N);
  size_t h; /* step in num der */
  size_t di; /* Delta i (update step in root finding) */
  double dtdi;
  size_t lower_bound = -1;
  size_t upper_bound = N;
  bool gteq_ti;    /* t >= t[i] */
  bool lt_tip1;    /* t < t[i+1] */
  bool eq_tip1;    /* t == t[i+1] */

  /* i might max be N */
  if (i > N - 2){
    i = N - 2;
  }
  gteq_ti = (t >= arr[i]);
  lt_tip1 = (t < arr[i + 1]);
  eq_tip1 = (t == arr[i + 1]);

  if (eq_tip1) return i + 1;

  while (!(gteq_ti & lt_tip1)){
    if (gteq_ti) {
      h = -sqrt_nt;
    }
    else{
      h = sqrt_nt;
    }
    /* Check we're not out of explored boundaries; */
    while (((i + h) > upper_bound) | ((i + h) < lower_bound)){
        h /= 2;
    }
    dtdi = (arr[i+h] - arr[i]) / h;
    di = (size_t)round((arr[i] - t) / dtdi);
    /* Check we're not out of explored boundaries; */
    while (((i + di) > upper_bound) | ((i + di) < lower_bound)){
      di /= 2; /* What happens if di=0? Could that happen? */
    }
    /* Update lower and upper boundaries; */
    if (i + di > lower_bound)
      lower_bound = i;
    if (i + di < upper_bound)
      upper_bound = i;
    /* Update i; */
    i += di;
    /* Update loop conditions; */
    gteq_ti = (t >= arr[i]);
    lt_tip1 = (t < arr[i + 1]);
    eq_tip1 = (t == arr[i + 1]);
    if (eq_tip1) return i + 1;
  }
  return i;
}
