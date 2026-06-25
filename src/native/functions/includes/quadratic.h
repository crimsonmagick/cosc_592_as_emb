
#ifndef COSC_592_AS_EM_QUADRATIC_H
#define COSC_592_AS_EM_QUADRATIC_H

struct ComplexNumber {
  double realPart;
  double imaginaryPart;
};

void findQuadraticRoots(double a, double b, double c, struct ComplexNumber *roots);

#endif