#include "quadratic.h"

#include <math.h>

void findQuadraticRoots(const double a, const double b, const double c, struct ComplexNumber *roots) {
  roots[0].imaginaryPart = roots[1].imaginaryPart = 0;

  const double discriminant = b * b - 4 * a * c;
  if (discriminant > 0) {
    roots[0].realPart = (-b + sqrt(discriminant)) / (2 * a);
    roots[1].realPart = (-b - sqrt(discriminant)) / (2 * a);
  } else if (discriminant == 0) {
    roots[0].realPart = roots[1].realPart = -b / (2 * a);
  } else {
    roots[0].realPart = roots[1].realPart = -b / (2 * a);
    roots[0].imaginaryPart = roots[1].imaginaryPart = sqrt(-discriminant) / (2 * a);
    roots[1].imaginaryPart *= -1;
  }
}
