#include <stdio.h>
#include "jfdlibm.h"
#include "fdlibm.h"

int main(void)
{
 int itr = 100000000;
 double t = 0;
 double c;

 for (itr = 0; itr < 10; itr++) {
   c  = jcos(itr);
   t += c;
   printf("cosine of %d is: %f\n", itr, c);
 }

 printf("cosine total sum is: %f\n", t);
}
