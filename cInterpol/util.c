

double power(double num, int exp) {
  // Only valid for positive exp
  // should be fast!
  double result;
  switch (exp){
  case 0:
    return 1.0;
  case 1:
    return num;
  default:
    result = power(num, exp/2);
    result *= result;
    if ((exp%2) == 1) result *= num;
    return result;
  }
}


int partfact(int order, int deriv){
  // Example partfact(3,0) == 1
  //         partfact(3,1) == 3
  //         partfact(3,2) == 3*2
  //         partfact(3,3) == 0
  //         partfact(5,3) == 5*4*3
  if (deriv == 0){
    return 1;
  }
  else if (deriv >= order){
    return 0;
  }
  else {
    int tmp = 1;
    for (int i=order; i > order-deriv; i--)
      tmp *= i;
    return tmp;
  }
}

/*
Example of how to evaluate derivative of polynomial:

    yout[oi] = 0.0;
    for (j=derivative; j<order+1; ++j)
      yout[oi] += partfact(j, derivative) * \
    	power(tout[oi] - t[ti], j-derivative) * \
    	c[ti*(order+1)+j];

*/
