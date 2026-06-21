#include <stdio.h>
#include "prime.h"

int main(void) {
  const int toTest = 5;
  const int testResult = isPrime(toTest);
  printf("Is %d prime? Answer: %d\n", toTest, testResult);
  return 0;
}