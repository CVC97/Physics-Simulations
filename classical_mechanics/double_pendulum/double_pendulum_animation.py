from manim import *


# global parameters
m1 = 1
m2 = 1
L = 1.75
speed_numerical = 15
speed_analytical = 3


# processing data
numerical_data = np.loadtxt("data/double_pendulum_numerical_data.csv", delimiter = ",", skiprows = 1)
analytical_data = np.loadtxt("data/double_pendulum_analytical_data.csv", delimiter = ",", skiprows = 1)

theta1_numerical = numerical_data[:,1]
theta2_numerical = numerical_data[:,3]
theta1_v_numerical = numerical_data[:,2]
theta2_v_numerical = numerical_data[:,4]

theta1_analytical = analytical_data[:,1]
theta2_analytical = analytical_data[:,3]
theta1_v_analytical = analytical_data[:,2]
theta2_v_analytical = analytical_data[:,4]


# iter for all angels
theta1_numerical_iter = iter(theta1_numerical[::speed_numerical])
theta2_numerical_iter = iter(theta2_numerical[::speed_numerical])
theta1_analytical_iter = iter(theta1_analytical[::speed_analytical])
theta2_analytical_iter = iter(theta2_analytical[::speed_analytical])

# iter for the phase space
theta1_numerical_ps_iter = iter(theta1_numerical[::speed_numerical])
theta2_numerical_ps_iter = iter(theta2_numerical[::speed_numerical])
theta1_v_numerical_ps_iter = iter(theta1_v_numerical[::speed_numerical])
theta2_v_numerical_ps_iter = iter(theta2_v_numerical[::speed_numerical])


# calculates relative position of mass for given 'theta'
def theta_to_coord(theta):
    return L * np.array([np.sin(theta), -np.cos(theta), 0])


# returns a double pendulum at 'origin' for given angels and color
def make_double_pendulum(origin, theta1, theta2, color):
    pendulum_stroke_opacity = 0.75
    pendulum_stroke_width = 7.5

    m1_coord = origin + theta_to_coord(theta1)
    m2_coord = m1_coord + theta_to_coord(theta2)
    line1 = Line(origin, m1_coord, stroke_opacity = pendulum_stroke_opacity, stroke_width = pendulum_stroke_width, color = color)
    line2 = Line(m1_coord, m2_coord, stroke_opacity = pendulum_stroke_opacity - 0.375, stroke_width = pendulum_stroke_width, color = color)
    anchor = Dot(origin, color = WHITE, radius = 0.05)
    mass1 = Dot(m1_coord, color = WHITE, radius = 0.05)
    mass2 = Dot(m2_coord, color = WHITE, radius = 0.05)
    return VGroup(line1, line2, anchor, mass1, mass2)


