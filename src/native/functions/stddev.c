#include <math.h>

double stddev(double *values, int n) {
  double mean = 0.0;

  for (int i = 0; i < n; i++)
    mean += values[i];

  mean /= n;

  double variance = 0.0;

  for (int i = 0; i < n; i++) {
    double diff = values[i] - mean;
    variance += diff * diff;
  }

  return sqrt(variance / n);
}
