#include <math.h>
#include <stdbool.h> /* bool */
#include <stdlib.h> /* size_t */

/* MAKO TEMPLATE INIT */

void poly_coeff${ORDER}(const double *restrict t, const double *restrict y, double *restrict c, const size_t nt){
  /*
    solve shifted first order coeff
  */
  size_t i;
  double dt;
  /* BEGIN MAKO TEMPLATE */
  % for expr in cse_def:
  ${expr}
  % endfor
  /* END MAKO TEMPLATE */
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
      /* BEGIN MAKO TEMPLATE */
      % for expr in cse_block:
      ${expr}
      % endfor

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
