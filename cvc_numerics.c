#include <stdlib.h>
#include <tgmath.h>


#define cvc_PI 3.14159265358979323846


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
double cvc_npow(double x, int n) {
    double prod = x;
    for (int i = 1; i < n; i++) {
        prod *= x;
    }
    return prod;
}


// Fakultät einer natürlichen Zahl N_0
double cvc_factorial(int n) {
    int fact = 1;
    for (int i = 2; i <= n; i++) {
        fact *= i;
    }
    return fact;
}


// e^(-y^2)
static double cvc_e_y2(double y) {
    return 2 * exp(-cvc_npow(y, 2)) / sqrt(cvc_PI);
}


// minimum / maximum of the absolute of two numbers
double cvc_min(double a, double b) {
    if (fabs(b) < fabs(a)) {
        return b;
    } else {
        return a;
    }
}

double cvc_max(double a, double b) {
    if (fabs(b) > fabs(a)) {
        return b;
    } else {
        return a;
    }
}


// Norm in 2 / 3 / N dimensions
double cvc_norm_2D(double x, double y) {
    return sqrt(cvc_npow(x, 2) + cvc_npow(y, 2));
}

double cvc_norm_3D(double x, double y, double z) {
    return sqrt(cvc_npow(x, 2) + cvc_npow(y, 2) + cvc_npow(z, 2));
}

double cvc_norm_ND(double v[], int N) {
    double sum = 0;
    for (int v_i = 0; v_i < N; v_i++) {
        sum += cvc_npow(v[v_i], 2);
    }
    return sqrt(sum);
}


// Vektor-Produkt (in 3D)
double *cvc_vector_product(const double a[], const double b[]) {
    double *target = (double*) malloc(3 * sizeof(double));
    target[0] = a[1] * b[2] - a[2] * b[1];
    target[1] = a[2] * b[0] - a[0] * b[2];
    target[2] = a[0] * b[1] - a[1] * b[0];
    return target;
}


// numerische Integration (Trapez)
double cvc_integrate_trapez(double left, double right, int N, double integrand(double)) {
    double sum = 0, interval = (right - left) / N;
    for (int i = 0; i < N; i++) {
        sum += (integrand(left + i*interval) + integrand(left + (i+1)*interval)) * interval / 2;
    }
    return sum;
}


// numerische Integration: Simpsonregel
double cvc_integrate_simpson(double func(double), double x, int N) {
    double delta_x = x / N, sum = 0, x_i, m_i, x_ii;
    for (int i = 0; i < N; i++) {
        x_i = delta_x * i;
        m_i = delta_x * (i+0.5);
        x_ii = delta_x * (i+1);
        sum += (func(x_i) + 4*func(m_i) + func(x_ii)) * delta_x / 6;
    }
    return sum;
}


// numerische Integration: Simpsonregel mit Funktion func für Integralgrenzen (left, right), Schrittweite dx und Parameter *params
double cvc_integrate_simpson_2_param(double left, double right, double dx, double func(double, void*), void *params) {
    double x_i = left, m_i, x_ii, sum = 0;
    while (x_i < right) {
        m_i = x_i + 0.5*dx;
        x_ii = x_i + dx;
        sum += (func(x_i, params) + 4*func(m_i, params) + func(x_ii, params)) * dx / 6;
        x_i += dx;
    }
    return sum;
}


// numerische Integration Fehlerfunktion: Mittelpunktsregel
double cvc_erf_midpoint(double x, double delta_x) {
    int N = fabs(x) / delta_x;
    double sum = 0, d_x = x / N;
    for (int i = 0; i < N; i++) {
        sum += cvc_e_y2( (i+0.5)*d_x ) * d_x;
    }
    return sum;
}


// numerische Integration Fehlerfunktion: Simpsonregel
double cvc_erf_simpson(double x, double delta_x) {
    int N = fabs(x) / delta_x;
    double sum = 0, d_x = x / N, x_i, m_i, x_ii;
    for (int i = 0; i < N; i++) {
        x_i = d_x * i;
        m_i = d_x * (i+0.5);
        x_ii = d_x * (i+1);
        sum += (cvc_e_y2(x_i) + 4*cvc_e_y2(m_i) + cvc_e_y2(x_ii)) * d_x / 6;
    }
    return sum;
}


// numerische Differenzierung: zentrale Differenz
double cvc_diff(double x, double delta, double func(double)) {
    return ( func(x + delta) - func(x - delta) ) / ( 2 * delta);
}


// Nullstellensuche: Bisektion
double cvc_find_root_bisection(double func(double), double a, double b, double epsilon, int max_iter) {
    double x_mid, f_x_mid, f_a, f_b;
    int i = 0;
    while (i++ < max_iter) {
        x_mid = (a + b) / 2;
        f_x_mid = func(x_mid);
        f_a = func(a);
        f_b = func(b);
        if (f_x_mid * f_b < 0) {
            a = x_mid;
        } else if (f_x_mid * f_a < 0) {
            b = x_mid;
        }
        if (f_a < epsilon && f_b < epsilon) {
            break;
        }
    }
    return x_mid;
}


// numerische Nullstellensuche: Newton-Raphson
double cvc_find_root_newton_raphson(double func(double), double x0, double delta, double rel_tol, int max_iter) {
    int i = 0;
    double x_old;
    while (i++ < max_iter) {
        x_old = x0;
        x0 -= func(x0) / cvc_diff(x0, delta, func);
        if (fabs(x_old - x0) / fabs(x0) < rel_tol) {
            break;
        }
    }
    return x0;
}


