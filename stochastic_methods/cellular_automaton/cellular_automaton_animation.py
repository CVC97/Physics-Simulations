from manim import *


# global grid parameters
GRID_CENTER = np.array([-3, -0.5, 0])
GRID_SIDE_LENGTH = 5.5
GRID_L = 96
GRID_NODE_DIST = GRID_SIDE_LENGTH / (GRID_L + 1)


# get grid coordinates for given row i and column j
def get_grid_coordinates(i_row, j_colum):
    grid_top_left_node = GRID_CENTER + np.array([-GRID_SIDE_LENGTH / 2 + GRID_NODE_DIST, GRID_SIDE_LENGTH / 2 - GRID_NODE_DIST, 0])
    return grid_top_left_node + np.array([j_colum, -i_row, 0])  * GRID_NODE_DIST


# data processing
soi_grid_over_time_data_a = np.loadtxt("data/soi_grid_over_time_a.csv", delimiter = ",", skiprows = 0)
soi_grid_over_time_data_b = np.loadtxt("data/soi_grid_over_time_b.csv", delimiter = ",", skiprows = 0)
soi_grid_over_time_data_c = np.loadtxt("data/soi_grid_over_time_c.csv", delimiter = ",", skiprows = 0)

# reshape data array (dim 0: time, dim 1: rows, dim 2: columns) and remove time column 1
time_array = soi_grid_over_time_data_b[:,0]
soi_grid_over_time_array_a = np.reshape(soi_grid_over_time_data_a[:,1:], (1001, GRID_L, GRID_L))
soi_grid_over_time_array_b = np.reshape(soi_grid_over_time_data_b[:,1:], (1001, GRID_L, GRID_L))
soi_grid_over_time_array_c = np.reshape(soi_grid_over_time_data_c[:,1:], (1001, GRID_L, GRID_L))


