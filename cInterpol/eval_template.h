#ifndef _CINTERPOL_EVAL_H_
#define _CINTERPOL_EVAL_H_

// ${_warning_in_the_generated_file_not_to_edit}

%for token in tokens:
%for wy in range(1, max_wy+1):
%for i in range(max_deriv[wy]+1):
void ${token}_scalar_${wy}_${i}(const double, const double * const restrict, const ${SIZE_T})

void ${token}_eval_${wy}_${i}(
    const ${SIZE_T},
    const double * const restrict,
    const double * const restrict,
    const ${SIZE_T},
    const double * const restrict, 
    double * const restrict,
    );
%endfor
%endfor
%endfor

#endif
