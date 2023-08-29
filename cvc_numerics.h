#ifndef NUMERICS_H
#define NUMERICS_H


// generelle (Natur-)konstanten
#define cvc_PI 3.14159265358979323846
#define cvc_EARTH_GRAVITATION 9.81

// Zeitparameter
#define cvc_MINUTE 60
#define cvc_HOUR 60 * cvc_MINUTE
#define cvc_DAY 24 * cvc_HOUR
#define cvc_WEEK 7 * cvc_DAY


// Struktur von 2er / 3er Tupeln
struct cvc_tuple_2 {
    double x1;
    double x2;
};

struct cvc_tuple_3 {
    double x1;
    double x2;
    double x3;
};


// Typ gewöhnliche DGL
typedef int cvc_ode_func(double, const double[], double[], void*);


// Potenz für natürliche Zahlen x^n
double cvc_npow(double x, int n);

// Fakultät einer natürlichen Zahl N_0
double cvc_factorial(int n);

// Norm in 2 / 3 dimensions
double cvc_norm_2D(double x, double y);
double cvc_norm_3D(double x, double y, double z);
double cvc_norm_ND(double v[], int N);

// Vektor-Produkt (in 3D)
double* cvc_vector_product(const double a[], const double b[]);


// Numerical Integration
double cvc_integrate(double x, int N);
double cvc_integrate_trapez(double left, double right, int N, double integrand(double));
double cvc_integrate_simpson(double func(double), double x, int N);
double cvc_integrate_simpson_2_param(double left, double right, double dx, double func(double, void*), void *params);

// Numerical Differentiation
double diff(double x, double delta, double func(double));

// Implementations of the error function 
double cvc_erf_simpson(double x, double delta_x);
double cvc_erf_midpoint(double x, double delta_x);


// Find root of given function func with respective parameters
double cvc_find_root_bisection(double func(double), double a, double b, double epsilon, int max_iter);
double cvc_find_root_newton_raphson(double func(double), double x0, double delta, double rel_tol, int max_iter);

// Solver of quadratic equations
struct cvc_tuple_2 cvc_solve_quadratic(double a, double b, double c);


// 2-Dimensional Integration: Midpoint
double cvc_integrate_midpoint_2D(int A(double, double), double a_x, double b_x, double a_y, double b_y, double delta_x, double f(double, double));

// Numerical Integration using Euler / Runke-Kutta / Verlet methods with state array y and given parameters
void cvc_euler_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params);
void cvc_rk2_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params);
void cvc_rk4_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params);
void cvc_verlet_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params);


#endif