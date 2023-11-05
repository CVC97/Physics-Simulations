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
const double T_max = 100;
const double delta_t = 10e-4;
const int dimension = 3;


// differential equations for the lorenz system
int DE_lorenz_system(double t, const double y[], double f[], void *params) {
    // caching the parameters
    double sigma = ((double*) params)[0];
    double r = ((double*) params)[0];
    double b = ((double*) params)[0];

    // caching the state of the system
    double x = y[0];
    double y = y[1];
    double z = y[2];

    // calculating the changes of the system
    f[0] = sigma * (y-x);
    f[1] = r*x - y - x*z
    f[2] = x*y - b*z;
}


int main(void) {

    return 0;
}