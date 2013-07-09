#include <math.h>
#include <stdbool.h> /* bool */
#include <stdlib.h> /* size_t */

/* MAKO TEMPLATE INIT */

void poly_coeff1(const double *restrict t, const double *restrict y, double *restrict c, const size_t nt){
  /*
    solve shifted first order coeff
  */
  size_t i;
  double dt;
  /* BEGIN MAKO TEMPLATE */
  /* END MAKO TEMPLATE */
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */

      c[i*2+0] = y[i*1+0];
      c[i*2+1] = (y[(i+1)*1+0] - y[i*1+0])/dt;
      /* END MAKO TEMPLATE */
    }
  /* Last coefficient is half order (extrapolation solely on last point in series)*/
  /* BEGIN MAKO TEMPLATE */
  c[i*2+0] = y[i*1+0];
  c[i*2+1] = 0;
  /* END MAKO TEMPLATE */

}
