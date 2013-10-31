#include <math.h>
#include <stdbool.h> /* bool */
%if SIZE_T == 'size_t':
#include <stdlib.h> /* size_t */
%endif
#include "coeff.h"

%for token in tokens:
%for wy in range(max_wy):
void ${token}_coeff${wy}(const double *restrict t,
			 const double *restrict y,
			 double *restrict c, 
			 const ${SIZE_T} nt){
  /*
    solve shifted first order coeff
  */
  ${SIZE_T} i;
  double dt;
% for expr in cse_def:
  ${expr}
% endfor
#pragma omp parallel for private(dt${''.join([', '+str(var_name) for var_name, va_expr in cse_defs])}) // i is implicitly priavte
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
    % for expr in cse_block:
      ${expr}
    % endfor

    % for expr in main_block:
      ${expr}
    % endfor
    }
  i = nt-1;
  dt = t[i]-t[i-1];
% for expr in end_block:
  ${expr}
% endfor
}
%endfor
%endfor
