from manim import *
import numpy as np

class Fox_Algorithm(Scene):
    def construct(self):
        config["frame_width"] = 14
        config["frame_height"] = 6

        TITLE = Text("Fox Algorithm", color=WHITE).scale(1.5)
        TITLE.to_edge(UP)
        self.add(TITLE)

        SIZE = 4
        A_matrix_v = np.arange(1, SIZE**2 + 1).reshape((SIZE, SIZE))
        B_matrix_v = np.arange(SIZE**2+1, (SIZE**2)*2+1).reshape((SIZE, SIZE))
        C_matrix_v = np.zeros((4,4), dtype=int)
        A_matrix = Matrix(A_matrix_v)
        B_matrix = Matrix(B_matrix_v)
        C_matrix = Matrix(C_matrix_v)
        mobj_scale = A_matrix.width

        times = MathTex('\\times')
        equals = MathTex('=')
        equation = VGroup(A_matrix, times, B_matrix, equals, C_matrix).arrange(RIGHT)
        equation.scale_to_fit_width(config["frame_width"] - 1.5)
        equation.to_edge(LEFT)
        self.add(equation)
        mobj_scale = A_matrix.width / mobj_scale 

        A_fb = SurroundingRectangle(
            A_matrix.get_entries()[0],
            buff = .2,
            color = BLUE_C,
            corner_radius=0.1)

        B_fb = SurroundingRectangle(
            B_matrix.get_rows()[0],
            buff = .2,
            color = PURPLE_C,
            corner_radius=0.1)
        
        self.wait(1)
    
        for r in range(0, SIZE): 
            for i in range(0, SIZE):
                #* Calculation of the algorithm
                c = (r + i) % SIZE
                C_matrix_v[i] += A_matrix_v[i, c] * B_matrix_v[c] 

                #* Animation of the algorithm
                Dummy = Matrix(C_matrix_v)
                Dummy.scale(mobj_scale)
                Dummy.next_to(equals, RIGHT)

                A_fb_Dummy = SurroundingRectangle(
                    A_matrix.get_entries()[i*SIZE + c],
                    buff = .2, 
                    color = BLUE_C,
                    corner_radius=0.1)

                B_fb_Dummy = SurroundingRectangle(
                    B_matrix.get_rows()[c],
                    buff = .2, 
                    color = PURPLE_C,
                    corner_radius=0.1)

                C_fb_Dummy = SurroundingRectangle(
                    Dummy.get_rows()[i],
                    buff = .2, 
                    color = GREEN_C,
                    corner_radius=0.1)
                
                if i == 0 and r == 0: 
                    C_fb = SurroundingRectangle(
                    Dummy.get_rows()[0],
                    buff = .2,
                    color = GREEN_C,
                    corner_radius=0.1)
                    self.play(
                        Transform(C_matrix, Dummy, run_time=2), 
                        Create(A_fb), 
                        Create(B_fb), 
                        Create(C_fb))
                else:
                    self.play(
                        Transform(C_matrix, Dummy, run_time=2),
                        Transform(A_fb, A_fb_Dummy),
                        Transform(B_fb, B_fb_Dummy),
                        Transform(C_fb, C_fb_Dummy))
                
                self.wait(0.5)
                
        self.wait(2)