#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "../../cvc_numerics.h"


// oscillation parameters
const double OSZ_A0 = 5;
const double OSZ_T = 2000;
const double OSZ_OMEGA = 2 * cvc_PI / OSZ_T;


// ocean parameters
const double OCEAN_HEIGHT = 5000;                               // generel ocean depth
const double OCEAN_HEIGHT_RIFF = 20;                            // riff depth

const double OCEAN_X_LEFT = -1000e3;                            // left ocean border
const double OCEAN_X_RIGHT = 0;                                 // right ocean border
const double OCEAN_X_RIFF_LEFT = -700e3;                        // left riff border
const double OCEAN_X_BEACH_LEFT = -550e3;                       // left beach border
const double OCEAN_X_BEACH_RIGHT = -450e3;                      // right beach border
const double OCEAN_X_RIFF_RIGHT = -300e3;                       // right beach border


// integration parameters
const double T_MAX = 22000;
const double DELTA_X = 1000;
const double DELTA_T = 1;
const int N = (OCEAN_X_RIGHT - OCEAN_X_LEFT) / DELTA_X;


// parameter structure of the d'Alembert integrator
struct params_dAlembert {
    double delta_t;
    double delta_x;
};


// ocean profile
double height_ocean(double x) {
    if (OCEAN_X_LEFT <= x && x < OCEAN_X_RIFF_LEFT) {
        return OCEAN_HEIGHT;
    } else if (OCEAN_X_RIFF_LEFT <= x && x < OCEAN_X_BEACH_LEFT) {
        return OCEAN_HEIGHT + (OCEAN_HEIGHT_RIFF-OCEAN_HEIGHT) * cvc_npow(sin(cvc_PI/2 * (x-OCEAN_X_RIFF_LEFT) / (OCEAN_X_BEACH_LEFT-OCEAN_X_RIFF_LEFT)), 2);
    } else if (OCEAN_X_BEACH_LEFT <= x && x < OCEAN_X_BEACH_RIGHT) {
        return OCEAN_HEIGHT_RIFF;
    } else if (OCEAN_X_BEACH_RIGHT <= x && x < OCEAN_X_RIFF_RIGHT) {
        return OCEAN_HEIGHT_RIFF - (OCEAN_HEIGHT_RIFF-OCEAN_HEIGHT) * cvc_npow(sin(cvc_PI/2 * (OCEAN_X_BEACH_RIGHT-x) / (OCEAN_X_BEACH_RIGHT-OCEAN_X_RIFF_RIGHT)), 2);
    } else if (OCEAN_X_RIFF_RIGHT <= x && x < OCEAN_X_RIGHT) {
        return OCEAN_HEIGHT;
    } else {
        return 0;
    }
}


// free end stimulus
double wave_excitation_A(double t) {
    return OSZ_A0 * sin(OSZ_OMEGA * t);
}


// wave speed for given x
double wave_speed_u(double x) {
    return sqrt(cvc_EARTH_GRAVITATION * height_ocean(x));
}


// Berechnet den Zustand der Welle des nächsten Zeitschrittees
int dAlembertFTCS(double t, double y_old[], double y[], struct params_dAlembert params) {
    double delta_x = params.delta_x;
    double delta_t = params.delta_t;

    // Berechnung des Zustandes für den nächsten Zeitschritt
    double *y_temp = (double*) malloc(N * sizeof(double));
    for(size_t i = 0; i < N; i++) {
        double x = OCEAN_X_LEFT + (i * delta_x);

        // Werte des vorherigen Zeitschrittes für die Berechnung des Nächsten
        double f = y[i % N];
        double f_west = y[(i - 1) % N];
        double f_east = y[(i + 1) % N];
        double f_t_minus = y_old[i % N];

        // Berechnung der Wellengeschwindigkeit für x, x_(i-1) und x_(i+1)
        double u_i = wave_speed_u(x);
        double u_i_minus = wave_speed_u(x - delta_x);
        double u_i_plus = wave_speed_u(x + delta_x);

        // Berechnung des Parameters beta^2 aus den Wellengeschwindigkeiten für x, x_(i-1) und x_(i+1)
        double beta_i_squared = cvc_npow(u_i * delta_t / delta_x, 2);
        double beta_i_minus_squared = cvc_npow(u_i_minus * delta_t / delta_x, 2);
        double beta_i_plus_squared = cvc_npow(u_i_plus * delta_t / delta_x, 2);

        if (beta_i_squared > 1) {
            printf("ERROR! beta^2 exceeds 1, please adjust delta_t (decrease) and / or delta_x (increase) for valid results.\n");
            return 1;
        }

        double f_east_ghost = y[N-1];                                                                    // rechter Ghost
        double f_west_ghost;

        if (0 <= t && t <= 2*cvc_PI/OSZ_OMEGA) {
            f_west_ghost = wave_excitation_A(t);                                                 // linker Ghost
        } else {
            f_west_ghost = 0;
        }

        // double f_west_ghost = wave_excitation_A(t);                                                 // linker Ghost
        

        double delta_f_t = 0; //cvc_diff

        if (i == 0) {
            y_temp[i] = 2*(1-beta_i_squared)*f - f_t_minus + beta_i_squared*(f_east+f_west_ghost) + 1.0/4*(beta_i_plus_squared-beta_i_minus_squared)*(f_east-f_west_ghost);
        } else if (i == N - 1) {
            y_temp[i] = 2*(1-beta_i_squared)*f - f_t_minus + beta_i_squared*(f_east_ghost+f_west) + 1.0/4*(beta_i_plus_squared-beta_i_minus_squared)*(f_east_ghost-f_west);
        } else {
            y_temp[i] = 2*(1-beta_i_squared)*f - f_t_minus + beta_i_squared*(f_east+f_west) + 1.0/4*(beta_i_plus_squared-beta_i_minus_squared)*(f_east-f_west);
        }
    }

    // Übertragen der neuen Werte in das Ursprungsaray
    for(int i = 0; i < N; i++) {
        y_old[i] = y[i];
        y[i] = y_temp[i];
    }

    free(y_temp);
    return 0;
}


int main(void) {

    // ocean initialization
    double *y_wave = (double*) calloc(N, sizeof(double));
    double *y_wave_old = (double*) calloc(N, sizeof(double));
    double x = OCEAN_X_LEFT;                                                                // Laufvariable der Position im Ozean
    double t = 0;                                            

    FILE* ocean_file = fopen("data/tsunami_data.csv", "w");
    fprintf(ocean_file, "0");
    for (int n_x = 0; n_x < N; n_x++) {
        fprintf(ocean_file, ", %g", OCEAN_X_LEFT + n_x * DELTA_X);
    }

    // transfer structure of the d'Alembert integrator
    struct params_dAlembert params_struct;
    while (t < T_MAX) {
        params_struct.delta_t = DELTA_T;
        params_struct.delta_x = DELTA_X;
        dAlembertFTCS(t, y_wave_old, y_wave, params_struct);
        fprintf(ocean_file, "\n%g", t);
        for (int n_x = 0; n_x < N; n_x++) {
            fprintf(ocean_file, ", %g", y_wave[n_x]);
        }
        t += DELTA_T;
    }
    fclose(ocean_file);
    free(y_wave);   
    free(y_wave_old);
    return 0;
}