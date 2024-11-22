#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


// returns the next map entry x_{n+1} for given x_n
double get_nonliner_next(double x_n, double mu) {
    return mu*x_n * (1-x_n);
}


int main(void) {
    // parameters
    double mu_start = 2;                                                // mu start
    double mu_end = 4;                                                  // mu end
    double delta_mu = 0.01;                                             // mu discretization

    double x_start = 0.6;                                               // initial value for x
    int N = 60;                                                         // maximum number of iterations over the map


    // setting up the file
    FILE* x_file = fopen("data/nonlinear_map_data.csv", "w");
    fprintf(x_file, "mu");
    for (int i = 0; i <= 60; i++) {
        fprintf(x_file, ", %d", i);
    }
    fprintf(x_file, "\n");


    // iterate through the different growth rates mu
    while (mu_start <= mu_end) {
        double x_0 = x_start;                                           // resetting the initial value for x

        // generating N items
        for (int i = 0; i <= N; i++) {
            
        }


        mu_start += delta_mu;                                           // increment the growth parameter mu                         
    }

}