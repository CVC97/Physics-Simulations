#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


const double L = 1;                                                 // domain length
const double delta_x = 0.0035;                                      // domain discretization
const double D = 0.1;                                               // diffusity
const double T_LINKS = 1;                                           // Direchlet-Boundary-Condition left: T = 1
const double T_RECHTS = -1;                                         // Direchlet-Boundary-Condition right: T = -1
const int N = L / delta_x;                                          // number of discretization steps


int heat_FTCS(double t, double y[], double dt) {
    double *y_temp = (double*) malloc(N * sizeof(double));
    for(size_t i = 0; i < N; i++) {
        double T = y[i % N];
        double TW = y[(i - 1) % N];
        double TO = y[(i + 1) % N];

        if (i == 0) {
            y_temp[i] = y[i] + dt * D * (T_LINKS - 2*T + TO) / cvc_npow(delta_x, 2);
        } else if (i == N - 1) {
            y_temp[i] = y[i] + dt * D * (TW - 2*T + T_RECHTS) / cvc_npow(delta_x, 2);
        } else {
            y_temp[i] = y[i] + dt * D * (TW - 2*T + TO) / cvc_npow(delta_x, 2);
        }
    }

    // transfering new values into original array
    for(int i = 0; i < N; i++) {
        y[i] = y_temp[i];
    }

    free(y_temp);
    return 0;
}


int main(void) {
    // time parameters
    double time = 0;
    double time_max = 1;
    double delta_time = cvc_npow(delta_x, 2) / (2.1 * D);         
    printf("delta_time: %g\n", delta_time);
    double *y = (double*) calloc(N, sizeof(double));                // initializing heat field

    // file initialization
    FILE* heat_file = fopen("data/heat_equation_data.csv", "w");
    fprintf(heat_file, "0");
    for (int i = 0; i < N; i++) {
        fprintf(heat_file, ", %g", (i+1) * delta_x);
    }
    fprintf(heat_file, "\n%g", time);
    for (int i = 0; i < N; i++) {
        fprintf(heat_file, ", %g", y[i]);
    }

    // iterating through timesteps till time_max
    while (time < time_max) {
        heat_FTCS(time, y, delta_time);
        time += delta_time;

        // generating heat file
        fprintf(heat_file, "\n%g", time);
        for (int i = 0; i < N; i++) {
            fprintf(heat_file, ", %g", y[i]);
        }
    }
    free(y);
    fclose(heat_file);
    return 0;
}
