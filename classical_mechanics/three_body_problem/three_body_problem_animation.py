from manim import *


TBP_2D_data = np.loadtxt("data/ThreeBody_2D_data.csv", delimiter = ",", skiprows = 1)
# TBP_2D_data = np.loadtxt("data/A1a_Argon_Positions.csv", delimiter = ",", skiprows = 1)
TBP_3D_data = np.loadtxt("data/ThreeBody_3D_data.csv", delimiter = ",", skiprows = 1)

r1_2D = TBP_2D_data[:,1:4]
r2_2D = TBP_2D_data[:,4:7]
r3_2D = TBP_2D_data[:,7:10]

r1_3D = TBP_3D_data[:,1:4]
r2_3D = TBP_3D_data[:,4:7]
r3_3D = TBP_3D_data[:,7:10]


# provide paramters
framerate = 60
run_time = 30
sun_speed = 100
fade_length = 50
tail = False


# main 2D animation
class three_body_problem_scene(Scene):
    def construct(self):
        timeline = ValueTracker(0)
        CVC = Text('CVC', font_size = 12, weight = BOLD, color = WHITE, font = 'Latin Modern Sans').align_on_border(RIGHT + DOWN, buff = 0.2)
        self.add(CVC) 

        # headline and vectorfeld
        text_TBP = Title("The 3-Body-Problem", font_size = 48).align_on_border(UP + LEFT, buff = 0.5).shift(0.5 * RIGHT)  

        # creation of the 3 suns
        sun1 = VGroup(Circle(color = WHITE, radius = 0.1, fill_color = WHITE, fill_opacity = 0.5))
        sun2 = VGroup(Circle(color = RED, radius = 0.1, fill_color = RED, fill_opacity = 0.5))
        sun3 = VGroup(Circle(color = YELLOW, radius = 0.1, fill_color = YELLOW, fill_opacity = 0.5))

        # position iters of the 3 suns
        sun1.iter = iter(r1_2D[::sun_speed,])
        sun2.iter = iter(r2_2D[::sun_speed,])
        sun3.iter = iter(r3_2D[::sun_speed,])

        # updater of the suns positions
        def sun_updater(sun):
            sun.move_to(next(sun.iter))

        # tail updater
        def dot1_fadeout_updater(dot1):
            if dot1.counter != fade_length and dot1.counter != 1:
                dot1.fill_opacity -= 1/fade_length
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1                
            elif dot1.counter == fade_length:
                dot1.move_to(sun1.get_center())
                dot1.fill_opacity = 1
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1
            else:
                dot1.counter = fade_length
                dot1.fill_opacity = 1

        def dot2_fadeout_updater(dot2):
            if dot2.counter != fade_length and dot2.counter != 1:
                dot2.fill_opacity -= 1/fade_length
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1                
            elif dot2.counter == fade_length:
                dot2.move_to(sun2.get_center())
                dot2.fill_opacity = 1
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1
            else:
                dot2.counter = fade_length
                dot2.fill_opacity = 1           

        def dot3_fadeout_updater(dot3):
            if dot3.counter != fade_length and dot3.counter != 1:
                dot3.fill_opacity -= 1/fade_length
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            elif dot3.counter == fade_length:
                dot3.move_to(sun3.get_center())
                dot3.fill_opacity = 1
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            else:
                dot3.counter = fade_length
                dot3.fill_opacity = 1

        # adding the tail
        for i in range(fade_length):
            dot1 = Dot(radius = 0.05, fill_color = WHITE, fill_opacity = 0.5)
            dot1.counter = fade_length + i
            dot1.fill_opacity = 0
            dot1.set_opacity(dot1.fill_opacity)
            self.add(dot1)
            dot1.add_updater(dot1_fadeout_updater)

            dot2 = Dot(radius = 0.05, fill_color = RED, fill_opacity = 0.5)
            dot2.counter = fade_length + i
            dot2.fill_opacity = 0
            dot2.set_opacity(dot2.fill_opacity)
            self.add(dot2)
            dot2.add_updater(dot2_fadeout_updater)

            dot3 = Dot(radius = 0.05, fill_color = YELLOW, fill_opacity = 0.5)
            dot3.counter = fade_length + i
            dot3.fill_opacity = 0
            dot3.set_opacity(dot3.fill_opacity)
            self.add(dot3)
            dot3.add_updater(dot3_fadeout_updater)


        # initial sun positions
        sun1.move_to(r1_2D[0,:])
        sun2.move_to(r2_2D[0,:])
        sun3.move_to(r3_2D[0,:])

        # adding the suns
        self.add(sun1, sun2, sun3)
        self.add(text_TBP)
        self.wait(1.5)
        #self.play(Unwrite(text_TBP), run_time = 3)

        # adding the updater
        sun1.add_updater(sun_updater)
        sun2.add_updater(sun_updater)
        sun3.add_updater(sun_updater)

        # timeline as ValueTracker
        self.play(timeline.animate.set_value(5), rate_func= linear, run_time = run_time)
        sun1.remove_updater(sun_updater)
        sun2.remove_updater(sun_updater)
        sun3.remove_updater(sun_updater)
        self.wait(5)


