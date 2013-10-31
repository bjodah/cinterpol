#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <math.h>
#include "../poly_eval.h"
#include "unittest.h"

int test_poly_eval_1(){
  // y=x**3
  int ok = 1;
  int nt=2;
  int wy=2;
  const double t[2] = {0.0, 1.0};
  const double c[8] = {0.0, 0.0,  0.0, 1.0, \
		      -1.0, 3.0, -3.0, 1.0};
  int nout = 5;
  const double tout[5] = {-1.0, 0.0, 0.5, 1.0, 2.0};
  double * yout = malloc(5*sizeof(double));

  poly_eval(nt, wy, t, c, nout, tout, yout, 0);
  for (int i=0; i<nout; ++i){
    if (power(tout[i],3) != yout[i])
      ok = 0; break;
  }
  free(yout);
  return ok;
}

int test_partfact_1(){
  int ok = 0;
  ok += (partfact(3,0) == 1);
  ok += (partfact(3,1) == 3);
  ok += (partfact(3,2) == 3*2);
  ok += (partfact(3,3) == 0);
  ok += (partfact(5,3) == 5*4*3);
  return (ok == 5);
}


int test_power_1(){
  int ok = 0;
  ok += (abs(power(2.5, 5)-pow(2.5,5)) < 1e-6);
  ok += (abs(power(2.5, 0)-pow(2.5,0)) < 1e-6);
  ok += (abs(power(2.5, 1)-pow(2.5,1)) < 1e-6);
  ok += (abs(power(0.0, 5)-pow(0.0,5)) < 1e-6);
  ok += (abs(power(0.0, 0)-pow(0.0,0)) < 1e-6);
  ok += (abs(power(0.0, 1)-pow(0.0,1)) < 1e-6);
  ok += (abs(power(-3.5, 5)-pow(-3.5,5)) < 1e-6);
  ok += (abs(power(-3.5, 0)-pow(-3.5,0)) < 1e-6);
  ok += (abs(power(-3.5, 1)-pow(-3.5,1)) < 1e-6);
  return (ok == 9);
}

#define NTESTS 3
static const TestCase t1 = {test_poly_eval_1, "test_poly_eval_1"};
static const TestCase t2 = {test_partfact_1, "test_partfact_1"};
static const TestCase t3 = {test_power_1, "test_power_1"};
static const TestCase* test_cases[NTESTS] = {&t1, &t2, &t3};

int main(int argc, char ** argv){
  int result, i, exit_status = 0;
  return run_tests(NTESTS, test_cases, argv[0]);
}
