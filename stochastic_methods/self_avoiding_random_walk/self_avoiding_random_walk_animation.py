from manim import *


# visualization of three proteins (low, medium, and high number of H-H links)
protein_folding_high_energy_data = np.loadtxt("data/protein_folding_high_energy.csv", delimiter = ",", skiprows = 1)
protein_folding_medium_energy_data = np.loadtxt("data/protein_folding_medium_energy.csv", delimiter = ",", skiprows = 1)
protein_folding_low_energy_data = np.loadtxt("data/protein_folding_low_energy.csv", delimiter = ",", skiprows = 1)



class RandomWalk(Mobject):
    def __init__(self, centre, shape, delta_mn, **kwargs):
        super().__init__(**kwargs)
        
        # canvas size
        self.m = shape[0]                                                                           # m: vertical elements
        self.n = shape[1]                                                                           # n: horizontal elements
        self.prior = False                                                                          # bool: has there been a previous monomer?
        self.prior_mn = False                                                                       # m, n of the previous monomer
        self.prior_center = False                                                                   # center of the previous monomer
        self.delta_mn = delta_mn                                                                    # sidelength of one individual square
        self.canvas_center = centre                                                                 # center of the random walk canvas
        self.canvas_origin = centre + self.n/2*delta_mn*LEFT + self.m/2*delta_mn*DOWN               # coordinates of the bottom left square
        self.canvas_height = self.m*delta_mn
        self.canvas_width = self.n*delta_mn
        self.canvas_rect = Rectangle(height = self.canvas_height+delta_mn, width = self.canvas_width+delta_mn, color = WHITE, stroke_width = 0.5).move_to(centre)
        self.canvas = np.zeros((self.m, self.n))                                                    # array tracking the placed monomers
        self.add(self.canvas_rect)

    
    # method to add a monomer (HYDROPHOBIC: 1, POLAR: 2) at position m, n
    def add_monomer(self, type, m, n):
        monomer_centre = self.canvas_origin + m*self.delta_mn*UP + n*self.delta_mn*RIGHT
        # hydrophobic residue (1: RED)
        if type == 1:
            hydrophobic_square = Square(color = RED, fill_opacity = 0.5, side_length = self.delta_mn-0.005, stroke_width = 1).move_to(monomer_centre)
            self.add(hydrophobic_square)
        # polar residue (2: BLUE)
        elif type == 2:
            hydrophobic_square = Square(color = BLUE, fill_opacity = 0.5, side_length = self.delta_mn-0.005, stroke_width = 1).move_to(monomer_centre)
            self.add(hydrophobic_square)
        # draw connector
        if self.prior:
            connector = Line(start = self.prior_center, end = monomer_centre, color = WHITE, stroke_width = 2, stroke_opacity = 0.5)
            self.add(connector)
        # setting the current monomer position as the upcoming prior
        self.prior = True
        self.prior_center = monomer_centre


class self_avoiding_random_walk_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        headline = Title(r"Self-Avoiding Random Walk", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT)
        self.add(headline)

        # parameters
        canvas_centre = np.array([-2.5, -0.5, 0])
        canvas_shape = (31, 31)
        canvas_cell_length = 0.15

        canvas = RandomWalk(canvas_centre, canvas_shape, canvas_cell_length)
        self.add(canvas)


        # iterating through the polymer data
        for monomer in protein_folding_low_energy_data:
            monomer_type = monomer[2]
            monomer_m = monomer[0]
            monomer_n = monomer[1]
            canvas.add_monomer(monomer_type, monomer_m, monomer_n)
            # print(monomer)


# print(A3_protein_folding_high_energy_data)