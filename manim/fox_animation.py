from manim import *
import numpy as np

class Fox_Algorithm(Scene):
    def construct(self):
        SIZE = 4
        A_matrix_v = np.arange(1, SIZE**2 + 1).reshape((SIZE, SIZE))
        B_matrix_v = np.arange(SIZE**2+1, (SIZE**2)*2+1).reshape((SIZE, SIZE))
        C_matrix_v = np.zeros((4,4), dtype=int)

        A_matrix = Matrix(A_matrix_v)
        B_matrix = Matrix(B_matrix_v)
        C_matrix = Matrix(C_matrix_v)

        dot = MathTex('\\cdot')
        equals = MathTex('=')
        
        mobj_scale = A_matrix.width
        equation = VGroup(A_matrix, dot, B_matrix, equals, C_matrix).arrange(RIGHT)
        equation.scale_to_fit_width(config["frame_width"] - 2)
        equation.to_edge(LEFT)
        mobj_scale = A_matrix.width / mobj_scale 
        self.add(equation)

        A_fb = SurroundingRectangle(A_matrix.get_entries()[0], buff = .2, color = BLUE_C,   corner_radius=0.1)
        B_fb = SurroundingRectangle(B_matrix.get_rows()[0],    buff = .2, color = PURPLE_C, corner_radius=0.1)
        C_fb = SurroundingRectangle(C_matrix.get_rows()[0],    buff = .2, color = GREEN_C,  corner_radius=0.1)
        self.play(Create(A_fb), Create(B_fb), Create(C_fb), run_time=0.5)
    
        for r in range(0, SIZE): 
            for i in range(0, SIZE):
                c = (r + i) % SIZE
                C_matrix_v[i] += A_matrix_v[i, c] * B_matrix_v[c] 
                Dummy = Matrix(C_matrix_v)
                Dummy.scale(mobj_scale)
                Dummy.next_to(equals, RIGHT)

                A_fb_Dummy = SurroundingRectangle((A_matrix.get_entries()[i*SIZE + c]), buff = .2, color = BLUE_C,   corner_radius=0.1)
                B_fb_Dummy = SurroundingRectangle(B_matrix.get_rows()[c],               buff = .2, color = PURPLE_C, corner_radius=0.1)
                C_fb_Dummy = SurroundingRectangle(Dummy.get_rows()[i],                  buff = .2, color = GREEN_C,  corner_radius=0.1)
                self.play(Transform(A_fb, A_fb_Dummy), Transform(B_fb, B_fb_Dummy), Transform(C_fb, C_fb_Dummy))
                self.play(Transform(C_matrix, Dummy))
                self.wait(0.5)
                
        self.wait(2)