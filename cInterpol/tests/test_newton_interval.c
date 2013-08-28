#include <stdio.h>
#include "../newton_interval.h"
#include "unittest.h"

int test1(){
  double t[] = {0.0,1.0,2.0,3.0};
  double ti = 0.5;
  int i=-1;
  i=(int)get_interval(t,4,ti);
  return (i == 0);
}

int test2(){
  double t[] = {0.0,1.0};
  double ti = 0.5;
  int i=-1;
  i=(int)get_interval(t,2,ti);
  return (i == 0);
}

int test3(){
  double t[] = {0.0,1.0,2.0};
  double ti = 0.9;
  int i=-1;
  i=(int)get_interval(t,3,ti);
  return (i == 0);
}

int test4(){
  double t[] = {0.0,1.0,2.0};
  double ti = -0.9;
  int i=-2;
  i=(int)get_interval(t,3,ti);
  return (i == -1);
}


#define NTESTS 4
static const TestCase t1 = {test1, "test1"};
static const TestCase t2 = {test2, "test2"};
static const TestCase t3 = {test3, "test3"};
static const TestCase t4 = {test4, "test4"};
static const TestCase* test_cases[NTESTS] = {&t1, &t2, &t3, &t4};

int main(int argc, char ** argv){
  int result, i, exit_status = 0;
  return run_tests(NTESTS, test_cases, argv[0]);
}
