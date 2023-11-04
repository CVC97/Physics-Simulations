from manim import *


# processing data
numerical_data = np.loadtxt("data/spherical_pendulum_data.csv", delimiter = ",", skiprows = 1)
speed_numerical = 30

length = numerical_data[:,1]
phi = numerical_data[:,2]
phi_dot = numerical_data[:,3]
theta = numerical_data[:,4]
theta_dot = numerical_data[:,5]


# iter for all angels
length_iter = iter(length[::speed_numerical])
phi_iter = iter(phi[::speed_numerical])
theta_iter = iter(theta[::speed_numerical])

# iter for the phase space
phi_ps_iter = iter(phi[::speed_numerical])
theta_ps_iter = iter(theta[::speed_numerical])
phi_dot_ps_iter = iter(phi_dot[::speed_numerical])
theta_dot_ps_iter = iter(theta_dot[::speed_numerical])



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
            x_label[0][0:1].set_color(RED)
            x_label[0][2:3].set_color(BLUE)
            xdot_label = Tex(labels[1], color = WHITE, font_size = 156 / self.side_length).next_to(square, LEFT)
            xdot_label[0][0:2].set_color(RED)
            xdot_label[0][3:5].set_color(BLUE)
            self.add(x_label, xdot_label)


    def c2p(self, x, y, z):
        ax = Axes(x_range = [min(self.x_array) - self.x_inc, max(self.x_array) + self.x_inc, 1], 
                  y_range = [min(self.xdot_array) - self.xdot_inc, max(self.xdot_array) + self.xdot_inc, 1], 
                  x_length = self.side_length, 
                  y_length = self.side_length).move_to(self.center)
        return ax.c2p(x, y, z)


class spherical_pendulum_scene(ThreeDScene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC)

        # headline
        text_spherical_pendulum = Title(r"Spherical Pendulum of Variable Length", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 


        # 3D coordinate system with spherical pendulum
        CO3D = [-5, -0.5, -8]
        CO3D_x_range = (-4, 4, 1)
        CO3D_y_range = (-4, 4, 1)
        CO3D_z_range = (0, 10.25, 1)
        ax = ThreeDAxes(
            x_range = CO3D_x_range, y_range = CO3D_y_range, z_range = CO3D_z_range,
            x_length = 8, y_length = 8, z_length = 5, axis_config = {'tip_length': 0.05, 'tip_width': 0.3}, 
            z_axis_config = {'color': WHITE},
            ).set_opacity(0.125)
    
        # spherical pendulum anchor
        prism_x = Prism(dimensions = [2, 0.125, 0.125], fill_color = WHITE, stroke_color = GREY).set_opacity(0.75).move_to(ax.c2p(0, 0, 10))
        prism_y = Prism(dimensions = [0.125, 2, 0.125], fill_color = WHITE, stroke_color = GREY).set_opacity(0.75).move_to(ax.c2p(0, 0, 10))
        cylinder = Cylinder(radius = 0.4, height = 0.5, color = WHITE, fill_color = WHITE, resolution = (24, 24), checkerboard_colors = [WHITE, GREY]).move_to(ax.c2p(0, 0, 10))
        spherical_pendulum_ax_group = VGroup(ax, cylinder).move_to(CO3D).rotate(
                axis = [1, 0, 0], angle = 6*PI/4
                ).rotate(
                    axis = [0, 1, 0], angle = 5*PI/4
                    ).rotate(axis = [1, 0, 0], angle = PI/20).rotate(
                        axis = [0, 1, 0], angle = PI/20
                        )
        

        # creates the pendulum in ax
        def create_pendulum(r, phi, theta):
            pendulum_group = VGroup()
            ball_size = 0.2
            x = r * np.cos(phi) * np.sin(theta)
            y = r * np.sin(phi) * np.sin(theta)
            z = r * np.cos(theta) + 10
            line = Line3D(start = np.array(ax.c2p(0, 0, 10)), end = np.array(ax.c2p(x, y, z)), color = WHITE, thickness = 0.005)
            sphere = Dot3D(point = ax.c2p(x, y, z), radius = ball_size, resolution = (20, 20),).set_color(RED)
            pendulum_group.add(line, sphere)

            # shadow
            # for i in range(11):
            #     radius = i / 10 * ball_size 
            #     pendulum_group.add(ax.plot_parametric_curve(lambda phi: np.array([radius*np.cos(phi), radius*np.sin(phi), z]), t_range = [0, 2*PI], stroke_opacity = 0.5, color = GREY).move_to(ax.c2p(x, y, 0)))
            pendulum_group.add(ax.plot_parametric_curve(lambda phi: np.array([0.1*np.cos(phi), 0.1*np.sin(phi), z]), t_range = [0, 2*PI], stroke_opacity = 0.5, color = GREY).move_to(ax.c2p(x, y, 0)))
            return pendulum_group


        pendulum = create_pendulum(length[0], phi[0], theta[0])


        # updates pendulum
        def pendulum_updater(pendulum):
            length = next(length_iter)
            phi = next(phi_iter)
            theta = next(theta_iter)
            pendulum.become(create_pendulum(length, phi, theta))



        # phase space
        phase_space = PhaseSpace(center = [3.25, -0.25, 0], phase_array = ([0, 2*PI], np.concatenate((phi_dot, theta_dot))), 
            side_length = 3.75, labels = (r'$\varphi\,/\,\vartheta$', r'$\dot{\varphi}\,/\,\dot{\vartheta}$'))
        

        # points in phase space
        phi_phase_space = Dot(phase_space.c2p(phi[0], phi_dot[0], 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75)
        theta_phase_space = Dot(phase_space.c2p(theta[0], theta_dot[0], 0), radius = 0.05, color = BLUE, fill_color = BLUE, fill_opacity = 0.75)


        def phi_ps_updater(dot):
            phi = next(phi_ps_iter)
            phi_dot = next(phi_dot_ps_iter)
            self.add(Line(start = dot.get_center(), end = phase_space.c2p(phi % (2*PI), phi_dot, 0), stroke_width = 1, color = RED).set_opacity(0.75))
            dot.become(Dot(phase_space.c2p(phi, phi_dot, 0), radius = 0.05, color = RED, fill_color = RED, fill_opacity = 0.75))


        def theta_ps_updater(dot):
            theta = next(theta_ps_iter)
            theta_dot = next(theta_dot_ps_iter)
            self.add(Line(start = dot.get_center(), end = phase_space.c2p(theta, theta_dot, 0), stroke_width = 1, color = BLUE).set_opacity(0.75))
            dot.become(Dot(phase_space.c2p(theta, theta_dot, 0), radius = 0.05, color = BLUE, fill_color = BLUE, fill_opacity = 0.75))


        self.add(text_spherical_pendulum)
        self.add(spherical_pendulum_ax_group, phase_space)
        self.add(pendulum, phi_phase_space, theta_phase_space)
        
        self.wait(1.5)
        timeline = ValueTracker(0)
        pendulum.add_updater(pendulum_updater)
        phi_phase_space.add_updater(phi_ps_updater)
        theta_phase_space.add_updater(theta_ps_updater)
        self.play(timeline.animate.set_value(5), rate_func = linear, run_time = 20)
        pendulum.remove_updater(pendulum_updater)
        phi_phase_space.remove_updater(phi_ps_updater)
        theta_phase_space.remove_updater(theta_ps_updater)
        self.wait(5)