from manim import *


# data processing
nonlinear_map_data = np.loadtxt(f"data/nonlinear_map_data.csv", delimiter = ",", skiprows = 1)
nonlinear_map_long_x_data = np.loadtxt(f"data/nonlinear_map_long_x_data.csv", delimiter = ",", skiprows = 1)
nonlinear_map_long_k_data = np.loadtxt(f"data/nonlinear_map_long_k_data.csv", delimiter = ",", skiprows = 1)


# bifurcation data
mu_array = nonlinear_map_data[:,0]
x_n_array = nonlinear_map_data[:,1:]
x_n_bifurcation_array = nonlinear_map_data[:,30:]
n_array = np.array([i for i in range(len(x_n_array[0]))])


# long-term data
mu_long_array = nonlinear_map_long_x_data[:,0]
x_n_long_array = nonlinear_map_long_x_data[:,1:]
k_n_long_array = nonlinear_map_long_k_data[:,1:]
n_long_array = np.array([i for i in range(len(x_n_long_array[0]))])



class BifurcationDiagram(Mobject):
    def __init__(self, center, x_range, y_range, x_length, y_length, **kwargs):
        super().__init__(**kwargs)

        self.center = center
        self.x_range = x_range
        self.y_range = y_range
        self.x_length = x_length
        self.y_length = y_length

        x_coord = [0, 1, 2, 3, 4]
        y_coord = [0, 1]

        x_dict = dict(zip(x_coord, x_coord))
        y_dict = dict(zip(y_coord, y_coord))


        self.ax = Axes(
            x_range = self.x_range, y_range = self.y_range, x_length = self.x_length, y_length = self.y_length, axis_config = {"tip_width": 0.15, "tip_height": 0.15}
            ).add_coordinates(x_dict, y_dict).move_to(self.center)
        self.ax_xlabel = self.ax.get_x_axis_label(Tex(r"$\mu$", font_size = 28)).shift(0.1 *LEFT)
        self.ax_ylabel = self.ax.get_y_axis_label(Tex(r"long-term $x_n$", font_size = 28)).shift(0.15 * DOWN)
        self.add(self.ax, self.ax_xlabel, self.ax_ylabel)


    # draws the next pint
    def get_dot(self, x, y):
        dot_point = self.ax.c2p(x, y, 0)
        dot = Dot(dot_point, radius = 0.0075, color = BLUE, fill_color = BLUE, fill_opacity = 1)
        dot.point = dot_point
        return dot
    

    # returns a connector for given start and end point
    def get_line(self, point_prior, point):
        line = Line(start = point_prior, end = point, color = BLUE, stroke_opacity = 0.75, stroke_width = 1)
        return line
    

    # draw point for every long-term value in the array
    def get_long_xn(self, mu, x_n):
        dot_group = VGroup()
        for x_n_i in x_n:
            dot = self.get_dot(mu, x_n_i)
            dot_group.add(dot)
        return dot_group
    


class SpaceDiagram(Mobject):
    def __init__(self, center, x_range, y_range, x_length, y_length, x_label, y_label, space = "real", **kwargs):
        super().__init__(**kwargs)

        self.center = center
        self.x_range = x_range
        self.y_range = y_range
        self.x_length = x_length
        self.y_length = y_length

        # x_coord = [0, 1, 2, 3, 4]
        y_coord = [0, 1]

        # x_dict = dict(zip(x_coord, x_coord))
        y_dict = dict(zip(y_coord, y_coord))


        self.ax = NumberPlane(
            x_range = self.x_range, y_range = self.y_range, x_length = self.x_length, y_length = self.y_length, axis_config = {"tip_width": 0.15, "tip_height": 0.15},
            x_axis_config = {"stroke_opacity": 0.215}, y_axis_config = {"stroke_opacity": 0.125}, background_line_style = {"stroke_opacity": 0.125}
            ).move_to(self.center)
        # if space == "real":
        #     self.ax.y_axis.add_numbers(y_dict)
        if x_label:
            self.ax_xlabel = self.ax.get_x_axis_label(Tex(x_label, font_size = 28)).shift(0.1 *LEFT)
            self.add(self.ax_xlabel)
        if y_label:
            self.ax_ylabel = self.ax.get_y_axis_label(Tex(y_label, font_size = 28)).shift(0.15 * DOWN)
            self.add(self.ax_ylabel)
        self.add(self.ax)


    # makes a plot given n- and x_n-array
    def make_plot(self, x_array, y_array, plot_color):
        plot_group = VGroup()
        max_y = max(abs(y_array))
        if max_y > 2:
            y_array /= (max_y/2)
        for i in range(len(x_array)-1):
            point_prior = self.ax.c2p(x_array[i], y_array[i])
            point = self.ax.c2p(x_array[i+1], y_array[i+1])
            connector = Line(start = point_prior, end = point, color = plot_color, stroke_opacity = 0.75)
            plot_group.add(connector)
        return plot_group




