from manim import *


# ocean parameters
OCEAN_HEIGHT = 5000;                                # generel ocean depth
OCEAN_HEIGHT_RIFF = 20;                             # riff depth

OCEAN_X_LEFT = -1000;                               # left ocean border
OCEAN_X_RIGHT = 0;                                  # right ocean border
OCEAN_X_RIFF_LEFT = -700;                           # left riff border
OCEAN_X_BEACH_LEFT = -550;                          # left beach border
OCEAN_X_BEACH_RIGHT = -450;                         # right beach border
OCEAN_X_RIFF_RIGHT = -300;                          # right beach border


# riff profile
def height_ocean(x):
    if (OCEAN_X_LEFT <= x and x < OCEAN_X_RIFF_LEFT):
        return OCEAN_HEIGHT
    elif (OCEAN_X_RIFF_LEFT <= x and x < OCEAN_X_BEACH_LEFT):
        return OCEAN_HEIGHT + (OCEAN_HEIGHT_RIFF-OCEAN_HEIGHT) * (np.sin(PI/2 * (x-OCEAN_X_RIFF_LEFT) / (OCEAN_X_BEACH_LEFT-OCEAN_X_RIFF_LEFT)))**2
    elif (OCEAN_X_BEACH_LEFT <= x and x < OCEAN_X_BEACH_RIGHT):
        return OCEAN_HEIGHT_RIFF
    elif (OCEAN_X_BEACH_RIGHT <= x and x < OCEAN_X_RIFF_RIGHT):
        return OCEAN_HEIGHT_RIFF - (OCEAN_HEIGHT_RIFF-OCEAN_HEIGHT) * (np.sin(PI/2 * (OCEAN_X_BEACH_RIGHT-x) / (OCEAN_X_BEACH_RIGHT-OCEAN_X_RIFF_RIGHT)))**2
    elif (OCEAN_X_RIFF_RIGHT <= x and x < OCEAN_X_RIGHT):
        return OCEAN_HEIGHT
    else:
        return -5000
    

# data processing
riff_x_plot = np.linspace(OCEAN_X_LEFT, OCEAN_X_RIGHT-1, 1000)
riff_h_plot = np.array([5000 - height_ocean(riff_x_plot_i) for riff_x_plot_i in riff_x_plot]) 
tsunami_data = np.loadtxt("data/tsunami_data.csv", delimiter = ",", skiprows = 0)
x_ocean_array = tsunami_data[0,1:] / 1000
wave_iter_list = []

# iter generation
for i in range(1, len(x_ocean_array)+1):
    wave_iter_list.append(iter(tsunami_data[1::10,i]))


