#include <iostream>
#include <fstream>
#include <time.h>
#include <cmath>


// type state of a node on the grid: empty node, hydrophobic [H] or polar [P] monomer, or border region 
typedef enum {
    BORDER = -1,
    EMPTY = 0,
    HYDROPHOBIC = 1,
    POLAR = 2,
} node_state;


// type direction of the subsequent monomer on the grid
typedef enum {
    NORTH = 1,
    EAST = 2,
    SOUTH = 3,
    WEST = 4,
} node_direction;


// type polymer end position on a the grid
typedef struct {
    int m;
    int n;
} node_position;


// type protein grid with the 33 x 33 array and the actual polymer end
typedef struct {
    node_state node[33][33];
    node_position prior;
    node_position end;
    int length;
    double energy;
} grid;


// returns the state of a new monomer according to the probability of a polar monomer 'p_polar'
node_state get_state(double p_polar) {
    double rand_uniform = (double) rand() / RAND_MAX;
    if (rand_uniform < p_polar) {
        return POLAR;
    } else {
        return HYDROPHOBIC;
    }
}


// function to initialize 33 x 33 grid with borders (i.e. a 31 x 31 grid to work on)
void grid_init(grid *polymer_grid) {
    for (int m = 0; m < 33; m++) {
        for (int n = 0; n < 33; n++) {
            if (m == 0 || m == 32 || n == 0 || n == 32) {
                polymer_grid->node[m][n] = BORDER;                              // initialize border nodes as BORDER
            } else {
                polymer_grid->node[m][n] = EMPTY;;                              // initializes other nodes as EMPTY
            }
        }
    }
    polymer_grid->end.m = 16;                                                   // center the m coordinate as the END
    polymer_grid->end.n = 16;                                                   // center the n coordinate as the EN
    polymer_grid->length = 0;                                                   // set the length to 0
    polymer_grid->energy = 0;                                                   // set the energy to 0
    return;
}


// generates random direction
node_direction get_grid_direction() {
    switch (rand() % 4 + 1) {
        case 1:
            return NORTH;
        case 2:
            return EAST;
        case 3:
            return SOUTH;
        case 4:
            return WEST;
        // should never be reached anyway, WHAT THE HECK
        default:
            return NORTH;
    }
}


// function to add monomer to the polymer grid
int grid_add_monomer(grid *polymer_grid, double p_polar, double epsilon, std::ofstream *outfile = NULL) {
    int prior_m = polymer_grid->prior.m;                                        // get the m position of the previous node
    int prior_n = polymer_grid->prior.n;                                        // get the n position of the previous node
    int m = polymer_grid->end.m;                                                // get the m position of the current ending
    int n = polymer_grid->end.n;                                                // get the n position of the current ending
    int delta_m = prior_m-m, delta_n = prior_n-n;                               // initialize the increment of m and n directed towards the previous node

    node_state next_state = get_state(p_polar);                                 // get new monomer state  according to probability 'p_polar'
    polymer_grid->node[m][n] = next_state;                                      // place new monomer
    polymer_grid->length += 1;                                                  // increase the chain length by 1

    // check for availability of neighboring nodes and chose coordinate for new monomer in case
    node_state state_NORTH = polymer_grid->node[m-1][n];                        // state of node NORTH
    node_state state_EAST = polymer_grid->node[m][n+1];                         // state of node EAST
    node_state state_SOUTH = polymer_grid->node[m+1][n];                        // state of node SOUTH
    node_state state_WEST = polymer_grid->node[m][n-1];                         // state of node WEST

    // update energy for HYDROPHOBIC monomer
    if (next_state == HYDROPHOBIC) {
        if (state_NORTH == HYDROPHOBIC && delta_m != -1) {
            polymer_grid->energy -= epsilon;
        }
        if (state_EAST == HYDROPHOBIC && delta_n != 1) {
            polymer_grid->energy -= epsilon;
        }
        if (state_SOUTH == HYDROPHOBIC && delta_m != 1) {
            polymer_grid->energy -= epsilon;
        }
        if (state_EAST == HYDROPHOBIC && delta_n != -1) {
            polymer_grid->energy -= epsilon;
        }
    }

    // write new monomer and energy to file in case
    if (outfile) {
        *outfile << m-1 << ", " << n-1 << ", " << next_state << ", " << polymer_grid->energy << "\n";
    }

    // no free node available: return polymer length
    if (state_NORTH && state_EAST && state_SOUTH && state_WEST) {
        return polymer_grid->length;
    // free node is available: try random directions until a free node is found                                           
    } else {
        do {
            node_direction next_direction = get_grid_direction();               // generate a random direction
            switch (next_direction) {                                           // set the next node according to the previously generated direction
                case NORTH: 
                    next_state = polymer_grid->node[m-1][n];
                    delta_m = -1;
                    delta_n = 0;
                    break;
                case EAST:
                    next_state = polymer_grid->node[m][n+1];
                    delta_m = 0;
                    delta_n = 1;
                    break;
                case SOUTH:
                    next_state = polymer_grid->node[m+1][n];
                    delta_m = 1;
                    delta_n = 0;
                    break;
                case WEST:
                    next_state = polymer_grid->node[m][n-1];
                    delta_m = 0;
                    delta_n = -1;
                    break;
            }
        } while (next_state);                                                   // breaks when the state of the chosen node is 0, i.e. available

        // update the grid prior as the current node position
        polymer_grid->prior.m = m;
        polymer_grid->prior.n = n;
        // update the grig ending as the upcoming node position for the next iteration
        polymer_grid->end.m += delta_m;
        polymer_grid->end.n += delta_n;
    }
    return 0;
}


