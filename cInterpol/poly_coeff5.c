#include <math.h>
#include <stdbool.h> /* bool */
#include <stdlib.h> /* size_t */

/* MAKO TEMPLATE INIT */

void poly_coeff5(const double t[], const double y[], double c[], const size_t nt){
  /*
    solve shifted first order coeff
  */
  size_t i;
  double dt;
  /* BEGIN MAKO TEMPLATE */
  double x0;
  double x1;
  double x2;
  double x3;
  double x4;
  double x5;
  double x6;
  double x7;
  /* END MAKO TEMPLATE */
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */
      x0 = -1.0L/2.0L;
      x1 = pow(dt, 2);
      x2 = -y[(i+1)*3+0];
      x3 = dt*y[(i+1)*3+1];
      x4 = dt*y[i*3+1];
      x5 = x1*y[i*3+2];
      x6 = -x1*y[(i+1)*3+2];
      x7 = 3*x5;

      c[i*6+0] = y[i*3+0];
      c[i*6+1] = y[i*3+1];
      c[i*6+2] = -x0*y[i*3+2];
      c[i*6+3] = x0*(20*x2 + 8*x3 + 12*x4 + x6 + x7 + 20*y[i*3+0])/pow(dt, 3);
      c[i*6+4] = -x0*(30*x2 + 14*x3 + 16*x4 + 2*x6 + x7 + 30*y[i*3+0])/pow(dt, 4);
      c[i*6+5] = x0*(12*x2 + 6*x3 + 6*x4 + x5 + x6 + 12*y[i*3+0])/pow(dt, 5);
      /* END MAKO TEMPLATE */
    }
  /* Last coefficient is half order (extrapolation solely on last point in series)*/
  /* BEGIN MAKO TEMPLATE */
  c[i*6+0] = y[i*3+0];
  c[i*6+1] = y[i*3+1];
  c[i*6+2] = y[i*3+2];
  c[i*6+3] = 0;
  c[i*6+4] = 0;
  c[i*6+5] = 0;
  /* END MAKO TEMPLATE */

}
