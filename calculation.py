from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setting

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

if __name__ == '__main__':
    print('done')