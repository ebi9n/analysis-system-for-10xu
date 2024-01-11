from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setting
from calculation import Calculation
FIGSIZE = setting.FIGSIZE
DPI = setting.DPI
FACECOLOR = setting.FACECOLOR
LASER_RANGE_COLOR = setting.LASER_RANGE_COLOR
LASER_RANGE_ALPHA = setting.LASER_RANGE_ALPHA
CLOSE_SHOW_DIST_PIXEL = setting.CLOSE_SHOW_DIST_PIXEL
FREQ_SHOW_FRAME = setting.FREQ_SHOW_FRAME
class PlotPhaseDiagram:
    def __init__(self):
        # change test
        """
        コンストラクタ
        """
        # figの作成
        self.fig = plt.figure(figsize=FIGSIZE, dpi=DPI,facecolor=FACECOLOR)
        self.ax = self.fig.add_subplot(111)
    def get_phase_diagram(self,
                         result_df=None):
        temp_result_index = ('temperature','all','all')
        pressure_result_index =('pressure','all','all')
        temp_arr = result_df[temp_result_index]
        pressure_arr = result_df[pressure_result_index]
        self.ax.scatter(pressure_arr,temp_arr)
        self.ax.set_ylabel('Temperature (K)')
        self.ax.set_xlabel('Preesure (GPa)')
        return self.fig