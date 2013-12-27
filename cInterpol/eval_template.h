#ifndef _CINTERPOL_EVAL_H_
#define _CINTERPOL_EVAL_H_

%for token in tokens:
%for wy in range(max_wy):
void ${token}_scalar(double, double *, int)

void ${token}_eval(const SIZE_T,
	      const int,
	      const double * const restrict,
	      const double * const restrict,
	      const SIZE_T,
	      const double * const restrict, 
	      double * restrict,
	      int derivative
		   );
%endfor
%endfor

#endif