// kombinierte Lösungsmethode quadratischer Gleichungen
struct cvc_tuple_2 cvc_solve_quadratic(double a, double b, double c) {
    double sol1, sol2;
    if (b > 0) {
        sol1 = (2*c) / (-b - sqrt(pow(b, 2) - 4*a*c));
        sol2 = (-b - sqrt(pow(b, 2) - 4*a*c)) / (2*a);
    } else {
        sol1 = (-b + sqrt(pow(b, 2) - 4*a*c)) / (2*a);
        sol2 = (2*c) / (-b + sqrt(pow(b, 2) - 4*a*c));
    }
    struct cvc_tuple_2 quadratic_solution;
    quadratic_solution.x1 = sol1;
    quadratic_solution.x2 = sol2;
    return quadratic_solution;
}


// 2-Dimensionale Integration: Mittelpunktsregel
double cvc_integrate_midpoint_2D(int A(double, double), double a_x, double b_x, double a_y, double b_y, double delta_x, double f(double, double)) {
    int N_x = (b_x - a_x) / delta_x;
    int N_y = (b_y - a_y) / delta_x;
    double x, y, sum = 0;
    for (int i_x = 0; i_x < N_x; i_x++) {
        for (int i_y = 0; i_y < N_y; i_y++) {
            x = a_x + (i_x + 0.5) * delta_x;
            y = a_y + (i_y + 0.5) * delta_x;
            sum += f(x, y) * A(x, y);
        }
    }
    return pow(delta_x, 2) * sum;
}



// numerische Euler Integration des Zustandsarrays y mit gegebenen Parametern
void cvc_euler_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params) {
    double *f = (double*) calloc(dimension, sizeof(double));    // Reservierung des Ableitungsarrays
    func(t, y, f, params);                                      // Füllen des Ableitungsarrays über Aufruf der entprechenden ODE
    for (int i = 0; i < dimension; i++) {
        y[i] += f[i] * delta_t;
    }
    free(f);                                                    // Freigeben des Ableitungsarrays
    return;
}


// numerische Integration mittels Runge-Kutta 2. Ordnung des Zustandsarrays y mit gegebenen Parametern
void cvc_rk2_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params) {
    double *support = (double*) calloc(dimension, sizeof(double));
    double *k1 = (double*) calloc(dimension, sizeof(double));
    double *k2 = (double*) calloc(dimension, sizeof(double));
    func(t, y, k1, params);                                     // Berechnung k1 = f(t, y)
    for (int i = 0; i < dimension; i++) {
        k1[i] *= delta_t;                                       // Berücksichtigung des Zeitschritts: k1 = f(t, y) * dt
        support[i] = y[i] + k1[i] / 2;                          // support = y + k1/2 (für nächsten Schritt)
    }
    func(t+delta_t/2, support, k2, params);                     // Berechnung k2 = f(t+dt/2, y+k1/2) und y_(i+1)
    for (int i = 0; i < dimension; i++) {
        k2[i] *= delta_t;
        y[i] += k2[i];
    }
    free(support), free(k1), free(k2);
    return;
}


// numerische Integration mittels Runge-Kutta 4. Ordnung des Zustandsarrays y mit gegebenen Parametern
void cvc_rk4_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params) {
    double *support = (double*) malloc(sizeof(double) * dimension);
    double *k1 = (double*) calloc(dimension, sizeof(double));
    double *k2 = (double*) calloc(dimension, sizeof(double));
    double *k3 = (double*) calloc(dimension, sizeof(double));
    double *k4 = (double*) calloc(dimension, sizeof(double));
    func(t, y, k1, params);                                     // Berechnung k1 = f(t, y) * dt und support = y + k1/2
    for (int i = 0; i < dimension; i++) {
        k1[i] *= delta_t;
        support[i] = y[i] + k1[i] / 2;
    }
    func(t+delta_t/2, support, k2, params);                     // Berechnung k2 = f(t+dt/2, y+k1/2) * dt und support = y + k2/2
    for (int i = 0; i < dimension; i++) {
        k2[i] *= delta_t;
        support[i] = y[i] + k2[i] / 2;
    }
    func(t+delta_t/2, support, k3, params);                     // Berechnung k3 = f(t+dt/2, y+k2/2) * dt und support = y + k3
    for (int i = 0; i < dimension; i++) {
        k3[i] *= delta_t;
        support[i] = y[i] + k3[i];
    }
    func(t+delta_t, support, k4, params);                       // Berechnung k4 = f(t+dt, y+k2) * dt und y_(i+1)
    for (int i = 0; i < dimension; i++) {
        k4[i] *= delta_t;
        y[i] += (k1[i] + 2*k2[i] + 2*k3[i] + k4[i]) / 6; 
    }
    free(support), free(k1), free(k2), free(k3), free(k4);
    return;   
}


// numerische Integration
void cvc_verlet_step(double t, double delta_t, double y[], cvc_ode_func func, int dimension, void *params) {
    int N = dimension / 2;
    double *a1 = (double*) calloc(dimension, sizeof(double));
    double *a2 = (double*) calloc(dimension, sizeof(double));
    func(t, y, a1, params);                                     // Berechnung von a1 = f(t, y) * dt
    for (int i = 0; i < N; i++) {                               // Berechnung (erster Hälfte, Positionen) von y_(i+1) aus a1
        y[i] += a1[i] * delta_t + a1[i+N] * (delta_t * delta_t) /2;
    }
    func(t+delta_t, y, a2, params);                             // Berechnung von a2 = f(t+delta_t, y_(i+1)) aus Positionen von y_(i+1)
    for (int i = 0; i < N; i++) {                               // Berechnung (zweite Hälfte, Geschwindigkeiten) von y_(i+1) aus a1 und a2
        y[i+N] += (a1[i+N] + a2[i+N]) * delta_t / 2;
    }                                                                                                                 
    free(a1), free(a2);
    return;
}