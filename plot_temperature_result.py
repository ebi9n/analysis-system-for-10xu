from plot_dist_color_map_control import plotDistColorMap
from calculation import Calculation
import setting
import matplotlib.pyplot as plt

FIGSIZE = setting.TEMP_VS_FRAME_FIGSIZE
DPI = setting.DPI
FACECOLOR = setting.FACECOLOR

class PlotTempResult:
    def __init__(self):
        self.all_temp_df = None
        self.fig = plt.figure(figsize=FIGSIZE, dpi=DPI,facecolor=FACECOLOR)
        self.ax_right = self.fig.add_subplot(121)
        self.ax_left = self.fig.add_subplot(122)
        
    def replot(self,
               dist_filepath=None,
               left_max_pixel=setting.LEFT_MAX_PIXEL,
               right_max_pixel=setting.RIGHT_MAX_PIXEL,
               laser_diam=setting.INITIAL_LASER_DIAMETER,
               heat_start_frame=setting.INITIAL_HEAT_START_FRAME,
               heat_end_frame=setting.INITIAL_HEAT_END_FRAME):
        
        self.all_temp_df = Calculation.calc_temp_vs_frame(dist_path=dist_filepath,
                                                          left_max_pixel=left_max_pixel,
                                                          right_max_pixel=right_max_pixel,
                                                          laser_diam=laser_diam,
                                                          heat_start_frame=heat_start_frame,
                                                          heat_end_frame=heat_end_frame)

        self.ax_left.plot(self.all_temp_df['left']['mean'],label='mean')
        self.ax_left.plot(self.all_temp_df['left']['max'],label='max')
        self.ax_left.plot(self.all_temp_df['left']['min'],label='min')
        self.ax_left.set_xlabel('Frame')
        self.ax_left.set_ylabel('Temperature (K)')
        self.ax_left.legend()
        
        self.ax_right.plot(self.all_temp_df['right']['mean'],label='mean')
        self.ax_right.plot(self.all_temp_df['right']['max'],label='max')
        self.ax_right.plot(self.all_temp_df['right']['min'],label='min')
        self.ax_right.set_xlabel('Frame')
        self.ax_right.set_ylabel('Temperature (K)')
        self.ax_right.legend()
        return self.fig
        
if __name__ =='__main__':
    print('!TEST!')
    dist_filepath = 'model_data/rotated_(-4e-1)ERLAMBDAFeO06_  02(v3.0)_dist(20).csv'
    plot_temp_result = PlotTempResult()
    figure = plot_temp_result.replot(dist_filepath,
                                     left_max_pixel=131,
                                     right_max_pixel=381)
    plt.show()
