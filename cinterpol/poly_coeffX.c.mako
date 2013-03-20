#include <math.h>
#include <stdbool.h> /* bool */
#include <stdlib.h> /* size_t */

/* MAKO TEMPLATE INIT */

void poly_coeff${ORDER}(double t[], double y[], double c[], size_t nt){
  /*
    solve shifted first order coeff
  */
  size_t i;
  double dt;
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */
      % for expr in main_block:
      ${expr}
      % endfor
      /* END MAKO TEMPLATE */
    }
  /* Last coefficient is half order (extrapolation solely on last point in series)*/
  /* BEGIN MAKO TEMPLATE */
  % for expr in end_block:
  ${expr}
  % endfor
  /* END MAKO TEMPLATE */

}
