#include <stdio.h>
#include "jfdlibm.h"
#include "fdlibm.h"

int main(void)
{
 int itr = 100000000;
 double c;

 for (itr = 0; itr < 100000000; ++itr)
   c += jcos(itr);

 printf("cosine total sum is: %.11f\n", c);
}