# main scene
class cellular_automaton_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC)

        # headline
        headline = Title(r"Model for the Spread of Infectious Diseases", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT)

        # legend
        square_susceptible = Square(color = WHITE, fill_opacity = 0.5, side_length = 0.3, stroke_width = 1).move_to([2, 2.1, 0])
        square_infected = Square(color = RED, fill_opacity = 0.5, side_length = 0.3, stroke_width = 1).move_to([2, 1.35, 0])
        square_recovered = Square(color = BLUE, fill_opacity = 0.5, side_length = 0.3, stroke_width = 1).move_to([2, 0.6, 0])
        square_vaccinated = Square(color = GREY, side_length = 0.3, stroke_width = 1).move_to([2, -0.15, 0])
        cross_vaccinated = Cross(stroke_color = GREY, stroke_width = 1, scale_factor = 0.15).move_to([2, -0.15, 0])
        text_susceptible = Tex(r"Susceptible $\textit{S}$", font_size = 36).next_to(square_susceptible, direction = RIGHT)
        text_infected = Tex(r"Infected $\textit{I}$", font_size = 36, color = RED).next_to(square_infected, direction = RIGHT)
        text_recovered = Tex(r"Recovered $\textit{R}$", font_size = 36, color = BLUE).next_to(square_recovered, direction = RIGHT)
        text_vaccinated = Tex(r"Vaccinated $\textit{V}$", font_size = 36, color = GREY).next_to(square_vaccinated, direction = RIGHT)
        legend_group = VGroup(square_susceptible, square_infected, square_recovered, square_vaccinated, cross_vaccinated, text_susceptible, text_infected, text_recovered, text_vaccinated)

        # probability legend
        text_p1 = Tex(r"$p_1(S\rightarrow I)=0.75$", font_size = 20).next_to([2.25, -1.3, 0])
        text_p2 = Tex(r"$p_2(I\rightarrow R)=0.5$", font_size = 20).next_to([2.25, -1.8, 0])
        text_p3 = Tex(r"$p_3(R\rightarrow S)=0.5$", font_size = 20).next_to([2.25, -2.3, 0])
        text_p4 = Tex(r"$p_4(V)=0$", font_size = 20).next_to([2.25, -2.8, 0])
        rectange_probabilities = Rectangle(color = WHITE, height = 2.5, width = 3.75, stroke_width = 1).move_to([3.5, -2, 0])
        text_probabilities = Tex(r"probabilities", color = WHITE, font_size = 18).move_to([2.3, -0.95, 0])
        probability_legend_group = VGroup(text_p1, text_p2, text_p3, text_p4)

        # main infection grid
        main_grid = Square(color = WHITE, side_length = GRID_SIDE_LENGTH, stroke_width = 0.5).move_to(GRID_CENTER)
        main_L = Tex(f"$L=96$", color = WHITE, font_size = 24).move_to([-5, 2.45, 0])
        main_T = Tex(f"$t=0$", color = WHITE, font_size = 24).move_to([-1, 2.45, 0])

        # gridmaker for given 3D array and time t
        def make_grid_from_array(grid_array, t):
            grid_total_group = VGroup()
            for i_row in range(96):
                for j_column in range(96):
                    node_status = grid_array[t, i_row, j_column]
                    node_position = get_grid_coordinates(i_row, j_column)
                    if node_status == -1:
                        grid_node = Square(color = GREY, fill_opacity = 0.5, side_length = GRID_NODE_DIST, stroke_width = 1).move_to(node_position)
                        grid_node_cross = Cross(stroke_color = GREY, stroke_width = 1, scale_factor = GRID_NODE_DIST / 2).move_to(node_position)
                        grid_total_group.add(grid_node, grid_node_cross)
                    elif node_status == 0:
                        grid_node = Square(color = WHITE, fill_opacity = 0.5, side_length = GRID_NODE_DIST, stroke_width = 1).move_to(node_position)
                        grid_total_group.add(grid_node)                  
                    elif node_status == 1:
                        grid_node = Square(color = RED, fill_opacity = 0.5, side_length = GRID_NODE_DIST, stroke_width = 1).move_to(node_position)
                        grid_total_group.add(grid_node)
                    elif node_status == 2:
                        grid_node = Square(color = BLUE, fill_opacity = 0.5, side_length = GRID_NODE_DIST, stroke_width = 1).move_to(node_position)
                        grid_total_group.add(grid_node)
            return grid_total_group


        # adding objects
        # self.add(headline)
        # self.wait(0.5)
        # self.play(FadeIn(legend_group), run_time = 3)
        # self.wait(0.5)
        # self.play(Create(main_grid), Write(main_L), Write(main_T), run_time = 1.5)
        # self.wait(1.5)
        # ### total grid, t = 0 ###
        # total_grid = make_grid_from_array(soi_grid_over_time_array_b, 0)
        # self.play(Create(total_grid), run_time = 5)
        # self.wait(0.5)
        # self.play(Create(rectange_probabilities), Write(text_probabilities), run_time = 1.5)
        # self.play(FadeIn(probability_legend_group), run_time = 3)
        # self.wait(1.5)

        # add everything at once
        self.add(headline, legend_group, main_grid, main_T, rectange_probabilities, text_probabilities, text_probabilities, probability_legend_group, main_L)
        # # ### total grid, t = 0 ###
        total_grid = make_grid_from_array(soi_grid_over_time_array_c, 0)
        self.add(total_grid)
        self.wait(1.5)
        ### total grid t ###
        for t in range(1, 101):
            self.remove(total_grid)
            total_grid = make_grid_from_array(soi_grid_over_time_array_c, t)
            self.add(total_grid)
            if t % 10 == 0:
                self.remove(main_T)
                main_T = Tex(f"$t={t}$", color = WHITE, font_size = 24).move_to([-1, 2.45, 0])
                self.add(main_T)
            self.wait(1/5)
        self.wait(5)