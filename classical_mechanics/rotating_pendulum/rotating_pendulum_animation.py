from manim import *


class RotatingPendulum(Mobject):
    def __init__(self, origin, R, **kwargs):
        super().__init__(**kwargs)
        self.origin = origin
        self.radius = R
        # self.length = l

        # rotating torus
        torus = Torus(major_radius = self.radius, minor_radius = 0.2, color = WHITE, fill_color = WHITE, resolution = (32, 32), checkerboard_colors = [WHITE, GREY]).move_to(self.origin)
        self.add(torus)


    # rotate the torus for a new given angle alpha
    def rotate_torus(self, alpha):
        return

    
    # draw rotating pendulum
    def get_pendulum(self, pendulum_origin, l, phi, theta, alpha):
        return



class rotating_pendulum_scene(ThreeDScene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC)

        # headline
        text_rotating_pendulum = Title(r"Rotating Pendulum", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 
        self.add(text_rotating_pendulum)


        # 3D coordinate system with spherical pendulum
        CO3D = [0, 0, 0]
        CO3D_x_range = (-4, 4, 1)
        CO3D_y_range = (-4, 4, 1)
        CO3D_z_range = (-10.25, 4, 1)
        ax = ThreeDAxes(
            x_range = CO3D_x_range, y_range = CO3D_y_range, z_range = CO3D_z_range,
            x_length = 8, y_length = 8, z_length = 5, axis_config = {'tip_length': 0.05, 'tip_width': 0.3}, 
            z_axis_config = {'color': WHITE},
            ).set_opacity(0.4)
        

        # rotating pendulum
        R = 1
        rotating_pendulum = RotatingPendulum(CO3D, R)
        rotating_pendulum_ax_group = Group(ax, rotating_pendulum).move_to(CO3D).rotate(
                axis = [1, 0, 0], angle = 6*PI/4
                ).rotate(
                    axis = [0, 1, 0], angle = 5*PI/4
                    ).rotate(axis = [1, 0, 0], angle = PI/20)

        self.add(rotating_pendulum, rotating_pendulum_ax_group)