from manim import *
from numpy import linalg as npl


# processing data
euler_data = np.loadtxt("data/pendulums_euler_data.csv", delimiter = ",", skiprows = 1)
rk2_data = np.loadtxt("data/pendulums_rk2_data.csv", delimiter = ",", skiprows = 1)
rk4_data = np.loadtxt("data/pendulums_rk4_data.csv", delimiter = ",", skiprows = 1)
verlet_data = np.loadtxt("data/pendulums_verlet_data.csv", delimiter = ",", skiprows = 1)


# spring model
def Spring(start = UP, end = DOWN, tip_buff = 0.25, nodes = 20, k = 0.5, color = WHITE, stroke_width = 4):
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
        spring_group.add(Line(l_start, l_end, color = color, stroke_width = stroke_width, stroke_opacity = 0.5))
    
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


class pendulums_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline and vectorfeld
        text_pendulums = Title(r"Coupled Spring-Mass System", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 

        x_line = -5.5
        y_sep = 0.8

        y_euler = 1.5
        y_rk2 = y_euler - 2*y_sep
        y_rk4 = y_euler - 4*y_sep
        y_verlet = y_euler - 6*y_sep

        # description of the integrators
        text_euler = Tex(r'(a) Euler:', font_size = 32, color = BLUE).align_on_border(LEFT, buff = 0.75).shift((y_euler+y_sep) * UP)
        text_rk2 = Tex(r'(b) Runge-Kutta 2:', font_size = 32, color = BLUE).align_on_border(LEFT, buff = 0.75).shift((y_rk2+y_sep) * UP)
        text_rk4 = Tex(r'(c) Runge-Kutta 4:', font_size = 32, color = BLUE).align_on_border(LEFT, buff = 0.75).shift((y_rk4+y_sep) * UP)
        text_verlet = Tex(r'(d) Verlet:', font_size = 32, color = BLUE).align_on_border(LEFT, buff = 0.75).shift((y_verlet+y_sep) * UP)

        # create spring
        def ccs(x_pos_array, y_pos):
            spring_group = VGroup()
            spring_group.add(Dot([x_line + x_pos_array[0], y_pos, 0], color = BLUE, radius = 0.1))
            for i_pos in range(1, len(x_pos_array)):
                spring_group.add(Dot([x_line + x_pos_array[i_pos], y_pos, 0], color = BLUE, radius = 0.1))
                spring_group.add(Spring(np.array([x_line + x_pos_array[i_pos], y_pos, 0]), np.array([x_line + x_pos_array[i_pos-1], y_pos, 0]), nodes = 7, tip_buff = 0.1, k = 0.2, stroke_width = 3))
            return spring_group
        
        
        # add text, descriptions
        self.add(text_pendulums) 
        self.add(text_euler, text_rk2, text_rk4, text_verlet)

        # add springs and their respective iters
        spring_euler = ccs(euler_data[0,1:], y_euler+0.25)
        spring_rk2 = ccs(rk2_data[0,1:], y_rk2+0.25)
        spring_rk4 = ccs(rk4_data[0,1:], y_rk4+0.25)
        spring_verlet = ccs(verlet_data[0,1:], y_verlet+0.25)
        self.add(spring_euler, spring_rk2, spring_rk4, spring_verlet)

        spring_euler.iter = iter(euler_data[::5,1:])
        spring_rk2.iter = iter(rk2_data[::5,1:])
        spring_rk4.iter = iter(rk4_data[::5,1:])
        spring_verlet.iter = iter(verlet_data[::5,1:])

        spring_euler.y = y_euler+0.25
        spring_rk2.y = y_rk2+0.25
        spring_rk4.y = y_rk4+0.25
        spring_verlet.y = y_verlet+0.25
        

        # spring updater
        def spring_updater(spring):
            spring_pos = next(spring.iter)
            spring.become(ccs(spring_pos, spring.y))


        self.wait(1.5)
        timeline = ValueTracker(0)

        spring_euler.add_updater(spring_updater)
        spring_rk2.add_updater(spring_updater)
        spring_rk4.add_updater(spring_updater)
        spring_verlet.add_updater(spring_updater)

        self.play(timeline.animate.set_value(10), rate_func = linear, run_time = 25)
        self.wait(5)