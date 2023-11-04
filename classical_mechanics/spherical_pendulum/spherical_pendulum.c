#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


typedef int ode_func(double, const double[], double[], void*);


// physical parameters
const double m = 10;


// initial conditions
const double PHI = -cvc_PI*0.6;
const double THETA = -6.5/8*cvc_PI;
const double PHI_DOT = 0.25;
const double THETA_DOT = 0;


// integration parameters
const double T_max = 100;
const double delta_t = 10e-4;
const int dimension = 4;                                                // dimension of the state vector
const double smoothing_factor = 1e-10;


// function describing the pendulums length for a given time 't'
double pendulum_length(double t) {
    return 6 + sin(t / 10);
}


int ODE_spherical_pendulum(double t, const double y[], double f[], void *params) {
    // calculating length and change in length of the pendulum
    double l = pendulum_length(t);
    double l_dot = cvc_diff(t, 0.0001, pendulum_length);

    // state of the spherical pendulum
    double phi = y[0];
    double phi_dot = y[1];
    double theta = y[2];
    double theta_dot = y[3];

    // transfer the velocities of the system
    f[0] = phi_dot;
    f[2] = theta_dot;

    // calculate the accelerations of the system
    f[1] = phi_dot * (2*l_dot/l - cos(theta)*theta_dot/cvc_max(sin(theta), smoothing_factor));
    f[3] = (cvc_EARTH_GRAVITATION*sin(theta) - 2*theta_dot*l_dot) / l + sin(theta)*cos(theta)*cvc_npow(phi_dot, 2);
    return 0;
}


int main(void) {
    double t = 0;                                                           // starting time 't'
    double y[] = {PHI, PHI_DOT, THETA, THETA_DOT};                          // state vector

    // setting up the files and adding initial state
    FILE* angel_file = fopen("data/spherical_pendulum_data.csv", "w");
    fprintf(angel_file, "t, l, phi, phi_dot, theta, theta_dot\n");
    fprintf(angel_file, "%g, %g", t, pendulum_length(t));
    for (int i = 0; i < dimension; i++) {
        fprintf(angel_file, ", %g", y[i]);
    }

    // iterating until 't' reaches 'T_max'
    while (t < T_max) {
        t += delta_t;
        cvc_rk4_step(t, delta_t, y, ODE_spherical_pendulum, dimension, NULL);
        fprintf(angel_file, "\n%g, %g", t, pendulum_length(t));
        for (int i = 0; i < dimension; i++) {
            fprintf(angel_file, ", %g", y[i]);
        }
    }
    fclose(angel_file);
    return 0;
}