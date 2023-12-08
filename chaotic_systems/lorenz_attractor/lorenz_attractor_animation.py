from manim import *


# global parameters
n_particles = 3
speed_numerical = 1


# processing data
numerical_data = np.loadtxt("data/lorenz_data.csv", delimiter = ",", skiprows = 1)

x1_array = numerical_data[:,1]
y1_array = numerical_data[:,2]
z1_array = numerical_data[:,3]

x2_array = numerical_data[:,4]
y2_array = numerical_data[:,5]
z2_array = numerical_data[:,6]

x3_array = numerical_data[:,7]
y3_array = numerical_data[:,8]
z3_array = numerical_data[:,9]

print(x1_array)


# # generating iters for each trajectoy and coordinate
x1_iter = iter(x1_array[::speed_numerical])
y1_iter = iter(y1_array[::speed_numerical])
z1_iter = iter(z1_array[::speed_numerical])

x2_iter = iter(x2_array[::speed_numerical])
y2_iter = iter(y2_array[::speed_numerical])
z2_iter = iter(z2_array[::speed_numerical])

x3_iter = iter(x3_array[::speed_numerical])
y3_iter = iter(y3_array[::speed_numerical])
z3_iter = iter(z3_array[::speed_numerical])


class lorenz_attractor_scene(ThreeDScene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        text_lorenz_attractor = Title(r"Lorenz Attractor", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 

        # 3D coordinate system
        CO3D = [0, 0, 0]
        CO3D_x_range = (-10, 10, 1)
        CO3D_y_range = (-10, 10, 1)
        CO3D_z_range = (0, 60, 1)
        ax = ThreeDAxes(
            x_range = CO3D_x_range, y_range = CO3D_y_range, z_range = CO3D_z_range,
            x_length = 8, y_length = 8, z_length = 5, axis_config = {'tip_length': 0.05, 'tip_width': 0.3}, 
            z_axis_config = {'color': WHITE},
            ).rotate(
                axis = [1, 0, 0], angle = 6*PI/4
                ).rotate(
                    axis = [0, 1, 0], angle = 5*PI/4
                    ).rotate(axis = [1, 0, 0], angle = PI/20).rotate(
                        axis = [0, 1, 0], angle = PI/20
                        ).set_opacity(0.2)
        

        # initialize trajectories
        traj1 = Dot(point = ax.c2p(x1_array[0], y1_array[0], z1_array[0]), radius = 0.02, color = WHITE).set_opacity(0.2)
        traj1.color = WHITE
        traj1.x_iter = x1_iter
        traj1.y_iter = y1_iter
        traj1.z_iter = z1_iter

        traj2 = Dot(point = ax.c2p(x2_array[0], y2_array[0], z2_array[0]), radius = 0.02, color = RED).set_opacity(0.2)
        traj2.color = RED
        traj2.x_iter = x2_iter
        traj2.y_iter = y2_iter
        traj2.z_iter = z2_iter

        traj3 = Dot(point = ax.c2p(x3_array[0], y3_array[0], z3_array[0]), radius = 0.02, color = BLUE).set_opacity(0.2)
        traj3.color = BLUE
        traj3.x_iter = x3_iter
        traj3.y_iter = y3_iter
        traj3.z_iter = z3_iter


        def traj_updater(traj):
            x = next(traj.x_iter)
            y = next(traj.y_iter)
            z = next(traj.z_iter)
            color = traj.color
            #self.add(Line(start = traj.get_center(), end = ax.c2p(x, y, z), stroke_width = 1, color = color).set_opacity(0.5))
            #traj.move_to([x, y, z])
            self.add(Dot(point = ax.c2p(x, y, z), radius = 0.02, color = color).set_opacity(0.2))

        
        self.add(text_lorenz_attractor, ax)
        # self.add(traj1, traj2, traj3)        
        # self.wait(1.5)
        # timeline = ValueTracker(0)

        # traj1.add_updater(traj_updater)
        # traj2.add_updater(traj_updater)
        # traj3.add_updater(traj_updater)

        # self.play(timeline.animate.set_value(5), rate_func = linear, run_time = 20)

        # traj1.remove_updater(traj_updater)
        # traj2.remove_updater(traj_updater)
        # traj3.remove_updater(traj_updater)

        # self.wait(5)

        for i in range(0, 1000000-1, 100):
            if i % 5000 == 0:
                print(f"Count: {i}\n")
            self.add(Line(start = ax.c2p(x1_array[i], y1_array[i], z1_array[i]), end = ax.c2p(x1_array[i+1], y1_array[i+1], z1_array[i+1]), stroke_width = 1, color = WHITE).set_opacity(0.5))
            # self.add(Line(start = ax.c2p(x2_array[i], y2_array[i], z2_array[i]), end = ax.c2p(x1_array[i+1], y1_array[i+1], z1_array[i+1]), stroke_width = 1, color = RED).set_opacity(0.5))
            # self.add(Line(start = ax.c2p(x3_array[i], y3_array[i], z3_array[i]), end = ax.c2p(x1_array[i+1], y1_array[i+1], z1_array[i+1]), stroke_width = 1, color = BLUE).set_opacity(0.5))