#ifndef _CINTERPOL_COEFF_H_
#define _CINTERPOL_COEFF_H_

%for token in tokens:
%for wy in range(max_wy):
void ${token}_coeff${wy}(const double *restrict,
			 const double *restrict, 
			 double *restrict, 
			 const size_t);
%endfor
%endfor

#endif
