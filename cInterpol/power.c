// Generated C99 source from Mako (Python templating engine) template: pow_template.c
// tune: 
//    switch_max: [1,2,3,4,5,6,7,8]
//    unrolled: [True,False]
//    negexp: [0,1]
// vendor:
//    gnu, intel
// optimize:
//    -O2, -O3



static double power(const double num, const int exp) {
    // should be fast! (watch out for underflow/overflow)
    if (exp < 0) return 1.0/power(num, -exp);
    double result;
    switch (exp){
    case 0:
	return 1.0;
    case 1:
	return num;
    case 2:
	result = num*num;
	
	return result;
    case 3:
	result = num*num;
	
	result *= num;
	return result;
    case 4:
	result = num*num;
	result *= result;
	return result;
    case 5:
	result = num*num;
	result *= result;
	result *= num;
	return result;
    default:
	result = power(num, exp/2);
	result *= result;
	if ((exp%2) == 1) result *= num;
	return result;
    }
}

