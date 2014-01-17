#ifndef _CINTERPOL_COEFF_H_
#define _CINTERPOL_COEFF_H_

//${_warning_in_the_generated_file_not_to_edit}

%for token in tokens:
%for wy in range(max_wy):
void ${token}_coeff${wy}(const double * const restrict,
			 const double * const restrict, 
			 double * const restrict, 
			 const ${SIZE_T});
%endfor
%endfor

#endif
