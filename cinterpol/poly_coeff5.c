#include <math.h>
#include <stdbool.h> /* bool */
#include <stdlib.h> /* size_t */

/* MAKO TEMPLATE INIT */

void poly_coeff5(double t[], double y[], double c[], size_t nt){
  /*
    solve shifted first order coeff
  */
  size_t i;
  double dt;
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */
      c[i*6+0] = y[i*3+0];
      c[i*6+1] = y[i*3+1];
      c[i*6+2] = (1.0L/2.0L)*y[i*3+2];
      c[i*6+3] = (1.0L/2.0L)*(-3*pow(dt, 2)*y[i*3+2] + pow(dt, 2)*y[(i+1)*3+2] - 12*dt*y[i*3+1] - 8*dt*y[(i+1)*3+1] - 20*y[i*3+0] + 20*y[(i+1)*3+0])/pow(dt, 3);
      c[i*6+4] = ((3.0L/2.0L)*pow(dt, 2)*y[i*3+2] - pow(dt, 2)*y[(i+1)*3+2] + 8*dt*y[i*3+1] + 7*dt*y[(i+1)*3+1] + 15*y[i*3+0] - 15*y[(i+1)*3+0])/pow(dt, 4);
      c[i*6+5] = (1.0L/2.0L)*(-pow(dt, 2)*y[i*3+2] + pow(dt, 2)*y[(i+1)*3+2] - 6*dt*y[i*3+1] - 6*dt*y[(i+1)*3+1] - 12*y[i*3+0] + 12*y[(i+1)*3+0])/pow(dt, 5);
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
