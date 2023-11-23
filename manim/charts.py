import shutil
import numpy as np
import pandas as pd
from manim import *

RAM = '8GB'
METHOD = 'MPI'
DTYPE = 'enteros'
THREADS = '8-Threads'
PROCESSOR = 'AMD Ryzen 3 5300U with Radeon Graphics'
EXP = [6, 7, 8]
keys = [f'{EXP[0]} {METHOD}', f'{EXP[1]} {METHOD}', f'{EXP[2]} {METHOD}']
dt = 'int' if DTYPE == 'enteros' else 'float'
df = pd.read_csv(f'results/{PROCESSOR}_{THREADS}_{RAM}/data_{dt}.csv')
data = df[df['exponent'].isin(keys)]['time_mean'].to_numpy()

class chart(Scene):
    def construct(self):
        config["frame_width"] = 12
        config["frame_height"] = 8

        chart   = BarChart(
            values = np.zeros(len(data)),
            y_range=[0, round(max(data)+max(data)/8,2) , round(max(data)/4,2)],
            x_length=16,
            y_length=6,
            bar_width=0.8,
            bar_names=[2**EXP[0], 2**EXP[1], 2**EXP[2]],
            y_axis_config={"font_size": 24},
            x_axis_config={"font_size": 24},
        ).scale(0.7)
        x_label = chart.get_x_axis_label(
            'Matrix Size',
            edge=DOWN,
            direction=DOWN,
            buff=0.05
        ).scale(0.6)
        y_label = chart.get_y_axis_label(
            'Time (s)',
            edge=UP,
            direction=UP,
            buff=-1
        ).scale(0.6)
        gv = VGroup(chart, x_label, y_label).to_edge(DOWN)

        t_top        = Text(f'Comparación de las ejecuciones del algoritmo Fox con matrices de números {DTYPE}').scale_to_fit_width(config["frame_width"]).to_edge(UP)
        t_processor  = Tex(PROCESSOR)
        t_threads    = Tex(THREADS).next_to(t_processor, RIGHT)
        t_ram        = Tex(f'{RAM} DDR4 3200MHz').next_to(t_threads, RIGHT)
        architecture = VGroup(t_processor, t_threads, t_ram).scale(0.65).next_to(gv, UP, buff=1)
        meth = METHOD if METHOD == 'MPI' else 'sequential'
        t_method = Tex(f'Using {meth} method').scale(0.65).next_to(architecture, DOWN)

        self.play(Create(gv), Create(t_top), Create(architecture), Create(t_method))
        self.play(chart.animate.change_bar_values(data), run_time=1.5)
        self.play(Create(chart.get_bar_labels(font_size=30, color=WHITE))) 
        self.wait(3)

if __name__ == '__main__':

    with tempconfig({
            "quality": "medium_quality", 
            "media_dir": "manim/media",
        }):
        scene = chart()
        scene.render()
    with tempconfig({
            "quality": "medium_quality", 
            "media_dir": "manim/media",
            "save_last_frame": True,
        }):
        scene = chart()
        scene.render()
    
    shutil.move('manim/media/images/chart.png',        
                f'results/{PROCESSOR}_{THREADS}_{RAM}/{METHOD}-{dt}/{EXP[0]}-{EXP[-1]}-{dt}-{METHOD}-chart.png')
    shutil.move('manim/media/videos/720p30/chart.mp4', 
                f'results/{PROCESSOR}_{THREADS}_{RAM}/{METHOD}-{dt}/{EXP[0]}-{EXP[-1]}-{dt}-{METHOD}-chart.mp4')