// function to print out the grid
void grid_print(grid* polymer_grid) {
    for (int m = 0; m < 33; m++) {
        for (int n = 0; n < 33; n++) {
            switch (polymer_grid->node[m][n]) {
                case BORDER:
                    std::cout << "+";
                    break;
                case HYDROPHOBIC:
                    std::cout << "H";
                    break;
                case POLAR:
                    std::cout << "P";
                    break;
                // node as EMPTY as Tottenhams trophy cabinet
                default:
                    std::cout << " ";
                    break;
            } ;
        }
        std::cout << "\n";
    }
    return;
}


// generating 3 protein samples
int main(void) {
    // physical constants
    double p_polar = 0.3;                                                       // probability of a polar monomer
    double epsilon = 1.0;                                                       // energy constant

    // setting up the files
    std::ofstream *outfile_high = new std::ofstream;
    std::ofstream *outfile_medium = new std::ofstream;
    std::ofstream *outfile_low = new std::ofstream;
    outfile_high->open("data/protein_folding_high_energy.csv");
    outfile_medium->open("data/protein_folding_medium_energy.csv");
    outfile_low->open("data/protein_folding_low_energy.csv");
    *outfile_high << "m, n, Node Status, Energy E\n";
    *outfile_medium << "m, n, Node Status, Energy E\n";
    *outfile_low << "m, n, Node Status, Energy E\n";

    // initialize the protein grid struct for high energy protein
    srand (6);                                                                  // seed 6 to to generate low energy protein
    grid *protein_grid_high = new grid;                                         // allocate struct grid memory dynamically                                         
    grid_init(protein_grid_high);                                               // initialize the polypeptide grid with borders and empty nodes
    do {} while(!grid_add_monomer(protein_grid_high, p_polar, epsilon, outfile_high));
    outfile_high->close();
    delete protein_grid_high;                                                   // free struct grid memory
    delete outfile_high;                                                        // free filebuffer

    // initialize the protein grid struct for medium energy protein
    srand (38);                                                                 // seed 38 to to generate low energy protein
    grid *protein_grid_medium = new grid;                                       // allocate struct grid memory dynamically                                         
    grid_init(protein_grid_medium);                                             // initialize the polypeptide grid with borders and empty nodes
    do {} while(!grid_add_monomer(protein_grid_medium, p_polar, epsilon, outfile_medium));
    outfile_medium->close();
    delete protein_grid_medium;                                                 // free struct grid memory
    delete outfile_medium;                                                      // free filebuffer

    // initialize the protein grid struct for low energy protein
    srand (217);                                                                // seed 217 to to generate low energy protein
    grid *protein_grid_low = new grid;                                          // allocate struct grid memory dynamically                                         
    grid_init(protein_grid_low);                                                // initialize the polypeptide grid with borders and empty nodes
    do {} while(!grid_add_monomer(protein_grid_low, p_polar, epsilon, outfile_low));
    outfile_low->close();
    delete protein_grid_low;                                                    // free struct grid memory
    delete outfile_low;                                                         // free filebuffer

    return 0;
}