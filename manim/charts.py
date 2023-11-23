import os
import shutil
import numpy as np
import pandas as pd
from manim import *

class chart(Scene):
    def construct(self):
        config["frame_width"] = 12
        config["frame_height"] = 8

        max_v = max(data)
        chart = BarChart(
            values = np.zeros(len(data)),
            y_range=[0, round(max_v + max_v/8,2), round(max_v/4,2)],
            x_length=16,
            y_length=6,
            bar_width=0.8,
            bar_names=[2**exp for exp in EXP],
            y_axis_config={"font_size": 24},
            x_axis_config={"font_size": 24},
        ).scale(0.7)
        x_label = chart.get_x_axis_label(
            'Matrix Size',
            edge=DOWN,
            direction=DOWN,
            buff=0.05
        ).scale(0.6)
        y_l = 'Time (s)' if MEASURE == 'time_mean' else 'Memory (MB)'
        y_label = chart.get_y_axis_label(
            y_l,
            edge=UP,
            direction=UP,
            buff=-1
        ).scale(0.6).rotate(PI/2).next_to(chart, LEFT)
        gv = VGroup(chart, x_label, y_label).to_edge(DOWN)

        dt           = 'enteros' if DTYPE == 'int' else 'flotantes'
        meth         = METHOD if METHOD == 'MPI' else 'secuencial'
        Title        = f'Comparación de la memoria RAM utilizada por el algoritmo Fox con matrices de números {dt} usando el método {meth}' if MEASURE == 'memory_mean' else f'Comparación del tiempo de ejecución del algoritmo Fox con matrices de números {dt} usando el método {meth}'
        t_top        = Tex(Title).scale(0.75).to_edge(UP)
        architecture = Tex(f'{PROCESSOR} {THREADS} {RAM} DDR4 3200MHz', color='purple_a').scale(0.6).next_to(t_top, DOWN)

        self.play(Create(gv), Create(t_top), Create(architecture))
        self.play(chart.animate.change_bar_values(data), run_time=1.5)
        self.play(Create(chart.get_bar_labels(font_size=30, color=WHITE))) 
        self.wait(3)

if __name__ == '__main__':

    RAM = '8GB'
    DTYPES = ['int', 'float']
    METHODS = ['MPI', 'SEC']
    THREADS = '4-Threads'
    PROCESSOR = 'AMD Ryzen 3 5300U with Radeon Graphics'
    EXPS = [[6, 7, 8], [9, 10, 11, 12]]
    MEASURE = 'memory_mean'
    for DTYPE in DTYPES:
        df = pd.read_csv(f'results/{PROCESSOR}_{THREADS}_{RAM}/data_{DTYPE}.csv')
        for METHOD in METHODS:
            for EXP in EXPS:
                keys = [f'{exp} {METHOD}' for exp in EXP]
                data = df[df['exponent'].isin(keys)][MEASURE].to_numpy()
                data = data/1024 if MEASURE == 'memory_mean' else data
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
    
                path = f'results/{PROCESSOR}_{THREADS}_{RAM}/{METHOD}-{DTYPE}'
                file = f'{EXP[0]}-{EXP[-1]}-{DTYPE}-{METHOD}-chart'
                if not os.path.exists(path):
                    os.makedirs(path)
                shutil.move('manim/media/images/chart.png',        
                            f'{path}/{file}.png')
                shutil.move('manim/media/videos/720p30/chart.mp4', 
                            f'{path}/{file}.mp4')