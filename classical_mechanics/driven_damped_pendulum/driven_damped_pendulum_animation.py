from manim import *


# processing data
pendulum_data = np.loadtxt("data/driven_damped_pendulum_2_1_data.csv", delimiter = ",", skiprows = 1)

time = pendulum_data[:,0]
theta = pendulum_data[:,1]
theta_v = pendulum_data[:,2]


# iter for pendulum and phase space
animation_speed = 5

theta_iter = iter(theta[::animation_speed])
theta_v_iter = iter(theta_v[::animation_speed])

theta_ps_iter = iter(theta[::animation_speed])
theta_v_ps_iter = iter(theta_v[::animation_speed])



# phase space class
class PhaseSpace(Mobject):
    def __init__(self, center, phase_array, side_length = 3, stroke_width = 1, labels = 0, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.side_length = side_length
        self.stroke_with = stroke_width
        self.phi_array = phase_array[0]
        self.r_array = phase_array[1]

        square = Square(side_length = side_length, stroke_width = stroke_width, stroke_color = WHITE, **kwargs).move_to(center)
        self.pax = PolarPlane(radius_max = max(abs((self.r_array))) * 1.1, size = self.side_length).move_to(self.center)
        self.add(square)

        if labels:
            x_label = Tex(labels[0], color = RED, font_size = 156 / self.side_length).next_to(square, DOWN)
            xdot_label = Tex(labels[1], color = RED, font_size = 156 / self.side_length).next_to(square, LEFT)
            self.add(x_label, xdot_label)


    # method to return the position in phase space for given x and y
    def c2p(self, phi, r):
        # phase_space_dot = Dot(ax.c2p(x, y, 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75)
        # phase_space_dot.state = np.array([x, y])
        # return phase_space_dot
        # return self.ax.c2p(x, y, 0)
        return self.pax.pr2pt(r, phi)
    


# driven pendulum class
class DrivenPendulum(Mobject):
    def __init__(self, center, radius, **kwargs):
        super().__init__(**kwargs)
        self.center = center
        self.radius = radius


    # method to rotate the pendulum according to the given angle
    def get_pendulum(self, theta):
        # inner pendulum
        pendulum_center = Circle(radius = 0.075*self.radius, color = BLACK, fill_color = BLACK, fill_opacity = 1, stroke_opacity = 0.5).move_to(self.center)
        pendulum_top_connector = Line(start = self.center, end = self.center + 0.925*self.radius*UP, color = WHITE, stroke_width = 20*self.radius)
        pendulum_left_connector = Line(start = self.center, end = self.center + 0.925*self.radius*UP, color = WHITE, stroke_width = 20*self.radius).rotate(about_point = self.center, angle = 2/3*PI)
        pendulum_right_connector = Line(start = self.center, end = self.center + 0.925*self.radius*UP, color = WHITE, stroke_width = 20*self.radius).rotate(about_point = self.center, angle = -2/3*PI)
        # self.add(pendulum_top_connector, pendulum_left_connector, pendulum_right_connector, pendulum_center)

        # outer pendulum
        pendulum_circle = Circle(radius = 0.925*self.radius, color = WHITE, stroke_width = 10*self.radius).move_to(self.center)
        pendulum_outer_circle = Circle(radius = self.radius, color = LIGHT_GRAY).move_to(self.center)
        pendulum_inner_circle = Circle(radius = 0.85*self.radius, color = LIGHT_GRAY).move_to(self.center)
        # self.add(pendulum_circle, pendulum_outer_circle, pendulum_inner_circle)

        # rotate all components according to theta
        pendulum_group = VGroup(pendulum_top_connector, pendulum_left_connector, pendulum_right_connector, pendulum_center, pendulum_circle, pendulum_outer_circle, pendulum_inner_circle)
        modulo_theta = theta % (2*PI)
        pendulum_group.rotate(about_point = self.center, angle = modulo_theta)
        return pendulum_group


    # method to return the motor
    def get_motor(self, A, omega, t):
        return



class driven_damped_pendulum_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        text_double_pendulum = Title(r"Driven Damped Pendulum", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 
        self.add(text_double_pendulum)


        # parameters
        pendulum_center = np.array([-3, -0.25, 0])
        pendulum_radius = 2
        rotated_pendulum_theta = next(theta_iter)

        phase_space_center = np.array([3, -0.25, 0])
        phase_space_side_length = 3.75
        phase_space_theta = next(theta_ps_iter) % (2*PI)
        phase_space_theta_v = next(theta_v_ps_iter)


        # pendulum
        pendulum = DrivenPendulum(pendulum_center, pendulum_radius)
        rotated_pendulum = pendulum.get_pendulum(rotated_pendulum_theta)
        rotated_pendulum.iter = theta_iter
        rotated_pendulum.getter = pendulum.get_pendulum
        self.add(pendulum, rotated_pendulum)

        # phase space
        phase_space = PhaseSpace(center = phase_space_center, phase_array = (np.array([0, 2*PI]), theta_v), side_length = phase_space_side_length, labels = (r'$\theta$, $\dot{\theta}$ (polar)', ''))
        # phase_space_dot = phase_space.get_dot(phase_space_theta, phase_space_theta_v)
        phase_space_dot = Dot(phase_space.c2p(phase_space_theta, phase_space_theta_v), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75)
        phase_space_dot.pos_getter = phase_space.c2p
        phase_space_dot.theta_iter = theta_ps_iter
        phase_space_dot.theta_v_iter = theta_v_ps_iter
        self.add(phase_space, phase_space_dot)


        # pendulum updater
        def pendulum_updater(pendulum):
            theta = next(pendulum.iter)
            pendulum.become(pendulum.getter(theta))


        # phase space updater
        def phase_space_updater(dot):
            # theta_old = dot.state[0]
            # theta_v_old = dot.state[1]
            theta_new = next(dot.theta_iter) % (2*PI)
            theta_v_new = next(dot.theta_v_iter)
            # new_dot = dot.getter(theta_new, theta_v_new)
            new_dot_pos = dot.pos_getter(theta_new, theta_v_new)
            self.add(Line(start = dot.get_center(), end = new_dot_pos, stroke_width = 1, color = RED).set_opacity(0.75))
            dot.move_to(new_dot_pos)


        self.wait(1.5)
        timeline = ValueTracker(0)

        rotated_pendulum.add_updater(pendulum_updater)
        phase_space_dot.add_updater(phase_space_updater)

        self.play(timeline.animate.set_value(10), rate_func = linear, run_time = 25)
        self.wait(5)