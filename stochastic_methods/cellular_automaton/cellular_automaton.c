#include <stdio.h>
#include <stdlib.h>
#include <tgmath.h>
#include <time.h>
#include <gsl/gsl_rng.h>
#include "../../cvc_numerics.h"
#include "../../cvc_rng.h"


// statically implemented pseudorandom number generator Mersenne Twister MT19937
double random_uniform(void) {
    static gsl_rng* generator = NULL;                                               // initializing the static rng variable
    if (generator == NULL) {                                                        // initializing MT19937 as rng at the first function call 
        generator = gsl_rng_alloc(gsl_rng_mt19937);
        gsl_rng_set(generator, time(NULL));
    }
    return gsl_rng_uniform(generator);
}


// print out a given quadratic grid of sidelength 'length' ignoring its ghosts
void print_grid(int *grid, int length) {
    printf("\n+++ print grid +++\n\n");
    for (int row_i = 1; row_i < length-1; row_i++) {
        for (int column_j = 1; column_j < length-1; column_j++) {
            int *node = &grid[row_i*length + column_j];
            if (*node == -1) {
                printf("V");
            } else {
                printf("%d", *node);
            }
        }
        printf("\n");
    }
    printf("\n+++ end of print +++\n");
    return;
}


// initialize the given 'grid' of 'length' (L+2) with integers 0 (Susceptible S), 1 (Infected I), 2 (Recovered R) and -1 (Vaccinated V)
void grid_init(int *grid, int length, double *probabilities) {
    double p4 = probabilities[3];                                                   // caching the probability of someone being initialized as V                                      
    // iterating through the grid ignoring the borders
    for (int row_i = 1; row_i < length-1; row_i++) {
        for (int column_j = 1; column_j < length-1; column_j++) {
            if (random_uniform() < p4) {                                            // person is initialized as V for random_uniform < 'p4'
                grid[row_i*length + column_j] = -1;
            } else {                                                                // person initialized as S, I or R with equal probabilities 
                grid[row_i*length + column_j] = (int) (random_uniform() * 3);
            }
        }
    }
    return;
}


// updates a single node with given postion according to the 'probabilities'
void update_node(int *grid, int length, int row_i, int column_j, double *probabilities) {
    // caching the turnover-propabilities from the double-array for later use
    double p1 = probabilities[0];
    double p2 = probabilities[1];
    double p3 = probabilities[2];
    int *node = &grid[row_i*length + column_j];                                     // caching the pointer on the selceted 'node' to change the grid in-place
    switch (*node) {                                                                // select for the state the selected person/node is in
        case -1:                                                                    // -1: person is in state vaccinated V and will remain there
            break;
        case 0:                                                                     // 0: person is susceptible S and gets infected I with p1 for (at least) one infected neighbor
            int north_node_state = grid[(row_i+1)*length + column_j];
            int south_node_state = grid[(row_i-1)*length + column_j];                                                 
            int east_node_state = grid[row_i*length + (column_j-1)];
            int west_node_state = grid[row_i*length + (column_j+1)];
            if ((north_node_state == 1 || south_node_state == 1 || east_node_state == 1 || west_node_state == 1) && random_uniform() < p1) {
                *node = 1;
            }
            break;
        case 1:                                                                     // 1: person is infected I and turns recovered R with p2            
            if (random_uniform() < p2) {
                *node = 2;
            }
            break;
        case 2:                                                                     // 2: person is recovered R and return susceptible S with p3
            if (random_uniform() < p3) {
                *node = 0;
            }
    }
    return;
}


// update the 'grid' with 'length' according to the 'probibilities' (all grid-points in sequence)
void grid_update_linear(int *grid, int length, double *probabilities) {
    for (int row_i = 1; row_i < length-1; row_i++) {
        for (int column_j = 1; column_j < length-1; column_j++) {
            update_node(grid, length, row_i, column_j, probabilities);
        }
    }
    return;
}


// update the 'grid' with 'length' according to the 'probibilities' (L^2 grid-points randomly chosen)
void grid_update_stochastic(int *grid, int length, double *probabilities) {
    for (int i = 0; i < (length-2) * (length-2); i++) {
        int row_i = ((int) (random_uniform() * (length-2))) + 1;
        int column_j = ((int) (random_uniform() * (length-2))) + 1;
        update_node(grid, length, row_i, column_j, probabilities);
    }
    return;
}


// returns the ratio infected to uninfected for the given 'grid' of 'length' 
double ratio_infected(int *grid, int length) {
    double sum_infected = 0;
    for (int row_i = 1; row_i < length-1; row_i++) {
        for (int column_j = 1; column_j < length-1; column_j++) {
            int *node = &grid[row_i*length + column_j];
            if (*node == 1) {
                sum_infected++;
            }
        }
    }
    return sum_infected / ((length-2) * (length-2));
} 


