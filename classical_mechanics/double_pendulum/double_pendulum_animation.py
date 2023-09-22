from manim import *


# global parameters
m1 = 1
m2 = 1
L = 1.5
speed_numerical = 15
speed_analytical = 3


# processing data
numerical_data = np.loadtxt("data/double_pendulum_numerical_data.csv", delimiter = ",", skiprows = 1)
analytical_data = np.loadtxt("data/double_pendulum_analytical_data.csv", delimiter = ",", skiprows = 1)

theta1_numerical = numerical_data[:,1]
theta2_numerical = numerical_data[:,3]
theta1_v_numerical = numerical_data[:,2]
theta1_v_numerical = numerical_data[:,4]

theta1_analytical = analytical_data[:,1]
theta2_analytical = analytical_data[:,3]
theta1_v_analytical = analytical_data[:,2]
theta1_v_analytical = analytical_data[:,4]


# iter for all angels
theta1_numerical_iter = iter(theta1_numerical[::speed_numerical])
theta2_numerical_iter = iter(theta2_numerical[::speed_numerical])
theta1_analytical_iter = iter(theta1_analytical[::speed_analytical])
theta2_analytical_iter = iter(theta2_analytical[::speed_analytical])


# calculates relative position of mass for given 'theta'
def theta_to_coord(theta):
    return L * np.array([np.sin(theta), -np.cos(theta), 0])


# returns a double pendulum at 'origin' for given angels and color
def make_double_pendulum(origin, theta1, theta2, color):
    pendulum_stroke_opacity = 0.75
    pendulum_stroke_width = 5

    m1_coord = origin + theta_to_coord(theta1)
    m2_coord = m1_coord + theta_to_coord(theta2)
    line1 = Line(origin, m1_coord, stroke_opacity = pendulum_stroke_opacity, stroke_width = pendulum_stroke_width, color = color)
    line2 = Line(m1_coord, m2_coord, stroke_opacity = pendulum_stroke_opacity - 0.375, stroke_width = pendulum_stroke_width, color = color)
    anchor = Dot(origin, color = WHITE, radius = 0.035)
    mass1 = Dot(m1_coord, color = WHITE, radius = 0.035)
    mass2 = Dot(m2_coord, color = WHITE, radius = 0.035)
    return VGroup(line1, line2, anchor, mass1, mass2)


class double_pendulum_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        text_double_pendulum = Title(r"Double Pendulum", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 

        # coordinates of the anchor points 
        numerical_origin = np.array([-3, 1, 0])
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


        self.add(text_double_pendulum, text_numerical, text_analytical, numerical_anchor, analytical_anchor)
        self.add(numerical_pendulum, analytical_pendulum)
        self.wait(1.5)
        timeline = ValueTracker(0)
        numerical_pendulum.add_updater(numerical_pendulum_updater)
        analytical_pendulum.add_updater(analytical_pendulum_updater)
        self.play(timeline.animate.set_value(10), rate_func = linear, run_time = 30)
        numerical_pendulum.remove_updater(numerical_pendulum_updater)
        analytical_pendulum.remove_updater(analytical_pendulum_updater)
        self.wait(5)
