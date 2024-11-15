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

    // calculating the derivation array
    
    return 0;
}


int main(void) {

    return 0;
}