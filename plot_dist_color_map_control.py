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

class plotDistColorMap:
    """
    カラーマップのプロットを実施
    """
    def __init__(self):
        # change test
        """
        コンストラクタ
        """
        # figの作成
        self.fig = None
        self.filepath = None
        self.dist_df = None
        self.temp_df = None
        self.fig = plt.figure(figsize=FIGSIZE, dpi=DPI,facecolor=FACECOLOR)
        # 座標軸の作成
        self.ax_main = self.fig.add_subplot(211)
        self.ax_left = self.fig.add_subplot(223)
        self.ax_right = self.fig.add_subplot(224)

    def replot(self,
               filename=None,
               draw_min_frame = None,
               draw_max_frame = None,
               left_max_pixel = None,
               right_max_pixel = None,
               beam_diam_pixel = None):
        beam_radius_pixel = beam_diam_pixel / 2
        if filename is not None:
            self.filepath = filename
            self.dist_df = pd.read_csv(self.filepath)
        # フォーマットを実施
        self.temp_df = self.format_dist_df(self.dist_df)

        # 全体部分をプロットする
        sns.heatmap(self.temp_df,ax=self.ax_main)
        self.ax_main.set_ylim(draw_max_frame,draw_min_frame)

        # レーザー範囲の左側を描画
        self.ax_main.axvspan(left_max_pixel - beam_radius_pixel,
                             left_max_pixel + beam_radius_pixel,
                             color=LASER_RANGE_COLOR,
                             alpha=LASER_RANGE_ALPHA)
        
        # レーザー範囲の左側を描画
        self.ax_main.axvspan(right_max_pixel - beam_radius_pixel,
                             right_max_pixel + beam_radius_pixel,
                             color=LASER_RANGE_COLOR,
                             alpha=LASER_RANGE_ALPHA)
        
        # 左側のレーザー範囲近傍を描画
        sns.heatmap(self.temp_df,ax=self.ax_left)
        self.ax_left.set_ylim(draw_max_frame,draw_min_frame)
        self.ax_left.set_xlim(left_max_pixel - CLOSE_SHOW_DIST_PIXEL/2 ,left_max_pixel + CLOSE_SHOW_DIST_PIXEL/2)
        self.ax_left.axvspan(left_max_pixel - beam_radius_pixel,
                             left_max_pixel + beam_radius_pixel,
                             color=LASER_RANGE_COLOR,
                             alpha=LASER_RANGE_ALPHA)
        
        # 右側のレーザー範囲近傍を描画
        sns.heatmap(self.temp_df,ax=self.ax_right)
        self.ax_right.set_ylim(draw_max_frame,draw_min_frame)
        self.ax_right.set_xlim(right_max_pixel - CLOSE_SHOW_DIST_PIXEL/2 ,right_max_pixel + CLOSE_SHOW_DIST_PIXEL/2)
        self.ax_right.axvspan(right_max_pixel - beam_radius_pixel,
                              right_max_pixel + beam_radius_pixel,
                              color=LASER_RANGE_COLOR,
                              alpha=LASER_RANGE_ALPHA)
        return self.fig
    @classmethod
    def format_dist_df(cls,dist_df):
        temp_df = dist_df.drop(['ROI','Frame','Wavelength'], axis=1)
        temp_df =temp_df.set_index(['Row','Column']).unstack()
        temp_df.index.names = ['Frame']
        temp_df.columns.names = ['Intensity','pixel']
        temp_df = temp_df.T.reset_index(level=0,drop=True).T
        return temp_df
    
if __name__ == '__main__':
    # テストを実施
    filename = "model_data/rotated_(-4e-1)ERLAMBDAFeO06_  02(v3.0)_dist(20).csv"
    plot_dist_color_map = plotDistColorMap()
    plot_dist_color_map.replot(filename=filename,
                               draw_min_frame=60,
                               draw_max_frame=100,
                               left_max_pixel= 120,
                               right_max_pixel= 360,
                               beam_diam_pixel= 7.8125)
    plt.show()
