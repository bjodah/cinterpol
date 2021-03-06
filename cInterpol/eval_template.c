// ${_warning_in_the_generated_file_not_to_edit}
//#include <math.h>
#include "power.c"
//#include <stdio.h>
%if SIZE_T == 'size_t':
#include <stdlib.h> /* size_t */
%endif
#include "newton_interval.h"

#define BREAKEVEN 100 // TODO: determine a typical value for this

// we only have integer exponents in pow, use specialized verion:
#define pow(arg1, arg2) power(arg1, arg2)
%for token in tokens:
%for wy in range(1, max_wy+1):
%for i in range(max_deriv[wy]+1):

double ${token}_scalar_${wy}_${i}(
    const double x, const double * const restrict c, const ${SIZE_T} offset)
{
% for cse_token, cse_def in eval_cse[token][wy][i]:
    const double ${cse_token} = ${cse_def};
% endfor
    return ${eval_expr[token][wy][i][0]};
}

void ${token}_eval_${wy}_${i}(
    const ${SIZE_T} nx,
    const double * const restrict x,
    const double * const restrict c,
    const ${SIZE_T} nout,
    const double * const restrict xout, 
    double * const restrict yout
    )
{
    // derivative = 0 evaluates function value, 1 evaluates first
    // derivative and so on..
    ${SIZE_T} xi = nx; // max: nx-1, nx considered "uninitialized"

#pragma omp parallel for firstprivate(xi) schedule(static) if (nout > BREAKEVEN)
    for (${SIZE_T} oi=0; oi<nout; ++oi){
	// Set xi
	if (xi == nx){ // xi == nx considered uninitialized!
	    xi = get_interval(x, nx, xout[oi]);
	    if (xi == -1)
		xi = 0;
	}
	else{
	    xi = get_interval_from_guess(x, nx, xout[oi], xi);
	    if (xi == -1)
		xi = 0;
	}

	// Calculate value of yout[oi] at xout[oi]
	// for shifted coefficients.
	yout[oi] = ${token}_scalar_${wy}_${i}(xout[oi]-x[xi], c, xi*${wy}*2);
    }
}
%endfor
%endfor
%endfor
#undef pow(arg1, arg2)
