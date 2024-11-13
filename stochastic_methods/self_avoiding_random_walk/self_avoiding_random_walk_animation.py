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
        self.add(self.canvas_rect)

        self.canvas = np.zeros((self.m+1, self.n+1))                                                # array tracking the placed monomers (additional layer in m, n direction for H-H pair check)
        self.polymer_length = 0                                                                     # physical polymer length
        self.polymer_energy = 0                                                                     # physical polymer energy

    
    # method to add a monomer (HYDROPHOBIC: 1, POLAR: 2) at position m, n
    def add_monomer(self, type, m, n):
        monomer_centre = self.canvas_origin + m*self.delta_mn*UP + n*self.delta_mn*RIGHT            # center of the new monomer square
        self.canvas[m,n] = type                                                                     # add residue to the canvas array
        self.polymer_length += 1                                                                    # increase the polymer length

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
            connector = Line(start = self.prior_center, end = monomer_centre, color = GREY, stroke_width = 2, stroke_opacity = 1)
            self.add(connector)

            # for second monomer onwards check for H-H pairs
            if type == 1:
                if self.canvas[m+1,n] == 1 and self.prior_mn[0] != m+1:
                    HH_cross = Cross(stroke_color = WHITE, stroke_width = 2, scale_factor = 0.035).move_to(monomer_centre + self.delta_mn/2*UP)
                    self.add(HH_cross)
                    self.polymer_energy += 1
                elif self.canvas[m-1,n] == 1 and self.prior_mn[0] != m-1:
                    HH_cross = Cross(stroke_color = WHITE, stroke_width = 2, scale_factor = 0.035).move_to(monomer_centre - self.delta_mn/2*UP)
                    self.add(HH_cross)
                    self.polymer_energy += 1
                elif self.canvas[m,n+1] == 1 and self.prior_mn[1] != n+1:
                    HH_cross = Cross(stroke_color = WHITE, stroke_width = 2, scale_factor = 0.035).move_to(monomer_centre + self.delta_mn/2*RIGHT)
                    self.add(HH_cross)
                    self.polymer_energy += 1
                elif self.canvas[m,n-1] == 1 and self.prior_mn[1] != n-1:
                    HH_cross = Cross(stroke_color = WHITE, stroke_width = 2, scale_factor = 0.035).move_to(monomer_centre - self.delta_mn/2*RIGHT)
                    self.add(HH_cross)
                    self.polymer_energy += 1                

        # setting the current monomer position as the upcoming prior
        self.prior = True
        self.prior_mn = (m,n)
        self.prior_center = monomer_centre

    
    # method to add a legend
    def get_legend(self, legend_centre_left, stretch):
        out_stretch = stretch
        in_stretch = stretch / 3
        polymer_chain = Line(start = legend_centre_left + out_stretch*UP + 0.25*LEFT, end = legend_centre_left + out_stretch*UP + 0.25*RIGHT, color = GREY, stroke_width = 2, stroke_opacity = 1)
        P_monomer = Square(color = BLUE, fill_opacity = 0.5, side_length = 0.25, stroke_width = 1).move_to(legend_centre_left + in_stretch*UP)
        H_monomer = Square(color = RED, fill_opacity = 0.5, side_length = 0.25, stroke_width = 1).move_to(legend_centre_left + in_stretch*DOWN)
        HH_link = Cross(stroke_color = WHITE, stroke_width = 2, scale_factor = 0.1).move_to(legend_centre_left + out_stretch*DOWN)
        polymer_chain_descriptor = Tex(r"polymer chain", font_size = 36, color = GREY).next_to(legend_centre_left + out_stretch*UP + RIGHT)
        P_monomer_descriptor = Tex(r"(P) monomer", font_size = 36, color = BLUE).next_to(legend_centre_left + in_stretch*UP + RIGHT)
        H_monomer_descriptor = Tex(r"(H) monomer", font_size = 36, color = RED).next_to(legend_centre_left + in_stretch*DOWN + RIGHT)
        HH_link_descriptor = Tex(r"H-H link", font_size = 36, color = WHITE).next_to(legend_centre_left + out_stretch*DOWN + RIGHT)
        return VGroup(polymer_chain, P_monomer, H_monomer, HH_link, polymer_chain_descriptor, P_monomer_descriptor, H_monomer_descriptor, HH_link_descriptor)
    

    # get quantities of polymer length L and energy E
    def get_quantity(self, length = 0, energy = 0):
        length_descriptor = Tex(f"$L={length}l$", color = WHITE, font_size = 24).next_to(self.canvas_rect, UP).shift(1.75*LEFT)
        energy_descriptor = Tex(f"$E=-{energy}\epsilon$", color = WHITE, font_size = 24).next_to(self.canvas_rect, UP).shift(1.5*RIGHT)
        return VGroup(length_descriptor, energy_descriptor)



class self_avoiding_random_walk_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        headline = Title(r"Self-Avoiding Random Walk", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT)
        self.add(headline)

        # parameters
        canvas_centre = np.array([-3, -0.5, 0])
        canvas_shape = (31, 31)
        canvas_cell_length = 0.15

        legend_centre_left = np.array([1.5, -0.5, 0])
        legend_stretch = 1

        canvas = RandomWalk(canvas_centre, canvas_shape, canvas_cell_length)
        canvas_legend = canvas.get_legend(legend_centre_left, legend_stretch)
        canvas_quantity = canvas.get_quantity(canvas.polymer_length, canvas.polymer_energy)
        self.add(canvas, canvas_legend, canvas_quantity)


        # iterating through the polymer data
        self.wait(1.5)
        for monomer in protein_folding_low_energy_data:
            # add new monomer
            monomer_type = monomer[2]
            monomer_m = int(monomer[0])
            monomer_n = int(monomer[1])
            canvas.add_monomer(monomer_type, monomer_m, monomer_n)

            # update random walk quantities
            self.remove(canvas_quantity)
            canvas_quantity = canvas.get_quantity(canvas.polymer_length, canvas.polymer_energy)
            self.add(canvas_quantity)
            self.wait(0.1)
        self.wait(5)