# 3D animation
class TBP_main_3D(ThreeDScene):
    def construct(self):
        timeline = ValueTracker(0)
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        axes = ThreeDAxes()

        # creation of the 3 suns
        sun1 = VGroup(Sphere(radius = 0.15, resolution = (16, 16)).set_color(WHITE))
        sun2 = VGroup(Sphere(radius = 0.15, resolution = (16, 16)).set_color(RED))
        sun3 = VGroup(Sphere(radius = 0.15, resolution = (16, 16)).set_color(YELLOW))

        # position iters of the 3 suns
        sun1.iter = iter(r1_3D[::sun_speed,])
        sun2.iter = iter(r2_3D[::sun_speed,])
        sun3.iter = iter(r3_3D[::sun_speed,])

        # updater of the sun positions
        def sun_updater(sun):
            sun.move_to(next(sun.iter))

        # tail updater
        def dot1_fadeout_updater(dot1):
            if dot1.counter != fade_length and dot1.counter != 1:
                dot1.fill_opacity -= 1/fade_length
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1                
            elif dot1.counter == fade_length:
                dot1.move_to(sun1.get_center())
                dot1.fill_opacity = 1
                dot1.set_opacity(dot1.fill_opacity)
                dot1.counter -= 1
            else:
                dot1.counter = fade_length
                dot1.fill_opacity = 1

        def dot2_fadeout_updater(dot2):
            if dot2.counter != fade_length and dot2.counter != 1:
                dot2.fill_opacity -= 1/fade_length
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1                
            elif dot2.counter == fade_length:
                dot2.move_to(sun2.get_center())
                dot2.fill_opacity = 1
                dot2.set_opacity(dot2.fill_opacity)
                dot2.counter -= 1
            else:
                dot2.counter = fade_length
                dot2.fill_opacity = 1           

        def dot3_fadeout_updater(dot3):
            if dot3.counter != fade_length and dot3.counter != 1:
                dot3.fill_opacity -= 1/fade_length
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            elif dot3.counter == fade_length:
                dot3.move_to(sun3.get_center())
                dot3.fill_opacity = 1
                dot3.set_opacity(dot3.fill_opacity)
                dot3.counter -= 1
            else:
                dot3.counter = fade_length
                dot3.fill_opacity = 1

        # adding the tails
        if tail:
            for i in range(fade_length):
                dot1 = Dot3D(radius = 0.05).set_color(WHITE)
                dot1.counter = fade_length + i
                dot1.fill_opacity = 0
                dot1.set_opacity(dot1.fill_opacity)
                self.add(dot1)
                dot1.add_updater(dot1_fadeout_updater)

                dot2 = Dot3D(radius = 0.05).set_color(RED)
                dot2.counter = fade_length + i
                dot2.fill_opacity = 0
                dot2.set_opacity(dot2.fill_opacity)
                self.add(dot2)
                dot2.add_updater(dot2_fadeout_updater)

                dot3 = Dot3D(radius = 0.05).set_color(YELLOW)
                dot3.counter = fade_length + i
                dot3.fill_opacity = 0
                dot3.set_opacity(dot3.fill_opacity)
                self.add(dot3)
                dot3.add_updater(dot3_fadeout_updater)
        
        # adding the suns
        self.add(axes, sun1, sun2, sun3)

        sun1.move_to(r1_3D[0,:])
        sun2.move_to(r2_3D[0,:])
        sun3.move_to(r3_3D[0,:])
        
        self.begin_ambient_camera_rotation(rate = 0.15)

        # adding the updaters
        sun1.add_updater(sun_updater)
        sun2.add_updater(sun_updater)
        sun3.add_updater(sun_updater)

        # timeline as ValueTracker
        self.play(timeline.animate.set_value(5), rate_func= linear, run_time = run_time)