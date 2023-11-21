from manim import *
import charts
import pandas as pd
import numpy as np

PROCESSOR = 'AMD Ryzen 5 3600 6-Core Processor'
RAM = '16GB'
DTYPE = 'int'

df = pd.read_csv(f'src/{PROCESSOR}_{RAM}.csv')

# with tempconfig({"quality": "medium_quality", "preview": True}):
#     scene = charts()
#     scene.render()