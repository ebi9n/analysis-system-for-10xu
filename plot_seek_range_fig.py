from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setting

FIGSIZE = setting.FIGSIZE
DPI = setting.DPI
FACECOLOR = setting.FACECOLOR
LASER_RANGE_COLOR = setting.LASER_RANGE_COLOR
LASER_RANGE_ALPHA = setting.LASER_RANGE_ALPHA
CLOSE_SHOW_DIST_PIXEL = setting.CLOSE_SHOW_DIST_PIXEL

class PlotSeekRangeFig:
    def __init__(self):
        # change test
        """
        コンストラクタ
        """
        # figの作成
        self.fig = None
        