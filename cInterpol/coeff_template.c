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
% for cse_token, cse_def in coeff_cses[token]:
  double ${cse_token};
% endfor
#pragma omp parallel for private(dt${''.join([', '+str(var_name) for var_name, va_expr in cse_defs])}) // i is implicitly priavte
  for (i=0; i < (nt-1); ++i)
    {
      dt = t[i+1]-t[i];
    % for cse_token, cse_def in coeff_cses[token]:
      ${cse_token} = ${cse_def};
    % endfor

    % for j, expr in enumerate(coeff_exprs_in_cse[token]):
      c[i*2*${wy}+${j}] = ${expr};
    % endfor
    }
  i = nt-1;
  dt = t[i]-t[i-1];
% for j, expr in coeff_end_epxrs[token]:
  c[i*2*${wy}+${j}] = ${expr};
% endfor
}
%endfor
%endfor
