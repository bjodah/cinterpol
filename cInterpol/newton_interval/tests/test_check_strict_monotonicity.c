#include "newton_interval.h"
#include "unittest.h"

#include <stdio.h>

int test1(){
    double arr[] = {0.0, 1.0, 2.0};
    int n = 3;
    int i = check_strict_monotonicity(arr, n);
    return (i == 1);
}

int test2(){
    double arr[] = {0.0, 1.0};
    int n = 2;
    int i = check_strict_monotonicity(arr, n);
    return (i == 1);
}

int test3(){
    double arr[] = {0.0};
    int n = 1;
    int i = check_strict_monotonicity(arr, n);
    return (i == 1);
}

int test4(){
    double arr[] = {0.0, 1.0, 0.5};
    int n = 3;
    int i = check_strict_monotonicity(arr, n);
    return (i == 0);
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
