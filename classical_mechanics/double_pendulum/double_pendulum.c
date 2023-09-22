#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


typedef int ode_func(double, const double[], double[], void*);


// physical parameters
const double m1 = 1;                                              // mass for the upper pendulum
const double m2 = 1;                                              // mass for the lower pendulum
const double L = 1;                                               // lenght 'L' between origin and mass1 as well as between mass1 and mass2


// initial conditions
const double THETA1 = 3.0 / 8 * cvc_PI;
const double THETA2 = 0;


// integration parameters
const double T_max = 10;
const double delta_t = 10e-5;
const int dimension = 6;                                    // dimension of the state vector


// writes analytical solution for given t and paramters *params in state vector y
int double_pendulum_analytical(double t, double y[], void *params) {
    // caching the parameters from *params
    double C1 = ((double*) params)[0];
    double C2 = ((double*) params)[1];
    double omega1 = ((double*) params)[2];
    double omega2 = ((double*) params)[3];
    double my = ((double*) params)[4];
    double phi1 = 0;
    double phi2 = 0;

    // calculating the state of the double pendulum for given t
    y[0] = C1 * cos(omega1*t + phi1) + C2 * cos(omega2*t + phi2);
    y[3] = -C1 * sqrt((1+my) / my) * cos(omega1*t + phi1) + C2 * sqrt((1+my) / my) * cos(omega2*t + phi2);
    return 0;
}


// ODE for the double pendulum with structure of state vector y = [theta1, theta1_v, theta1_a, theta2, theta2_v, theta2_a]
int ODE_double_pendulum(double t, const double y[], double f[], void *params) {
    // state of the double pendulum
    double theta1 = y[0];                                   // angel of mass1
    double theta1_v = y[1];                                 // angular velocity of mass1
    double theta1_a = y[2];                                 // angular acceleration of mass1
    double theta2 = y[3];                                   // angel of mass2
    double theta2_v = y[4];                                 // angular velocity of mass2
    double theta2_a = y[5];                                 // angular acceleration of mass2

    f[0] = theta1_v;                                        // transfering theta1_v to f array
    f[3] = theta2_v;                                        // transfering theta2_v to f_array

    // calculating the new accelerations for both masses
    f[1] = - m2 / (m1 + m2) * (theta2_a * cos(theta1-theta2) + cvc_npow(theta2_v, 2) * sin(theta1-theta2)) - cvc_EARTH_GRAVITATION / L * sin(theta1);
    f[4] = - (theta1_a * cos(theta1-theta2) + cvc_npow(theta1_v, 2) * sin(theta1-theta2)) - cvc_EARTH_GRAVITATION / L * sin(theta2);
    return 0; 
}


int main(void) {
    double t = 0;                                                       // time variable 't' running until 'T_max'
    double y_numerical[] = {THETA1, THETA2, 0, 0, 0, 0};                // numerical state vector
    double y_analytical[] = {THETA1, THETA2, 0, 0, 0, 0};               // analytical state vector 

    // determining intial values C1, C2, omega1, and omega2 from the initial state
    double my = m2 / m1;
    double my_bar = sqrt((1+my) / my);
    double omega1 = cvc_EARTH_GRAVITATION / L * (1 + my + sqrt((1+my) * my));
    double omega2 = cvc_EARTH_GRAVITATION / L * (1 + my - sqrt((1+my) * my));
    double C1 = THETA1 / 2 - THETA2 / (2*my_bar);
    double C2 = THETA1 / 2 + THETA2 / (2*my_bar);
    double params[] = {C1, C2, omega1, omega2, my};

    // setting up the files and adding initial state
    FILE* angel_numerical_file = fopen("data/double_pendulum_numerical_data.csv", "w");
    FILE* angel_analytical_file = fopen("data/double_pendulum_analytical_data.csv", "w");
    fprintf(angel_numerical_file, "t, theta1, theta1_v, theta1_a, theta2, theta2_v, theta2_a\n");
    fprintf(angel_analytical_file, "t, theta1, theta1_v, theta1_a, theta2, theta2_v, theta2_a\n");
    fprintf(angel_numerical_file, "%g", t);
    fprintf(angel_analytical_file, "%g", t);
    for (int i = 0; i < 6; i++) {
        fprintf(angel_numerical_file, ", %g", y_numerical[i]);
        fprintf(angel_analytical_file, ", %g", y_analytical[i]);
    }

    // iterating until 't' reaches 'T_max'
    while (t < T_max) {
        t += delta_t;
        cvc_rk4_step(t, delta_t, y_numerical, ODE_double_pendulum, dimension, NULL);
        double_pendulum_analytical(t, y_analytical, params);
        fprintf(angel_numerical_file, "%g", t);
        for (int i = 0; i < dimension; i++) {
            fprintf(angel_numerical_file, ", %g", y_numerical[i]);
            fprintf(angel_analytical_file, ", %g", y_analytical[i]);
        }
    }
    fclose(angel_numerical_file);
    fclose(angel_analytical_file);
    return 0;
}