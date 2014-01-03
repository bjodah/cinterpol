#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "../eval.c" // we need to test some static functions
#include "unittest.h"

int test_poly_eval_2_0(){
  // y=x**3
  int ok = 1;
  int nt = 2;
  int order=3;
  const double t[2] = {0.0, 1.0};
  const double c[8] = {0.0, 0.0,  0.0, 1.0, \
		      -1.0, 3.0, -3.0, 1.0};
  int nout = 5;
  const double tout[5] = {-1.0, 0.0, 0.5, 1.0, 2.0};
  double * yout = malloc(5*sizeof(double));

  poly_eval_2_0(nt, t, c, nout, tout, yout);
  for (int i=0; i<nout; ++i){
    if (pow(tout[i],3) != yout[i])
      ok = 0; break;
  }
  free(yout);
  return ok;
}

#define NTESTS 1
static const TestCase t1 = {test_poly_eval_2_0, "test_poly_eval_2_0"};
static const TestCase* test_cases[NTESTS] = {&t1};

int main(int argc, char ** argv){
  int result, i;
  return run_tests(NTESTS, test_cases, argv[0]);
}
