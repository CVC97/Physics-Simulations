#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


typedef int ode_func(double, const double[], double[], void*);


// physical parameters
const double SIGMA = 1;
const double R = 1;
const double B = 1;


// integration parameters
const double T_max = 10000;
const double delta_t = 10e-3;
const int DIMENSION = 3;
const int N_TRAJECTORIES = 3;


// differential equations for the lorenz system
int DE_lorenz_system(double t, const double y[], double f[], void *params) {
    // caching the parameters
    double sigma = ((double*) params)[0];
    double b = ((double*) params)[1];
    double r = ((double*) params)[2];

    for (int i = 0; i < N_TRAJECTORIES; i++) {
        // caching the state of the system
        double x_state = y[3*i + 0];
        double y_state = y[3*i + 1];
        double z_state = y[3*i + 2];

        // calculating the changes of the system
        f[3*i + 0] = sigma * (y_state-x_state);
        f[3*i + 1] = r*x_state - y_state - x_state*z_state;
        f[3*i + 2] = x_state*y_state - b*z_state;
    }
}


int main(void) {
    double t = 0;                                                           // initial time
    double parameters[3] = {10, 3.0/8, 28};                                 // parameters for the lorenz system

    // initial states of each particle
    const int y_dimension = N_TRAJECTORIES * DIMENSION;
    double y[] = {
        2, 1, 1,
        2.1, 1, 1,
        2.2, 1, 1
    };

    // setting up the files and adding initial state
    FILE* state_file = fopen("data/lorenz_data.csv", "w");
    fprintf(state_file, "time");
    for (int i = 1; i < N_TRAJECTORIES + 1; i++) {
        fprintf(state_file, ", x%d, y%d, z%d", i, i, i);
    }
    fprintf(state_file, "\n%g", t);
    for (int i = 0; i < y_dimension; i++) {
        fprintf(state_file, ", %g", y[i]);
    }

    // iteration till 'T_max'
    while (t < T_max) {
        t += delta_t;
        cvc_rk4_step(t, delta_t, y, DE_lorenz_system, y_dimension, parameters);
        fprintf(state_file, "\n%g", t);
        for (int i = 0; i < y_dimension; i++) {
            fprintf(state_file, ", %g", y[i]);
        }
    }
    fclose(state_file);
    return 0;
}