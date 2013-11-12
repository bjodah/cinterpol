#include <math.h>
#include <stdio.h>
%if SIZE_T == 'size_t':
#include <stdlib.h> /* size_t */
%endif
#include "newton_interval.h"
#include "eval.h"

%for token in tokens:
%for wy in range(max_wy):
double ${token}_scalar_${wy}(double t, double * c, int deriv)
{
  switch (deriv){
%for i in range(max_deriv)
  case (${i})
    return ${eval_scalar_expr[token][i]};
%endfor
   }
}

void ${token}_eval_${wy}(const ${SIZE_T} nt,
			 const double * const restrict t,
			 const double * const restrict c,
			 const ${SIZE_T} nout,
			 const double * const restrict tout, 
			 double * restrict yout,
			 int derivative
			 ){
  // derivative = 0 evaluates function value, 1 evaluates first
  // derivative and so on..
  int j;
  ${SIZE_T} ti = nt; // max: nt-1, nt considered "uninitialized"
  ${SIZE_T} oi; // iterators for t, tout and chunk

#pragma omp parallel for private(j) firstprivate(ti) schedule(static)
  for (oi=0; oi<nout; ++oi){
    // Set ti
    if (ti == nt){ // ti == nt considered uninitialized!
      ti = get_interval(t, nt, tout[oi]);
      if (ti == -1)
	ti = 0;
    }
    else{
      ti = get_interval_from_guess(t, nt, tout[oi], ti);
      if (ti == -1)
	ti = 0;
    }

    // Calculate value of yout[oi] at tout[oi]
    switch (derivative){
    %for deriv, deriv_expr in enumerate(eval_deriv_exprs[token]):
      case (${deriv})
        yout[oi] = ${deriv_expr[token]};
        break;
    %endfor
    }
  }
  
  return 0; // All went well
}

%endfor
%endfor
