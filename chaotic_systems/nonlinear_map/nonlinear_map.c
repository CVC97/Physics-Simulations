#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"
#include "../../cvc_fourier.h"


// returns the next map entry x_{n+1} for given x_n
double get_nonliner_next(double x_n, double mu) {
    return mu*x_n * (1-x_n);
}


int main(void) {
    // parameters
    double mu_start = 0;                                                // mu start
    double mu_end = 4;                                                  // mu end
    double delta_mu = 0.005;                                             // mu discretization

    double x_start = 0.6;                                               // initial value for x
    int N = 60;                                                         // maximum number of iterations over the map
    int long_N = 60+1;                                                    // number of long-term values stored and fourier-transformed


    // setting up the files
    FILE* x_file = fopen("data/nonlinear_map_data.csv", "w");
    FILE* long_x_file = fopen("data/nonlinear_map_long_x_data.csv", "w");
    FILE* long_k_file = fopen("data/nonlinear_map_long_k_data.csv", "w");
    fprintf(x_file, "mu");
    fprintf(long_x_file, "mu");
    fprintf(long_k_file, "mu");
    // numerating x_n values in file header
    for (int i = 0; i <= N; i++) {
        fprintf(x_file, ", %d", i);
        // numerating the long-term values of x_n and k_n
        if (long_N-N+i >= 0) {
            fprintf(long_x_file, ", %d", i);
            fprintf(long_k_file, ", %d", i);
        }
    }
    fprintf(x_file, "\n");
    fprintf(long_x_file, "\n");
    fprintf(long_k_file, "\n");


    // iterate through the different growth rates mu
    while (mu_start <= mu_end) {
        double x_0 = x_start;                                           // resetting the initial value for x

        // arrays for long-term (last 30) values x_n and their fourier transformed k_n values
        double x_n[long_N];                                             // real space values
        double k_n[long_N];                                             // fourier space values

        // first two columns
        fprintf(x_file, "%g, %g", mu_start, x_0);
        fprintf(long_x_file, "%g", mu_start);
        fprintf(long_k_file, "%g", mu_start);
        // (potentially) add initial x_n, k_n to array
        if (N < long_N) {
            x_n[0] = x_0;  
        }

        // generating N items
        for (int i = 0; i < N; i++) {
            x_0 = get_nonliner_next(x_0, mu_start);
            fprintf(x_file, ", %g", x_0);

            // adding long-term x_n to the rescpective array
            if (long_N-N+i >= 0) {
                x_n[long_N-N+i] = x_0;
            }
        }
        // fourier transform
        cvc_dft(x_n, k_n, long_N);                                      // generate array of DFT long-term values
        // print values to long-term files
        for (int i = 0; i < long_N; i++) {
            fprintf(long_x_file, ", %g", x_n[i]);
            fprintf(long_k_file, ", %g", k_n[i]);     
        }
        fprintf(long_x_file, "\n");
        fprintf(long_k_file, "\n");
        fprintf(x_file, "\n");                                          // linebreak for next mu
        mu_start += delta_mu;                                           // increment the growth parameter mu                         
    }

}