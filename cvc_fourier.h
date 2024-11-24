#ifndef FOURIER_H
#define FOURIER_H

#include "cvc_numerics.h"


// discrete fouriert transform
int cvc_dft(double x[], double k[], int N);

// discrete fast fourier transform
int cvc_fft_radix_2(double x[], double k[], int N);


#endif