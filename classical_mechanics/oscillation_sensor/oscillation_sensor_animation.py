from manim import *
from numpy import linalg as npl


# processing data
oscillation_sensor_data = np.loadtxt("data/oscillation_sensor.csv", delimiter = ",", skiprows = 1)

x1_array = 5 * oscillation_sensor_data[::10,1]
y1_array = 5 * oscillation_sensor_data[::10,2] / 4

x1_iter = iter(x1_array)
y1_iter = iter(y1_array)
x1_A_iter = iter(x1_array)
y1_A_iter = iter(y1_array)
x1_B_iter = iter(x1_array)
y1_B_iter = iter(y1_array)


# force field
x0 = -5             # x-position anchor 1
x1 = 5              # x-position anchor 2
r0 = 5              # rest length of both springs
k = 0.1             # spring constant
smoothing_factor = 1e-10


# spring model
def Spring(start = UP, end = DOWN, tip_buff = 0.25, nodes = 20, k = 0.5, color = WHITE):
    spring_group = VGroup()
    start[2], end[2] = 0, 0

    # extended parameters
    direction = (end - start) / npl.norm(end - start)
    anti_direction = np.array([direction[1], -direction[0], direction[2]])
    eff_start = start + tip_buff*direction
    eff_end = end - tip_buff*direction
    eff_length = npl.norm(eff_end - eff_start)
    node_length = eff_length / nodes
    node_deviance = k

    # add line with given start 'l_start' and endpoint 'l_end'
    def spring_add_line(l_start, l_end):
        spring_group.add(Line(l_start, l_end, color = color, stroke_width = 4, stroke_opacity = 0.5))
    
    # adding point with given 'pos'
    def spring_add_dot(d_pos):
        spring_group.add(Dot(d_pos, color = color, radius = 0.02))

    # objects
    spring_add_line(start, eff_start)               # start linie
    spring_add_line(eff_end, end)                   # end line
    spring_add_dot(eff_start)                       # start dot
    spring_add_dot(eff_end)                         # end dot
    spring_add_line(eff_start, eff_start + direction * node_length / 2 + anti_direction * node_deviance / 2)                                # first line
    spring_add_dot(eff_start + direction * node_length / 2 + anti_direction * node_deviance / 2)                                            # first dot
    spring_add_line(eff_start + direction * (nodes - 1/2) * node_length + (-1)**(nodes+1) * anti_direction * node_deviance / 2, eff_end)    # last line
    for i in range(1, nodes):
        spring_add_line(eff_start + direction * (i - 1/2) * node_length + (-1)**(i+1) * anti_direction * node_deviance / 2, eff_start + direction * (i + 1/2) * node_length + (-1)**(i) * anti_direction * node_deviance / 2)
        spring_add_dot(eff_start + direction * (i + 1/2) * node_length + (-1)**(i) * anti_direction * node_deviance / 2)
    return spring_group


# force field
def F(pos):
    pos = pos / 2 
    pos[1] = pos[1] * 4
    force_left = -k * ( (np.sqrt((pos[0]-x0)**2 + pos[1]**2) - r0) / (np.sqrt((pos[0]-x0)**2 + pos[1]**2) + smoothing_factor) ) * ((pos[0]-x0) * RIGHT + pos[1] * UP )
    force_right = -k * ( (np.sqrt((pos[0]-x1)**2 + pos[1]**2) - r0) / (np.sqrt((pos[0]-x1)**2 + pos[1]**2) + smoothing_factor) ) * ((pos[0]-x1) * RIGHT + pos[1] * UP )
    return force_left + force_right


class oszillation_sensor_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline and vectorfeld
        text_oszi = Tex(r"Schwingungssensor: $\Vec{F}=m\ddot{\Vec{x}}=-k\Vec{x}$ (Newton)", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT)  
        eq_field = Tex(
            r"$\Vec{F}=-k\left(1-\frac{r_0}{\sqrt{(x-x_1)^2+y^2}}\right)\begin{bmatrix} x-x_1 \\ y \end{bmatrix}-k\left(1-\frac{r_0}{\sqrt{(x-x_2)^2+y^2}}\right)\begin{bmatrix} x-x_2 \\ y \end{bmatrix}$", 
            color = WHITE, font_size = 32).align_on_border(DOWN + LEFT, buff = 0.5).shift(1.5 * RIGHT)  
        avf = ArrowVectorField(
            F, x_range = [-10, 10, 1], y_range = [-4, 4, 1], length_func = lambda x: 1*x, 
            colors = [WHITE], opacity = 0.375, vector_config = {'stroke_width': 2}).scale(0.5)

        # spring parameters
        spring_nodes = 20
        spring_tip_buff = 0.25
        spring_k = 0.5

        # mass, anchorings and springs
        mass1 = Circle(color = RED, radius = 0.1, fill_color = RED, fill_opacity = 0.75).move_to([x1_array[0], y1_array[0], 1])
        mass1.z_index = 2
        line_A = Line([-5, -2, 0], [-5, 2, 0], color = WHITE, stroke_width = 5)
        line_B = Line([5, -2, 0], [5, 2, 0], color = WHITE, stroke_width = 5)
        A = Dot([-5, 0, 0], color = RED, radius = 0.05)
        B = Dot([5, 0, 0], color = RED, radius = 0.05)
        connec_A = Spring(start = np.array([-5, 0, 0]), end = np.array([x1_array[0], y1_array[0], 0]), k = spring_k, tip_buff = spring_tip_buff, nodes = spring_nodes)
        connec_B = Spring(start = np.array([5, 0, 0]), end = np.array([x1_array[0], y1_array[0], 0]), k = spring_k, tip_buff = spring_tip_buff, nodes = spring_nodes)

        # mass updater
        def mass_updater(mass):
            x_mass = next(x1_iter)
            y_mass = next(y1_iter)
            self.add(Line(start = mass.get_center(), end = [x_mass, y_mass, 0], stroke_width = 1, color = RED).set_opacity(0.5))
            mass.move_to([x_mass, y_mass, 0])

        # spring A updater
        def spring_A_updater(spring):
            x_mass = next(x1_A_iter)
            y_mass = next(y1_A_iter)
            connec_A.become(Spring(start = np.array([-5, 0, 0]), end = np.array([x_mass, y_mass, 0]), k = spring_k, tip_buff = spring_tip_buff, nodes = spring_nodes))

        # spring B updater
        def spring_B_updater(spring):
            x_mass = next(x1_B_iter)
            y_mass = next(y1_B_iter)
            connec_B.become(Spring(start = np.array([5, 0, 0]), end = np.array([x_mass, y_mass, 0]), k = spring_k, tip_buff = spring_tip_buff, nodes = spring_nodes))


        # self.add(text_oszi, eq_field, avf, line_A, line_B, A, B, mass1)

        self.play(Write(text_oszi), run_time = 1.5)
        self.wait(0.5)
        self.play(FadeIn(line_A), FadeIn(line_B), FadeIn(mass1), FadeIn(connec_A), FadeIn(connec_B), FadeIn(A), FadeIn(B), run_time = 3)
        self.wait(0.5)
        self.play(Write(eq_field), Create(avf), run_time = 3)
        self.wait(1.5)

        mass1.add_updater(mass_updater)
        connec_A.add_updater(spring_A_updater)
        connec_B.add_updater(spring_B_updater)

        timeline = ValueTracker(0)
        self.play(timeline.animate.set_value(10), rate_func = linear, run_time = 20)
        self.wait(5)