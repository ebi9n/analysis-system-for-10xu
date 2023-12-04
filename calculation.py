from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setting
from plot_dist_color_map_control import plotDistColorMap
class Calculation:
    @staticmethod
    def get_max_pixel(calib_path,
                    left_min_pixel=setting.LEFT_RANGE_MIN,
                    left_max_pixel=setting.LEFT_RANGE_MAX,
                    right_min_pixel = setting.RIGHT_RANGE_MIN,
                    right_max_pixel = setting.RIGHT_RANGE_MAX):
        
        calib_DF = pd.read_csv(calib_path)
        # 各pixelの強度を足し合わせる
        insty_sum_per_pixel_series = calib_DF.groupby('Row')['Intensity'].sum()

        left_max_insty_pixel = insty_sum_per_pixel_series[left_min_pixel:left_max_pixel].idxmax()
        right_max_insty_pixel = insty_sum_per_pixel_series[right_min_pixel:right_max_pixel].idxmax()

        return left_max_insty_pixel, right_max_insty_pixel

    def calc_temp_vs_frame(dist_path,
                        left_max_pixel=setting.LEFT_MAX_PIXEL,
                        right_max_pixel=setting.RIGHT_MAX_PIXEL,
                        laser_diam=setting.INITIAL_LASER_DIAMETER):
        laser_radius_pixel = laser_diam / 2
        dist_df = pd.read_csv(dist_path)
        temp_df = plotDistColorMap.format_dist_df(dist_df)
        
        
        all_temp_df = Calculation.get_calculated_temp_df(temp_df,
                                        left_max_pixel,
                                        right_max_pixel,
                                        laser_radius_pixel)
        return all_temp_df
        

    @staticmethod
    def get_calculated_temp_df(temp_df,
                    left_max_pixel,
                    right_max_pixel,
                    laser_radius_pixel):
        left_temp_df = temp_df.loc[:,left_max_pixel - laser_radius_pixel: left_max_pixel + laser_radius_pixel]
        right_temp_df = temp_df.loc[:,right_max_pixel - laser_radius_pixel : right_max_pixel + laser_radius_pixel]

        left_mean_temp_series = left_temp_df.mean(axis=1).replace(np.nan,300)
        left_max_temp_series = left_temp_df.max(axis=1).replace(np.nan,300)
        left_min_temp_series = left_temp_df.min(axis=1).replace(np.nan,300)

        right_mean_temp_series = right_temp_df.mean(axis=1).replace(np.nan,300)
        right_max_temp_series  = right_temp_df.max(axis=1).replace(np.nan,300)
        right_min_temp_series  = right_temp_df.min(axis=1).replace(np.nan,300)

        temp_meanmaxmin_arr = np.array([left_mean_temp_series,
                                        left_max_temp_series,
                                        left_min_temp_series,
                                        right_mean_temp_series,
                                        right_max_temp_series,
                                        right_min_temp_series])
        calculated_temp_df = pd.DataFrame(temp_meanmaxmin_arr.T,
                                        columns= [['left','left','left','right','right','right'],
                                                    ['mean','max','min','mean','max','min']
                                                    ])
        return calculated_temp_df

if __name__ == '__main__':
    print('-----calc start-----')
    dist_path = "model_data/rotated_(-4e-1)ERLAMBDAFeO06_  02(v3.0)_dist(20).csv"
    all_temp_df = Calculation.calc_temp_vs_frame(dist_path,
                                     left_max_pixel=131,
                                     right_max_pixel=381,
                                     laser_diam=setting.INITIAL_LASER_DIAMETER)
    fig = plt.figure(figsize=(9,4), dpi=150,facecolor='white')
    ax_right = fig.add_subplot(121)
    ax_left = fig.add_subplot(122)
    ax_right.plot(all_temp_df['left']['mean'])
    
    plt.show()
    all_temp_df.to_csv('test.csv')
