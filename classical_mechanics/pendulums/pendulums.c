#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


typedef int ode_func(double, const double[], double[], void*);


// physical parameters
const int N = 10;                                                               // number of pendulums 
const double k = 200;                                                           // spring constant
const double base_length = 1;                                                   // base length of each spring
const double mass = 1;                                                          // mass of each pendulum

// simulation parameters
const double T_max = 20.0;
const double delta_t = 1e-3;                                                    // Zeitliche Schrittweite


// solving the ODE
int pendumlumsODE(double t, const double y[], double f[], void *params) {
    // transfering velovities from the state array
    for (int i = 0; i < N; i++) {                   
        f[i] = y[N+i];
    }

    // calculating accelerations from the state array
    f[N] = -k*y[0] / mass;                                                      // position 0 generell
    if (N != 1) {
        f[N] += k*(y[1] - y[0] - base_length);                                  // position 1 to position 0 for more than 1 pendulum
        f[2*N-1] += -k*(y[N-1] - y[N-2] - base_length) / mass;                  // position N - 1 (for more than 1 pendulum)
    }
    for (int i = 1; i < N - 1; i++) {                                           // positions 1 till N - 2
        f[N+i] += -k*(y[i] - y[i-1] - base_length) / mass + k*(y[i+1] - y[i] - base_length) / mass; 
    }
    return 0;
}


// energy calculation
double pendulums_energy(const double y[]) {
    double E_pot = 0;
    double E_kin = 0;

    // calculating kinetic energy
    for (int i = 0; i < N; i++) {
        E_kin += mass / 2 * cvc_npow(y[N+i], 2);
    }

    // potentiel energy
    E_pot += k / 2 * cvc_npow(y[0], 2);  
    if (N != 1) {
        E_pot += k / 2 * cvc_npow(y[1] - y[0] - base_length, 2);
        E_pot += k / 2 * cvc_npow(y[N-1] - y[N-2] - base_length, 2);                                     
    }
    for (int i = 1; i < N - 1; i++) {                          
        E_pot += k / 2 * cvc_npow(y[i] - y[i-1] - base_length, 2) + k / 2 * cvc_npow(y[i+1] - y[i] - base_length, 2); 
    }
    return E_kin + E_pot;
}


int main(void) {
    int dimension = 2*N;
    double t = 0;

    // creating state arrays
    double y_euler[dimension], y_rk2[dimension], y_rk4[dimension], y_verlet[dimension], energy;
    for (int i = 0; i < N; i++) {
        y_euler[i] = i;
        y_rk2[i] = i;
        y_rk4[i] = i;
        y_verlet[i] = i;
    }

    for (int i = N; i < 2*N; i++) {                                             // zeroes for the acceleration
        y_euler[i] = 0;
        y_rk2[i] = 0;  
        y_rk4[i] = 0;  
        y_verlet[i] = 0;                     
    }
    y_euler[N] = 20;
    y_rk2[N] = 20;
    y_rk4[N] = 20;
    y_verlet[N] = 20;

    // output data
    FILE* pos_euler_file = fopen("data/pendulums_euler_data.csv", "w");
    FILE* pos_rk2_file = fopen("data/pendulums_rk2_data.csv", "w");
    FILE* pos_rk4_file = fopen("data/pendulums_rk4_data.csv", "w");
    FILE* pos_verlet_file = fopen("data/pendulums_verlet_data.csv", "w");

    fprintf(pos_euler_file, "Zeit t, Pendel");
    fprintf(pos_rk2_file, "Zeit t, Pendel");
    fprintf(pos_rk4_file, "Zeit t, Pendel");
    fprintf(pos_verlet_file, "Zeit t, Pendel");

    FILE* energy_file = fopen("data/verlet_energy_data.csv", "w");
    fprintf(energy_file, "Zeit t, Pendel");

    for (int i = 1; i < N; i++) {
        fprintf(pos_euler_file, ", P%d", i);
        fprintf(pos_rk2_file, ", P%d", i);
        fprintf(pos_rk4_file, ", P%d", i);
        fprintf(pos_verlet_file, ", P%d", i);

        fprintf(energy_file, ", P%d", i);
    }
    fprintf(pos_euler_file, "\n");
    fprintf(pos_rk2_file, "\n");
    fprintf(pos_rk4_file, "\n");
    fprintf(pos_verlet_file, "\n");

    fprintf(energy_file, "\n");


    // writing timestep 0 into data files
    fprintf(pos_euler_file, "%g", t);
    fprintf(pos_rk2_file, "%g", t);
    fprintf(pos_rk4_file, "%g", t);
    fprintf(pos_verlet_file, "%g", t);

    fprintf(energy_file, "%g, %g\n", t, energy);
    for (int i = 0; i < N; i++) {
        fprintf(pos_euler_file, ", %g", y_euler[i]);
        fprintf(pos_rk2_file, ", %g", y_rk2[i]);
        fprintf(pos_rk4_file, ", %g", y_rk4[i]);
        fprintf(pos_verlet_file, ", %g", y_verlet[i]);
    }
    fprintf(pos_euler_file, "\n"); 
    fprintf(pos_rk2_file, "\n"); 
    fprintf(pos_rk4_file, "\n"); 
    fprintf(pos_verlet_file, "\n"); 


    // iteration till T_max
    while (t < T_max) {
        t += delta_t;

        cvc_euler_step(t, delta_t, y_euler, pendumlumsODE, dimension, NULL); 
        cvc_rk2_step(t, delta_t, y_rk2, pendumlumsODE, dimension, NULL); 
        cvc_rk4_step(t, delta_t, y_rk4, pendumlumsODE, dimension, NULL); 
        cvc_verlet_step(t, delta_t, y_verlet, pendumlumsODE, dimension, NULL);  // Aufruf der Integrationsfunktion
        energy = pendulums_energy( (const double*) y_verlet);                   // Berechnung der GEsamtenergie des Systems

        // writing onto dataa files
        fprintf(pos_euler_file, "%g", t);
        fprintf(pos_rk2_file, "%g", t);
        fprintf(pos_rk4_file, "%g", t);
        fprintf(pos_verlet_file, "%g", t);

        fprintf(energy_file, "%g, %g\n", t, energy);
        for (int i = 0; i < N; i++) {
            fprintf(pos_euler_file, ", %g", y_euler[i]);
            fprintf(pos_rk2_file, ", %g", y_rk2[i]);
            fprintf(pos_rk4_file, ", %g", y_rk4[i]);
            fprintf(pos_verlet_file, ", %g", y_verlet[i]);
        }
        fprintf(pos_euler_file, "\n"); 
        fprintf(pos_rk2_file, "\n"); 
        fprintf(pos_rk4_file, "\n"); 
        fprintf(pos_verlet_file, "\n"); 
    }
    fclose(pos_euler_file);
    fclose(pos_rk2_file);
    fclose(pos_rk4_file);
    fclose(pos_verlet_file);

    fclose(energy_file);
    return 0;
}