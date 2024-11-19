#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"



typedef int ode_func(double, const double[], double[], void*);


// ODE for the driven and damped pendulum with state vector y = {theta, theta_v}
int ODE_driven_damped_pendulum(double t, const double y[], double f[], void *params) {
    // physical parameters from the params array
    double A = ((double*) params)[0];                                   // amplitude A of the external drive
    double omega = ((double*) params)[1];                               // circular frequency w of the external drive
    double gamma = ((double*) params)[2];                               // friction constant gamma of the system

    // current state of the system
    double theta = y[0];                                                // angle
    double theta_v = y[1];                                              // angular velocity

    // calculating the derivation array
    f[0] = theta_v;                                                     // writing angular velocity into derivation array
    f[1] = A*cos(omega*t) - gamma*theta_v - sin(theta);                 // calculating angular acceleration and writing it into derivation array
    return 0;
}


int main(void) {
    // physical parameters
    double A = 1;                                                     // VARIATION of A in [0.1, 2]
    double omega = 0.5;                                                 // VARIATION of omega in [0.2, 1]
    double gamma = 0.2;                                                 // gamma consistent across parameter variation
    double params[3] = {A, omega, gamma};                               // parameter array

    // algorithm control parameters
    double delta_t = 1e-2;                                              // timestep
    double t = 0;                                                       // starting time
    double T_max = 1000;                                                  // end time

    // setting up the state array
    int dimension = 2;                                                  // dimension of the state array
    double theta = 0;                                                   // initial angle
    double theta_v = 0;                                                 // initial angular velocity
    double y[2] = {theta, theta_v};                                     // state array


    // setting up the file
    char filepath_buffer[60];
    char *filepath_start = "data/driven_damped_pendulum";
    char *filepath_end = "data.csv";
    snprintf(filepath_buffer, 60, "%s_%0.1g_%0.1g_%s", filepath_start, A, omega, filepath_end);
    printf("FILEPATH: %s\n", filepath_buffer);

    FILE* angel_file = fopen(filepath_buffer, "w");
    fprintf(angel_file, "t, theta, theta_v\n");
    fprintf(angel_file, "%g, %g, %g\n", t, y[0], y[1]);


    // iterating until end time is reached
    while (t < T_max) {
        t += delta_t;
        cvc_rk4_step(t, delta_t, y, ODE_driven_damped_pendulum, dimension, params);
        fprintf(angel_file, "%g, %g, %g\n", t, y[0], y[1]);
    }
    fclose(angel_file);
    return 0;
}