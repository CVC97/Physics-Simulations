#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


// physical constants
const int N = 2;                                                                // dimension N
const double mass = 1;                                                          // mass
const double k = 10;                                                            // spring constant k of both springs          
const double r_0 = 1;                                                           // rest length r_0 of both springs
const double r_A[2] = {-1, 0};                                                  // left spring anchoring r_A
const double r_B[2] = {1, 0};                                                   // right spring anchoring r_b

const double smoothing_factor = 1e-12;                                          // avoiding numerical issues for dividing through 0


// ODE of the spring system
int ODE_dual_springs(double t, const double y[], double f[], void *params) {
    // transfering velocities into the derivation array
    f[0] = y[2];
    f[1] = y[3];

    // calculation of the distances between mass and each anchoring
    double dist_r_A = cvc_norm_2D(y[0] - r_A[0], y[1] - r_A[1]) + smoothing_factor;
    double dist_r_B = cvc_norm_2D(y[0] - r_B[0], y[1] - r_B[1]) + smoothing_factor;

    // calculation force absolute
    double f_A = -k * (dist_r_A - r_0);
    double f_B = -k * (dist_r_B - r_0);

    // calculation x- and y-component of each spring
    double f_A_x = f_A * (y[0] - r_A[0]) / dist_r_A;
    double f_A_y = f_A * (y[1] - r_A[1]) / dist_r_A;

    double f_B_x = f_B * (y[0] - r_B[0]) / dist_r_B;
    double f_B_y = f_B * (y[1] - r_B[1]) / dist_r_B;

    // transfer / calculation x- and y-component of the total acting force
    f[2] = (f_A_x + f_B_x) / mass;
    f[3] = (f_A_y + f_B_y) / mass;
    return 0;
}


int main(void) {
    // simulation parameters
    int dimension = 2 * N;                                                      // dimensionality of the state vector
    double T_x = 2 * cvc_PI / sqrt(2*k), T_x_Euler = 0, T_x_RK4 = 0;            // analytical period length
    double t = 0;                                                               // initial time t = 0
    double delta_t = 10e-4;                                                     // size of timestep delta_t

    // initialization of the starting positions
    double y1_rk4[4] = {-0.75, 0.2, 0, -0.2};
    double y2_rk4[4] = {-0.5, -0.5};
    double y3_rk4[4] = {0, -0.3, 1, 1};

    // data file
    FILE* fancy_pos_file = fopen("data/oscillation_sensor.csv", "w"); 
    fprintf(fancy_pos_file, "Zeit, x1(t), y1(t), x2(t), y2(t), x3(t), y3(t)\n");
    fprintf(fancy_pos_file, "%g, %g, %g, %g, %g, %g, %g\n", t, y1_rk4[0], y1_rk4[1], y2_rk4[0], y2_rk4[1], y3_rk4[0], y3_rk4[1]);

    // integration over 10 periods T_x_RK4
    while (t <= 10 * T_x) {
        t += delta_t;
        cvc_rk4_step(t, delta_t, y1_rk4, ODE_dual_springs, dimension, NULL);
        cvc_rk4_step(t, delta_t, y2_rk4, ODE_dual_springs, dimension, NULL);
        cvc_rk4_step(t, delta_t, y3_rk4, ODE_dual_springs, dimension, NULL);
        fprintf(fancy_pos_file, "%g, %g, %g, %g, %g, %g, %g\n", t, y1_rk4[0], y1_rk4[1], y2_rk4[0], y2_rk4[1], y3_rk4[0], y3_rk4[1]);
    }
    fclose(fancy_pos_file);
    return 0;
}