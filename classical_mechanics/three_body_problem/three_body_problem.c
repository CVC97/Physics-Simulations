#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


// body masses in sun masses
const double m1 = 10e0;
const double m2 = 10e0;
const double m3 = 20e0;
const double G = 4 * cvc_PI * cvc_PI;                                           // gravitation constant
const double smoothing_factor = 10e-1;                                          // avoiding numerical errors while dividing by 0


// integration parameters
const double T_max = 50;
const double delta_t = 10e-5;


// gravitational acceleration forced by mj on mi 
double gravitation(double posi, double posj, double mj, double r) {
    return -G * (posi-posj) * mj / cvc_npow(r, 3);
}


// center of mass calculation
double com(double pos1, double m1, double pos2, double m2, double pos3, double m3) {
    return (pos1 * m1 + pos2 * m2 + pos3 * m3) / (m1 + m2 + m3);
}


// ODE for the sun positions
int ThreeBody_ODE(double t, const double y[], double f[], void *params) {
    // coordinates of the 3 masses (structure of the y-vector)
    double x1 = y[0];
    double y1 = y[1];
    double z1 = y[2];

    double x2 = y[3];
    double y2 = y[4];
    double z2 = y[5];

    double x3 = y[6];
    double y3 = y[7];
    double z3 = y[8];

    // transfer of the velocities from y to f
    for (int i = 0; i < 9; i++) {
        f[i] = y[i+9];
    }

    // calculating the distances between ri und rj
    double r12 = cvc_norm_3D(x1-x2, y1-y2, z1-z2) + smoothing_factor;
    double r23 = cvc_norm_3D(x2-x3, y2-y3, z2-z3) + smoothing_factor;
    double r31 = cvc_norm_3D(x3-x1, y3-y1, z3-z1) + smoothing_factor;

    // calculating the accelerations for given f
    f[9] = gravitation(x1, x2, m2, r12) + gravitation(x1, x3, m3, r31);           // g_x1
    f[10] = gravitation(y1, y2, m2, r12) + gravitation(y1, y3, m3, r31);          // g_y1
    f[11] = gravitation(z1, z2, m2, r12) + gravitation(z1, z3, m3, r31);          // g_z1

    f[12] = gravitation(x2, x3, m3, r23) + gravitation(x2, x1, m1, r12);          // g_x2
    f[13] = gravitation(y2, y3, m3, r23) + gravitation(y2, y1, m1, r12);          // g_y2
    f[14] = gravitation(z2, z3, m3, r23) + gravitation(z2, z1, m1, r12);          // g_z2

    f[15] = gravitation(x3, x1, m1, r31) + gravitation(x3, x2, m2, r23);          // g_x3
    f[16] = gravitation(y3, y1, m1, r31) + gravitation(y3, y2, m2, r23);          // g_y3
    f[17] = gravitation(z3, z1, m1, r31) + gravitation(z3, z2, m2, r23);          // g_z3
    return 0;
}


int main(void) {
    int dimension = 18;
    double t = 0;

    // inititialization of the state arrays
    double y_2D[18] = {
        -4, 0, 0,                       // position m1
        2, -2, 0,                       // position m2
        0, 2, 0,                        // position m3

        1, 0, 0,                        // velocity m1
        -1, 0, 0,                       // velocity m2
        0, 0, 0                         // velocity m3
    };

    double y_3D[18] = {
        -10, 0, 0,                      // position m1
        10, 0, 0,                       // position m2
        0, sqrt(30), 0.001,             // position m3

        1, 0.1, 0,                      // velocity m1
        -1, 0, 0,                       // velocity m2
        0.5, 0, 0                       // velocity m3
    };

    // setting up the files
    FILE* pos_file_2D = fopen("data/ThreeBody_2D_data.csv", "w");
    FILE* pos_file_3D = fopen("data/ThreeBody_3D_data.csv", "w");
    fprintf(pos_file_2D, "t, x1, y1, z1, x2, y2, z2, x3, y3, z3\n");
    fprintf(pos_file_3D, "t, x1, y1, z1, x2, y2, z2, x3, y3, z3\n");

    // center of mass calculation
    double com_2D[3], com_3D[3];
    for (int i = 0; i < 3; i++) {
        com_2D[i] = com(y_2D[i], m1, y_2D[3+i], m2, y_2D[6+i], m3);
        com_3D[i] = com(y_3D[i], m1, y_3D[3+i], m2, y_3D[6+i], m3);
    }

    // adding corrected coordinates to the files
    fprintf(pos_file_2D, "%g", t);
    fprintf(pos_file_3D, "%g", t);
    for (int i = 0; i < 9; i++) {
        fprintf(pos_file_2D, ", %g", y_2D[i]-com_2D[i % 3]);
        fprintf(pos_file_3D, ", %g", y_3D[i]-com_3D[i % 3]);
    }

    fprintf(pos_file_2D, "\n");
    fprintf(pos_file_3D, "\n");

    // iterating through the timesteps until T_max
    while (t < T_max) {
        // applying numerical integration step using verlet
        cvc_verlet_step(t, delta_t, y_2D, ThreeBody_ODE, dimension, NULL);
        cvc_verlet_step(t, delta_t, y_3D, ThreeBody_ODE, dimension, NULL);
        t += delta_t;

        // center of mass calculation
        for (int i = 0; i < 3; i++) {
            com_2D[i] = com(y_2D[i], m1, y_2D[3+i], m2, y_2D[6+i], m3);
            com_3D[i] = com(y_3D[i], m1, y_3D[3+i], m2, y_3D[6+i], m3);
        }

        // adding corrected coordinates to the files
        fprintf(pos_file_2D, "%g", t);
        fprintf(pos_file_3D, "%g", t);
        for (int i = 0; i < 9; i++) {
            fprintf(pos_file_2D, ", %g", y_2D[i]-com_2D[i % 3]);
            fprintf(pos_file_3D, ", %g", y_3D[i]-com_3D[i % 3]);
        }
        fprintf(pos_file_2D, "\n");
        fprintf(pos_file_3D, "\n");
    }
    fclose(pos_file_2D);
    fclose(pos_file_3D);
}