class tsunami_scene(Scene):
    def construct(self):
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC)

        # header
        text_heat = Tex(r"1D-d'Alembert-Gleichung: $\partial_t^2\xi(x, t)=u^2(x)\cdot\partial_x^2\xi(x, t)$", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.75 * RIGHT)
        self.add(text_heat)

        # riff: coordinate system
        x_riff_range = [OCEAN_X_LEFT, OCEAN_X_RIGHT, 50]
        y_riff_range = [0, OCEAN_HEIGHT, 1000]
        x_riff_length = 12
        y_riff_length = 1.25
        x_riff_dict = dict(zip(
            [OCEAN_X_LEFT, OCEAN_X_RIFF_LEFT, OCEAN_X_BEACH_LEFT, OCEAN_X_BEACH_RIGHT, OCEAN_X_RIFF_RIGHT, OCEAN_X_RIGHT], 
            [r"$x_\mathrm{L}$", r"$x_\mathrm{Riff,\,L}$", r"$x_\mathrm{Strand,\,L}$", r"$x_\mathrm{Strand,\,R}$", r"$x_\mathrm{Riff,\,R}$", r"$x_\mathrm{R}$"]))
        y_riff_dict = dict(zip([5000, 3000, 1000], [0, -2000, -4000]))
        npla_riff = NumberPlane(
            x_range = x_riff_range, y_range = y_riff_range, x_length = x_riff_length, y_length = y_riff_length,
            axis_config = {"include_numbers": False, "stroke_opacity": 0.25}, background_line_style = {"stroke_opacity": 0.25}, ).shift(2.25 * DOWN)
        ax_riff = Axes(
            x_range = x_riff_range, y_range = y_riff_range, x_length = x_riff_length, y_length = y_riff_length, 
            axis_config = {"stroke_width": 1, "stroke_opacity": 0.75}, tips = False).add_coordinates(x_riff_dict, y_riff_dict, font_size = 20).shift(2.25 * DOWN)
        line_graph_riff = ax_riff.plot_line_graph(x_values = riff_x_plot, y_values = riff_h_plot, line_color = GREY, add_vertex_dots = False, stroke_width = 2)
        riff_coordinate_system = VGroup(ax_riff, npla_riff, line_graph_riff)
        self.add(riff_coordinate_system)

        # wave: coordinate system
        x_wave_range = [OCEAN_X_LEFT, OCEAN_X_RIGHT, 50]
        y_wave_range = [-20, 20, 5]
        x_wave_length = 12
        y_wave_length = 3.5
        y_wave_dict = dict(zip([-20, -10, 10, 20], [-20, -10, 10, 20]))
        ax_wave = Axes(
            x_range = x_wave_range, y_range = y_wave_range, x_length = x_wave_length, y_length = y_wave_length, 
            axis_config = {"stroke_width": 1, "stroke_opacity": 0.75}, tips = False).add_coordinates([], y_wave_dict, font_size = 20).shift(0.725 * UP)
        wave_coordinate_system = VGroup(ax_wave)
        self.add(wave_coordinate_system)

        # riff lines
        x_riff_L_line = DashedLine(ax_riff.c2p(OCEAN_X_RIFF_LEFT, 0, 0), ax_wave.c2p(OCEAN_X_RIFF_LEFT, 20, 0), dash_length = 0.05, dashed_ratio = 0.75, color = WHITE, stroke_opacity = 0.5, stroke_width = 1)
        x_beach_L_line = DashedLine(ax_riff.c2p(OCEAN_X_BEACH_LEFT, 0, 0), ax_wave.c2p(OCEAN_X_BEACH_LEFT, 20, 0), dash_length = 0.05, dashed_ratio = 0.75, color = WHITE, stroke_opacity = 0.5, stroke_width = 1)
        x_beach_R_line = DashedLine(ax_riff.c2p(OCEAN_X_BEACH_RIGHT, 0, 0), ax_wave.c2p(OCEAN_X_BEACH_RIGHT, 20, 0), dash_length = 0.05, dashed_ratio = 0.75, color = WHITE, stroke_opacity = 0.5, stroke_width = 1)
        x_riff_R_line = DashedLine(ax_riff.c2p(OCEAN_X_RIFF_RIGHT, 0, 0), ax_wave.c2p(OCEAN_X_RIFF_RIGHT, 20, 0), dash_length = 0.05, dashed_ratio = 0.75, color = WHITE, stroke_opacity = 0.5, stroke_width = 1)
        self.add(x_riff_L_line, x_beach_L_line, x_beach_R_line, x_riff_R_line)

        # wave
        wave_line_list = []
        for i, wave_iter in enumerate(wave_iter_list):
            x_wave = x_ocean_array[i]
            y_wave = next(wave_iter)
            if y_wave > -OCEAN_HEIGHT_RIFF:
                wave_line = Line(start = ax_wave.c2p(x_wave, y_wave, 0), end = ax_wave.c2p(x_wave, -20, 0), color = BLUE, stroke_opacity = 0.3)
            wave_line_list.append(wave_line)
            self.add(wave_line_list[i])

        # wave updater
        def wave_updater(wave):
            for i, wave_iter in enumerate(wave_iter_list):
                x_wave = x_ocean_array[i]
                y_wave = next(wave_iter)
                if y_wave > -OCEAN_HEIGHT_RIFF:
                    wave_line = Line(start = ax_wave.c2p(x_wave, y_wave, 0), end = ax_wave.c2p(x_wave, -20, 0), color = BLUE, stroke_opacity = 0.3)
                wave_line_list[i].become(wave_line)

        # adding dynamic
        time = ValueTracker(0)
        ax_wave.add_updater(wave_updater)
        self.wait(0.5)
        self.play(time.animate.set_value(1), rate_func = linear, run_time = 29.5)