// returns the average ratio infected to uninfected over 'T' simulation steps for given 'grid', 'length' and 'probabilities'
double average_ratio_infected(int *grid, int length, int T, double *probabilities) {
    double sum_ratio = ratio_infected(grid, length);
    for (int i = 0; i < T; i++) {
        grid_update_stochastic(grid, length, probabilities);
        sum_ratio += ratio_infected(grid, length);
    }
    return sum_ratio / T;
}


int main(void) {
    int L = 96;                                                                 // grid length
    int T = 1000;                                                               // number 'T' of simulation steps

    // allocating memory for three grids a, b and c
    int *infectious_grid_t96_a = (int*) calloc((L+2)*(L+2), sizeof(int));
    int *infectious_grid_t96_b = (int*) calloc((L+2)*(L+2), sizeof(int));
    int *infectious_grid_t96_c = (int*) calloc((L+2)*(L+2), sizeof(int));
    if (infectious_grid_t96_a == NULL || infectious_grid_t96_b == NULL || infectious_grid_t96_c == NULL) {
        printf("ERROR! Memory is not available, please add more RAM.");
        return 1;
    }
    printf("Time Evolution Grid: calculating (< 4 sec) ...\n");                 // progress bar for time evolution

    // initializing the three probability arrays
    double probability_array_t96_a[4] = {0.5, 0.5, 0.5, 0};                     // probability array for a: 'p1' = 'p2' = 'p3' = 0.5, no vaccination rate
    double probability_array_t96_b[4] = {0.75, 0.5, 0.5, 0};                    // probability array b: high turnover rates for infections and lower ones for susceptibility and recovery
    double probability_array_t96_c[4] = {0.75, 0.5, 0.5, 0.25};                 // probability array c: same as b, only with vaccination rate of 'p4' = 0.25 

    // initializing the grids using the above probabilities
    grid_init(infectious_grid_t96_a, L+2, probability_array_t96_a);
    grid_init(infectious_grid_t96_b, L+2, probability_array_t96_b);
    grid_init(infectious_grid_t96_c, L+2, probability_array_t96_c);  

    // setting up the files a, b and c for the different probability arrays and writing the initial timestep 0 in the first column of the first row
    FILE* grid_file_a = fopen("data/soi_grid_over_time_a.csv", "w");
    FILE* grid_file_b = fopen("data/soi_grid_over_time_b.csv", "w");
    FILE* grid_file_c = fopen("data/soi_grid_over_time_c.csv", "w");
    fprintf(grid_file_a, "0");
    fprintf(grid_file_b, "0");
    fprintf(grid_file_c, "0");

    // iterating through the grid ignoring the borders to fill the files fist row with the initial grid data (the 1D structure of the grid resembles the one on the RAM dimension wise)
    for (int row_i = 1; row_i < L+1; row_i++) {
        for (int column_j = 1; column_j < L+1; column_j++) {
            fprintf(grid_file_a, ", %d", infectious_grid_t96_a[row_i*(L+2) + column_j]);
            fprintf(grid_file_b, ", %d", infectious_grid_t96_b[row_i*(L+2) + column_j]);
            fprintf(grid_file_c, ", %d", infectious_grid_t96_c[row_i*(L+2) + column_j]);
        }
    }

    // iterating over T timesteps
    for (int t = 1; t <= T; t++) {
        // adding timestep t to the files first column
        fprintf(grid_file_a, "\n%d", t);
        fprintf(grid_file_b, "\n%d", t);
        fprintf(grid_file_c, "\n%d", t);

        // updating the three grids according to the probability array
        grid_update_stochastic(infectious_grid_t96_a, L+2, probability_array_t96_a);
        grid_update_stochastic(infectious_grid_t96_b, L+2, probability_array_t96_b);
        grid_update_stochastic(infectious_grid_t96_c, L+2, probability_array_t96_c);

        // iterating through the grid adding its data for timestep t
        for (int row_i = 1; row_i < L+1; row_i++) {
            for (int column_j = 1; column_j < L+1; column_j++) {
                fprintf(grid_file_a, ", %d", infectious_grid_t96_a[row_i*(L+2) + column_j]);
                fprintf(grid_file_b, ", %d", infectious_grid_t96_b[row_i*(L+2) + column_j]);
                fprintf(grid_file_c, ", %d", infectious_grid_t96_c[row_i*(L+2) + column_j]);
            }
        }
    }
    free(infectious_grid_t96_a);
    free(infectious_grid_t96_b);
    free(infectious_grid_t96_c);
    fclose(grid_file_a);
    fclose(grid_file_b);
    fclose(grid_file_c);
    return 0;
}