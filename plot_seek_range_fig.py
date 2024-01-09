import numpy as np
import matplotlib.pyplot as plt
import setting
from calculation import Calculation
FIGSIZE = setting.FIGSIZE
DPI = setting.DPI
FACECOLOR = setting.FACECOLOR
LASER_RANGE_COLOR = setting.LASER_RANGE_COLOR
LASER_RANGE_ALPHA = setting.LASER_RANGE_ALPHA
CLOSE_SHOW_DIST_PIXEL = setting.CLOSE_SHOW_DIST_PIXEL
FREQ_SHOW_FRAME = setting.FREQ_SHOW_FRAME
class PlotSeekRangeFig:
    def __init__(self):
        # change test
        """
        コンストラクタ
        """
        # figの作成
        self.fig = plt.figure(figsize=FIGSIZE, dpi=DPI,facecolor=FACECOLOR)
        self.ax = self.fig.add_subplot(111)
        self.XRD_filepath = None
    def get_seek_range_fig(self,
                           XRD_filepath = None,
                           peak_seek_range_min=setting.PEAK_SEEK_RANGE_MIN,
                           peak_seek_range_max=setting.PEAK_SEEK_RANGE_MAX):
        
        if XRD_filepath:
            formatted_XRD_df = Calculation.format_XRD_df(XRD_filepath)
        twotheta_arr = np.array(formatted_XRD_df.index)
        
        for frame in range(0,len(formatted_XRD_df.columns),FREQ_SHOW_FRAME):
            insty_arr = formatted_XRD_df.iloc[:,frame]
            self.ax.plot(twotheta_arr,insty_arr,label=f'{frame}')
        y_min, y_max = self.ax.get_ylim()  # 現在の軸のy軸範囲を取得
        self.ax.fill_between(x=[peak_seek_range_min, peak_seek_range_max], 
                         y1=y_min, y2=y_max, 
                         color='gray', alpha=0.5)  # 指定された範囲を塗りつぶす
        self.ax.legend(loc='best')
        self.ax.set_xlabel('2 theta (deg)')
        self.ax.set_ylabel('Intensity')
        self.ax.set_xlim(xmin=np.max([0,peak_seek_range_min-2]),xmax=np.min([20,peak_seek_range_max+2]))
        return self.fig

if __name__ == '__main__':
    plot_seek_range_fig = PlotSeekRangeFig()
    fig = plot_seek_range_fig.get_seek_range_fig(XRD_filepath='model_data/XRD_test_input.csv',
                                           peak_seek_range_min=9,
                                           peak_seek_range_max=10)
    plt.show()