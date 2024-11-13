from manim import *


# visualization of three proteins (low, medium, and high number of H-H links)
A3_protein_folding_high_energy_data = np.loadtxt("data/protein_folding_high_energy.csv", delimiter = ",", skiprows = 1)
A3_protein_folding_medium_energy_data = np.loadtxt("data/protein_folding_medium_energy.csv", delimiter = ",", skiprows = 1)
A3_protein_folding_low_energy_data = np.loadtxt("data/protein_folding_low_energy.csv", delimiter = ",", skiprows = 1)



class RandomWalk(Mobject):
    def __init__(self, centre, m, n, delta_mn, **kwargs):
        super().__init__(**kwargs)



class self_avoiding_random_walk_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 


print(A3_protein_folding_high_energy_data)