class bifurcation_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        text_nonlinear_map = Title(r"Logistic Map: Bifurcation Diagram", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 
        self.add(text_nonlinear_map)

        diagram_center = np.array([0, -0.5, 0])
        x_range = [0, 4, 1]
        y_range = [0, 1, 0.2]
        x_length = 10
        y_length = 4.5

        bifurcation_diagram = BifurcationDiagram(center = diagram_center, x_range = x_range, y_range = y_range, x_length = x_length, y_length = y_length)
        bifurcation_dot = bifurcation_diagram.get_dot(0, 0)
        self.add(bifurcation_diagram, bifurcation_dot)


        # animation
        mu_edge_1 = 2.5
        mu_edge_2 = 3.5
        self.wait(1.5)
        for i, mu in enumerate(mu_array):
            new_mu = mu
            new_x_n = x_n_bifurcation_array[i]
            # replace dot
            # self.remove(bifurcation_dot)
            if mu < mu_edge_1:
                bifurcation_dot = bifurcation_diagram.get_long_xn(new_mu, new_x_n[-2:])
                self.add(bifurcation_dot)
                self.wait(0.02)
            elif mu < mu_edge_2:
                bifurcation_dot = bifurcation_diagram.get_long_xn(new_mu, new_x_n[-5:])
                self.add(bifurcation_dot)
                self.wait(0.05)
            else:
                bifurcation_dot = bifurcation_diagram.get_long_xn(new_mu, new_x_n)
                self.add(bifurcation_dot)
                self.wait(0.1)
        self.wait(5)



class nonlinear_map_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline
        text_nonlinear_map = Title(r"Logistic Map: Time and Frequency Domain", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT) 
        self.add(text_nonlinear_map)


        # real space diagram parameter
        rs_diagram_center = np.array([-3, -0.5, 0])
        rs_x_range = [0, 60, 10]
        rs_y_range = [0, 1, 0.2]
        rs_x_length = 5
        rs_y_length = 4.5
        rs_x_label = r"$n$"
        rs_y_label = r"$x_n$"

        # fourier space diagram parameter
        fs_diagram_center = np.array([3, -0.5, 0])
        fs_x_range = [0, 60, 10]
        fs_y_range = [-2, 2, 0.5]
        fs_x_length = 5
        fs_y_length = 4.5
        fs_x_label = r"$k$"
        fs_y_label = False

        real_space_diagram = SpaceDiagram(
            center = rs_diagram_center, x_range = rs_x_range, y_range = rs_y_range, x_length = rs_x_length, y_length = rs_y_length, x_label = rs_x_label, y_label = rs_y_label)
        fourier_space_diagram = SpaceDiagram(
            center = fs_diagram_center, x_range = fs_x_range, y_range = fs_y_range, x_length = fs_x_length, y_length = fs_y_length, x_label = fs_x_label, y_label = fs_y_label, space = "fourier")
        self.add(real_space_diagram, fourier_space_diagram)

        real_space_plot = real_space_diagram.make_plot(n_long_array, x_n_long_array[0], RED)
        fourier_space_plot = fourier_space_diagram.make_plot(n_long_array[1:], k_n_long_array[0,1:], BLUE)
        self.add(real_space_plot, fourier_space_plot)

        mu_text = Tex("$\mu={:.3f)}$".format(mu), color = WHITE, font_size = 36).move_to(np.array([0, 2.25, 0]))
        self.add(mu_text)


        # animation
        mu_edge_1 = 2.5
        mu_edge_2 = 3.5
        self.wait(1.5)
        for i, mu in enumerate(mu_array):
            self.remove(real_space_plot, fourier_space_plot, mu_text)
            real_space_plot = real_space_diagram.make_plot(n_long_array, x_n_long_array[i], RED)
            fourier_space_plot = fourier_space_diagram.make_plot(n_long_array[1:], k_n_long_array[i,1:], BLUE)
            mu_text = Tex("$\mu={:.3f)}$".format(mu), color = WHITE, font_size = 36).move_to(np.array([0, 2.25, 0]))
            self.add(real_space_plot, fourier_space_plot, mu_text)
            if mu < mu_edge_1:
                self.wait(0.02)
            elif mu < mu_edge_2:
                self.wait(0.05)
            else:
                self.wait(0.2)
        self.wait(5)