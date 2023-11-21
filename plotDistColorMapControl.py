from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

FIGSIZE = (10,10)
DPI = 100
FACECOLOR = "white"
class plotDistColorMapControl:
    """
    カラーマップのプロットを実施
    """
    def __init__(self):
        """
        コンストラクタ
        """
        # figの作成
        self.fig = plt.figure(figsize=FIGSIZE, dpi=DPI,facecolor=FACECOLOR)
        # 座標軸の作成
        self.ax_main = self.fig.add_subplot(211)
        self.ax_up = self.fig.add_subplot(223)
        self.ax_down = self.fig.add_subplot(224)
        self.filepath = None
        self.dist_df = None
        self.temp_df = None
    def replot(self,
               filename=None,
               draw_min_frame = None,
               draw_max_frame = None):
        if filename is not None:
            self.filepath = filename
            self.dist_df = pd.read_csv(self.filepath)
        
        # 描画が重ならないように一度消去
        self.ax_main.clear()
        
        # フォーマットを実施
        self.temp_df = self.format_dist_df(self.dist_df)

        # 全体部分をプロットする
        
        sns.heatmap(self.temp_df,ax=self.ax_main)
        self.ax_main.set_ylim(draw_min_frame,draw_max_frame)
        self.fig.savefig("test2.png")
        
    @classmethod
    def format_dist_df(cls,dist_df):
        temp_df = dist_df.drop(['ROI','Frame','Wavelength'], axis=1)
        temp_df =temp_df.set_index(['Row','Column']).unstack()
        temp_df.index.names = ['Frame']
        temp_df.columns.names = ['Intensity','pixel']
        temp_df = temp_df.T.reset_index(level=0,drop=True).T
        return temp_df
    
if __name__ == '__main__':
    filename = "model_data/rotated_(-4e-1)ERLAMBDAFeO06_  02(v3.0)_dist(20).csv"
    plot_dist_color_map = plotDistColorMapControl()
    plot_dist_color_map.replot(filename=filename,draw_min_frame=100,draw_max_frame=200)

