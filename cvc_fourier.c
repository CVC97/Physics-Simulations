#include <complex.h>
#include "cvc_numerics.h"


// discrete fourier transform 
void cvc_dft(double x_array[], double k_array[], int N) {
    for (int k_i = 0; k_i < N; k_i++) {
        double complex k_sum = 0;
        for (int x_i = 0; x_i < N; x_i++) {
            k_sum += x_array[x_i] * cexp(-I*2*cvc_PI*x_i*k_i/N);
        }
        k_array[k_i] = k_sum;
    }
    return;
}


// discrete fast fourier transform
void cvc_fft_radix_2(double x_array[], double k_array[], int N) {

    return;
}