# phase space class
class PhaseSpace(Mobject):
    def __init__(self, center, phase_array, side_length = 3, stroke_width = 1, labels = 0, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.side_length = side_length
        self.stroke_with = stroke_width
        self.x_array = phase_array[0]
        self.xdot_array = phase_array[1]
        self.x_inc = (max(self.x_array) - min(self.x_array)) / 10
        self.xdot_inc = (max(self.xdot_array) - min(self.xdot_array)) / 10

        square = Square(side_length = side_length, stroke_width = stroke_width, stroke_color = WHITE, **kwargs).move_to(center)
        self.add(square)

        if labels:
            x_label = Tex(labels[0], color = WHITE, font_size = 156 / self.side_length).next_to(square, DOWN)
            xdot_label = Tex(labels[1], color = WHITE, font_size = 156 / self.side_length).next_to(square, LEFT)
            self.add(x_label, xdot_label)


    def c2p(self, x, y, z):
        ax = Axes(x_range = [min(self.x_array) - self.x_inc, max(self.x_array) + self.x_inc, 1], 
                  y_range = [min(self.xdot_array) - self.xdot_inc, max(self.xdot_array) + self.xdot_inc, 1], 
                  x_length = self.side_length, 
                  y_length = self.side_length).move_to(self.center)
        return ax.c2p(x, y, z)


class double_pendulum_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        text_double_pendulum = Title(r"Double Pendulum", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 

        # coordinates of the anchor points 
        numerical_origin = np.array([-3.25, 1.5, 0])
        analytical_origin = np.array([3, 1, 0])

        text_numerical = Tex(r'(a) numerical:', font_size = 32, color = RED).move_to(numerical_origin).shift(1 * UP)
        text_analytical = Tex(r'(b) analytical:', font_size = 32, color = BLUE).move_to(analytical_origin).shift(1 * UP)


        # pendulums
        numerical_anchor = Line(numerical_origin - np.array([0.5, 0, 0]), numerical_origin + np.array([0.5, 0, 0]), color = WHITE, stroke_width = 5)
        analytical_anchor = Line(analytical_origin - np.array([0.5, 0, 0]), analytical_origin + np.array([0.5, 0, 0]), color = WHITE, stroke_width = 5)

        numerical_pendulum = make_double_pendulum(numerical_origin, theta1_numerical[0], theta2_numerical[0], color = RED)
        analytical_pendulum = make_double_pendulum(analytical_origin, theta1_analytical[0], theta2_analytical[0], color = BLUE)


        def numerical_pendulum_updater(pendulum):
            theta1 = next(theta1_numerical_iter)
            theta2 = next(theta2_numerical_iter)
            pendulum.become(make_double_pendulum(numerical_origin, theta1, theta2, RED))


        def analytical_pendulum_updater(pendulum):
            theta1 = next(theta1_analytical_iter)
            theta2 = next(theta2_analytical_iter)
            pendulum.become(make_double_pendulum(analytical_origin, theta1, theta2, BLUE))


        # phase space
        phase_space = PhaseSpace(center = [3.25, -0.25, 0], phase_array = (np.concatenate((theta1_numerical, theta2_numerical)), np.concatenate((theta1_v_numerical, theta2_v_numerical))), 
            side_length = 3.75, labels = (r'$\varphi$', r'$\dot{\varphi}$'))
        

        # points in phase space
        theta1_dot = Dot(phase_space.c2p(theta1_numerical[0], theta1_v_numerical[0], 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75)
        theta2_dot = Dot(phase_space.c2p(theta2_numerical[0], theta2_v_numerical[0], 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75 - 0.375)


        def theta1_dot_updater(dot):
            theta1 = next(theta1_numerical_ps_iter)
            theta1_v = next(theta1_v_numerical_ps_iter)
            self.add(Line(start = dot.get_center(), end = phase_space.c2p(theta1, theta1_v, 0), stroke_width = 1, color = RED).set_opacity(0.75))
            dot.become(Dot(phase_space.c2p(theta1, theta1_v, 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75))


        def theta2_dot_updater(dot):
            theta2 = next(theta2_numerical_ps_iter)
            theta2_v = next(theta2_v_numerical_ps_iter)
            self.add(Line(start = dot.get_center(), end = phase_space.c2p(theta2, theta2_v, 0), stroke_width = 1, color = RED).set_opacity(0.75 - 0.375))
            dot.become(Dot(phase_space.c2p(theta2, theta2_v, 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75 - 0.375))


        self.add(text_double_pendulum, numerical_anchor, phase_space)#, text_numerical, text_analytical, analytical_anchor)
        self.add(numerical_pendulum, theta1_dot, theta2_dot)#, analytical_pendulum)
        self.wait(1.5)
        timeline = ValueTracker(0)
        numerical_pendulum.add_updater(numerical_pendulum_updater)
        #analytical_pendulum.add_updater(analytical_pendulum_updater)
        theta1_dot.add_updater(theta1_dot_updater)
        theta2_dot.add_updater(theta2_dot_updater)
        self.play(timeline.animate.set_value(10), rate_func = linear, run_time = 25)
        numerical_pendulum.remove_updater(numerical_pendulum_updater)
        #analytical_pendulum.remove_updater(analytical_pendulum_updater)
        theta1_dot.remove_updater(theta1_dot_updater)
        theta2_dot.remove_updater(theta2_dot_updater)
        self.wait(5)
