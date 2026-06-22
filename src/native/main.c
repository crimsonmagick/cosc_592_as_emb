#include <stdio.h>
#include "math/simple/prime.h"
#include "math/complex/quadratic.h"

int main(void) {
  const int toTest = 5;
  const int testResult = isPrime(toTest);
  printf("Is %d prime? Answer: %d\n", toTest, testResult);
  struct ComplexNumber roots[2];
  const int a = 1;
  const int b = 2;
  const int c = 5;
  printf("Coefficients a=%d, b=%d, c=%d\n", a, b, c);
  findQuadraticRoots(1, 2, 5, roots);
  printf("Roots: root1.realPart=%f, root1.imaginaryPart=%f, "
         "root2.realPart=%f, root2.imaginaryPart=%f",
         roots[0].realPart, roots[0].imaginaryPart, roots[1].realPart, roots[1].imaginaryPart);

  return 0;
}
