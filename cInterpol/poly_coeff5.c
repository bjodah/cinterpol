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
  /* END MAKO TEMPLATE */
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */
      x0 = pow(dt, 2);
      x1 = -y[(i+1)*3+0];
      x2 = dt*y[(i+1)*3+1];
      x3 = dt*y[i*3+1];
      x4 = 3*x0*y[i*3+2];

      c[i*6+0] = y[i*3+0];
      c[i*6+1] = y[i*3+1];
      c[i*6+2] = (1.0L/2.0L)*y[i*3+2];
      c[i*6+3] = (1.0L/2.0L)*(x0*y[(i+1)*3+2] - 20*x1 - 8*x2 - 12*x3 - x4 - 20*y[i*3+0])/pow(dt, 3);
      c[i*6+4] = (1.0L/2.0L)*(-2*x0*y[(i+1)*3+2] + 30*x1 + 14*x2 + 16*x3 + x4 + 30*y[i*3+0])/pow(dt, 4);
      c[i*6+5] = (1.0L/2.0L)*(x0*(y[(i+1)*3+2] - y[i*3+2]) - 6*dt*(y[(i+1)*3+1] + y[i*3+1]) + 12*y[(i+1)*3+0] - 12*y[i*3+0])/pow(dt, 5);
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
