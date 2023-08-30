from manim import *


# data processing
heat_data = np.loadtxt("data/heat_equation_data.csv", delimiter = ",", skiprows = 0)

x_array = heat_data[0,:]
heat_iter_list = []

# iter generation
for i in range(len(x_array)):
    heat_iter_list.append(iter(heat_data[1::10,i]))


class heat_equation_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC)


        # header
        # text_heat = Title(r"Heat Equation: $\partial_t T(x,t)=D\cdot\partial_x^2 T(x, t)$", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(RIGHT)
        text_heat = Title(r"Heat Equation", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(RIGHT)
        self.add(text_heat)

        # heat sources
        left_source = Circle(radius = 1.0, color = RED, fill_opacity = 0.5).move_to([-5.5, 0, -1])
        right_source = Circle(radius = 1.0, color = BLUE, fill_opacity = 0.5).move_to([5.5, 0, -1])
        self.add(left_source, right_source)

        # heating rode
        Rode = Rectangle(height = 0.75 + 0.02, width = 10 + 0.02, fill_color = WHITE, fill_opacity = 0.5, stroke_opacity = 1, stroke_color = WHITE)
        self.add(Rode)

        # initial heat elementes of the rode
        T_line_list = []
        for i, heat_iter in enumerate(heat_iter_list):
            T = next(heat_iter)
            if T > 0:
                T_line = Line(start = [(-0.5 + x_array[i]) * 10, -0.75/2, 0], end = [(-0.5 + x_array[i]) * 10, 0.75/2, 0], color = RED, stroke_opacity = T)
            else:
                T_line = Line(start = [(-0.5 + x_array[i]) * 10, -0.75/2, 0], end = [(-0.5 + x_array[i]) * 10, 0.75/2, 0], color = BLUE, stroke_opacity = T)
            T_line_list.append(T_line)
            self.add(T_line_list[i])

        # heat elements updater
        def T_updater(Rode):
            for i, heat_iter in enumerate(heat_iter_list):
                T = next(heat_iter)
                if T > 0:
                    T_line_list[i].become(Line(start = [(-0.5 + x_array[i]) * 10, -0.75/2, 0], end = [(-0.5 + x_array[i]) * 10, 0.75/2, 0], color = RED, stroke_opacity = T))
                else:
                    T_line_list[i].become(Line(start = [(-0.5 + x_array[i]) * 10, -0.75/2, 0], end = [(-0.5 + x_array[i]) * 10, 0.75/2, 0], color = BLUE, stroke_opacity = abs(T)))

        # adding dynamic
        time = ValueTracker(0)
        Rode.add_updater(T_updater)
        self.wait(1.5)
        self.play(time.animate.set_value(1), rate_func= linear, run_time = 19.5)
        Rode.remove_updater(T_updater)
        self.wait(5)
