#include <math.h>
#include <stdbool.h> /* bool */
#include <stdlib.h> /* size_t */

/* MAKO TEMPLATE INIT */

void poly_coeff3(double t[], double y[], double c[], size_t nt){
  /*
    solve shifted first order coeff
  */
  size_t i;
  double dt;
  /* BEGIN MAKO TEMPLATE */
  double x0;
  /* END MAKO TEMPLATE */
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */
      x0 = pow(dt, 2);

      c[i*4+0] = y[i*2+0];
      c[i*4+1] = y[i*2+1];
      c[i*4+2] = -(dt*y[(i+1)*2+1] + 2*dt*y[i*2+1] - 3*y[(i+1)*2+0] + 3*y[i*2+0])/x0;
      c[i*4+3] = (y[(i+1)*2+1] + y[i*2+1] - 2*(y[(i+1)*2+0] - y[i*2+0])/dt)/x0;
      /* END MAKO TEMPLATE */
    }
  /* Last coefficient is half order (extrapolation solely on last point in series)*/
  /* BEGIN MAKO TEMPLATE */
  c[i*4+0] = y[i*2+0];
  c[i*4+1] = y[i*2+1];
  c[i*4+2] = 0;
  c[i*4+3] = 0;
  /* END MAKO TEMPLATE */

}
