#include "../newton_interval.h"
#include <stdio.h>
#include <assert.h>

void test1(){
  double t[] = {0.0,1.0,2.0,3.0};
  double ti = 0.5;
  int i=-1;
  i=(int)get_interval(t,4,ti);
  assert(i == 0);
}

void test2(){
  double t[] = {0.0,1.0};
  double ti = 0.5;
  int i=-1;
  i=(int)get_interval(t,2,ti);
  assert(i == 0);
}


void main(){
  test1();
  test2();
}
