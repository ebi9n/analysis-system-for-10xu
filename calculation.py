import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import setting
from plot_dist_color_map_control import plotDistColorMap
class Calculation:

    @staticmethod
    def get_sum_in_range(format_XRD_df,sum_range_min_twotheta, sum_range_max_twotheta):
        all_frame_num = len(formatted_XRD_df.columns)
        twotheta_arr = formatted_XRD_df.index
        min_twotheta_idx = np.abs(twotheta_arr - sum_range_min_twotheta).argmin()
        max_twotheta_idx = np.abs(twotheta_arr - sum_range_max_twotheta).argmin()
        sum_list = []
        for frame in range(all_frame_num):
            insty_arr = formatted_XRD_df.iloc[:,frame].values
            sum = np.sum(insty_arr[min_twotheta_idx:max_twotheta_idx])
            sum_list.append(sum)
        sum_arr = np.array(sum_list)
        return sum_arr

    @staticmethod
    def normalize_formatted_df(formatted_XRD_df,
                           quench_start_frame,
                           quench_end_frame):
        normalize_insty_series = formatted_XRD_df.iloc[:,quench_start_frame : quench_end_frame].sum(axis=1)
        normalized_formatted_df = formatted_XRD_df.div(normalize_insty_series,axis=0)
        return normalized_formatted_df
    
    @staticmethod
    def format_XRD_df(XRD_path):
        XRD_df = pd.read_csv(XRD_path,
                             header=None)
        formatted_XRD_df = XRD_df.set_index([0,1]).unstack()
        
        return formatted_XRD_df
    
    @staticmethod
    def calc_pressure(volume ,temperature, EoS):
        return EoS(volume,  temperature)
    @staticmethod
    def calc_pressure_each_column(volume_arr,all_complemented_temp_df,EoS):
        all_pressure_list = []
        for col in all_complemented_temp_df.columns:
            temp_arr = all_complemented_temp_df[col]
            pressure_arr = Calculation.calc_pressure(volume_arr,temp_arr,EoS)
            all_pressure_list.append(pressure_arr)
        
        result_df = pd.DataFrame(np.array(all_pressure_list).T,columns=all_complemented_temp_df.columns)
        existing_columns = result_df.columns
        new_columns = pd.MultiIndex.from_tuples([('pressure', col[0], col[1]) for col in existing_columns])
        result_df.columns = new_columns

        return result_df
    @staticmethod
    def get_all_result_df(volume_arr,all_complemented_temp_df,EoS):
        all_complemented_temp_df_copy = all_complemented_temp_df.copy()
        pressure_result_df = Calculation.calc_pressure_each_column(volume_arr,all_complemented_temp_df_copy,EoS)
        temp_existing_columns = all_complemented_temp_df_copy.columns
        new_temp_columns = pd.MultiIndex.from_tuples([('temperature', col[0], col[1]) for col in temp_existing_columns])
        all_complemented_temp_df_copy.columns = new_temp_columns
        volume_df = pd.DataFrame(volume_arr)
        all_result_df = pd.concat([pressure_result_df,all_complemented_temp_df_copy,volume_df],axis=1)
        renamed_df = all_result_df.rename(columns={0 : 'volume'})
        return renamed_df
    @staticmethod
    def calc_lattice_volume(XRD_filepath,
                            peak_seek_range_min= setting.PEAK_SEEK_RANGE_MIN,
                            peak_seek_range_max= setting.PEAK_SEEK_RANGE_MAX):
        # ピーク位置を探査
        formatted_XRD_df =Calculation.format_XRD_df(XRD_filepath)
        peak_pos_arr = Calculation.calc_peak_twotheta(formatted_XRD_df,
                                                 peak_seek_range_min,
                                                 peak_seek_range_max)
        
        # 物理法則から体積を計算
        a = Calculation.calc_cubic_a(peak_pos_arr)
        # 体積を返す
        volume_arr = a**3
        return volume_arr    
    @staticmethod
    def calc_peak_twotheta(formatted_XRD_df,
                           peak_seek_range_min,
                           peak_seek_range_max):
        twotheta_arr = np.array(formatted_XRD_df.index)
        insty_arr = np.array(formatted_XRD_df.values)

        nearest_range_min_idx = np.abs(twotheta_arr - peak_seek_range_min).argmin()
        nearest_range_max_idx = np.abs(twotheta_arr - peak_seek_range_max).argmin()
        peak_pos_list = [(twotheta_arr[nearest_range_min_idx:nearest_range_max_idx])[np.argmax(insty_arr[frame][nearest_range_min_idx:nearest_range_max_idx])] for frame in range(len(insty_arr[0]))]
        peak_pos_arr = np.array(peak_pos_list)
        return peak_pos_arr
    
    @staticmethod
    def calc_cubic_a(peak_twotheta_deg,
                     h=1,k=1,l=0,
                     wl=setting.XRAY_WAVELENGTH):
        peak_twotheta_rad = (peak_twotheta_deg/ 360) *2 *  np.pi
        a = np.sqrt(h**2 + k**2 + l**2) * wl/(2 * np.sin(peak_twotheta_rad/2) )
        return a
    
    @staticmethod
    def calc_cubic_volume(a):
        volume = a**3
        return volume

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
                        laser_diam=setting.INITIAL_LASER_DIAMETER,
                        heat_start_frame=setting.INITIAL_HEAT_START_FRAME,
                        heat_end_frame=setting.INITIAL_HEAT_END_FRAME):
        laser_radius_pixel = laser_diam / 2
        dist_df = pd.read_csv(dist_path)
        temp_df = plotDistColorMap.format_dist_df(dist_df)
        
        all_temp_df = Calculation.get_calculated_temp_df(temp_df,
                                        left_max_pixel,
                                        right_max_pixel,
                                        laser_radius_pixel,
                                        heat_start_frame,
                                        heat_end_frame)
        return all_temp_df

    @staticmethod
    def read_temp_df_from_csv(all_temp_path):
        df = pd.read_csv(all_temp_path)
        df = df.set_index(df.columns[0])
        
        df.columns = [['left','left','left','right','right','right'],
              ['mean','max','min','mean','max','min']
                                                    ]
        
        df = df[0:]
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df

    @staticmethod
    def get_calculated_temp_df(temp_df,
                    left_max_pixel,
                    right_max_pixel,
                    laser_radius_pixel,
                    heat_start_frame,
                    heat_end_frame):
        left_temp_df = temp_df.loc[:,left_max_pixel - laser_radius_pixel: left_max_pixel + laser_radius_pixel].replace(0,np.nan)
        right_temp_df = temp_df.loc[:,right_max_pixel - laser_radius_pixel : right_max_pixel + laser_radius_pixel].replace(0,np.nan)

        left_mean_temp_series = left_temp_df.mean(axis=1)
        left_max_temp_series = left_temp_df.max(axis=1)
        left_min_temp_series = left_temp_df.min(axis=1)

        right_mean_temp_series = right_temp_df.mean(axis=1)
        right_max_temp_series  = right_temp_df.max(axis=1)
        right_min_temp_series  = right_temp_df.min(axis=1)

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
        calculated_temp_df[0:heat_start_frame] = 300
        calculated_temp_df[heat_end_frame:] = 300

        return calculated_temp_df
    

    @staticmethod
    def complement_temp_series(temp_series,
                               formatted_XRD_df,
                               XRD_frame_per_ms = setting.XRD_FREQ,
                               temp_frame_per_ms =setting.TEMP_FREQ):
        complementary_list = []
        temp_timeline = np.arange(0,len(temp_series)) * temp_frame_per_ms / 1000
        XRD_insty_arr =  np.array(formatted_XRD_df.values)
        calc_frame_arr = np.arange(len(XRD_insty_arr[0]))

        for itr in calc_frame_arr:
            now_second = itr / (1000/XRD_frame_per_ms)
            print(f'\r ... now analyzing at {now_second}', end='')
            diff_XRD_btwn_temp = np.abs(now_second - temp_timeline)
            most_near_frame = np.argsort(diff_XRD_btwn_temp)[0]
            next_near_frame = np.argsort(diff_XRD_btwn_temp)[1]
            estimated_temp = (diff_XRD_btwn_temp[next_near_frame] * temp_series[most_near_frame] + diff_XRD_btwn_temp[most_near_frame] * temp_series[next_near_frame]) / temp_frame_per_ms * 1000

            complementary_list.append(estimated_temp)
        complementary_series = pd.Series(complementary_list)
        print(complementary_series)
        
        return complementary_series

    
    @staticmethod
    def get_all_complemented_temp_df(all_temp_df,
                                     formatted_XRD_df,
                                     XRD_frame_per_ms= setting.XRD_FREQ,
                                     temp_frame_per_ms= setting.TEMP_FREQ):
        left_mean_temp_series = all_temp_df['left']['mean']
        left_max_temp_series = all_temp_df['left']['max']
        left_min_temp_series = all_temp_df['left']['min']
        right_mean_temp_series = all_temp_df['right']['mean']
        right_max_temp_series = all_temp_df['right']['max']
        right_min_temp_series = all_temp_df['right']['min']

        mean_temp_series = (right_mean_temp_series + left_mean_temp_series)/2

        complemented_left_mean_series = Calculation.complement_temp_series(left_mean_temp_series,
                                                                           formatted_XRD_df,
                                                                           XRD_frame_per_ms=XRD_frame_per_ms,
                                                                           temp_frame_per_ms=temp_frame_per_ms)
        complemented_left_max_series = Calculation.complement_temp_series(left_max_temp_series,
                                                                           formatted_XRD_df,
                                                                           XRD_frame_per_ms=XRD_frame_per_ms,
                                                                           temp_frame_per_ms=temp_frame_per_ms)
        complemented_left_min_series = Calculation.complement_temp_series(left_min_temp_series,
                                                                           formatted_XRD_df,
                                                                           XRD_frame_per_ms=XRD_frame_per_ms,
                                                                           temp_frame_per_ms=temp_frame_per_ms)
        complemented_right_mean_series = Calculation.complement_temp_series(right_mean_temp_series,
                                                                           formatted_XRD_df,
                                                                           XRD_frame_per_ms=XRD_frame_per_ms,
                                                                           temp_frame_per_ms=temp_frame_per_ms)
        complemented_right_max_series = Calculation.complement_temp_series(right_max_temp_series,
                                                                           formatted_XRD_df,
                                                                           XRD_frame_per_ms=XRD_frame_per_ms,
                                                                           temp_frame_per_ms=temp_frame_per_ms)
        complemented_right_min_series = Calculation.complement_temp_series(right_min_temp_series,
                                                                           formatted_XRD_df,
                                                                           XRD_frame_per_ms=XRD_frame_per_ms,
                                                                           temp_frame_per_ms=temp_frame_per_ms)
        complemented_mean_series = Calculation.complement_temp_series(mean_temp_series,
                                                                        formatted_XRD_df,
                                                                        XRD_frame_per_ms=XRD_frame_per_ms,
                                                                        temp_frame_per_ms=temp_frame_per_ms)
        complement_all_arr = np.array([complemented_left_mean_series,
                                        complemented_left_max_series,
                                        complemented_left_min_series,
                                        complemented_right_mean_series,
                                        complemented_right_max_series,
                                        complemented_right_min_series,
                                        complemented_mean_series])
        
        all_complemented_temp_df = pd.DataFrame(complement_all_arr.T,
                                        columns= [['left','left','left','right','right','right','all'],
                                                    ['mean','max','min','mean','max','min','all']
                                                    ])
        
        return all_complemented_temp_df
                
if __name__ == '__main__':
    if False:
        print('-----calc start-----')
        dist_path = "model_data/rotated_(-4e-1)ERLAMBDAFeO06_  02(v3.0)_dist(20).csv"
        all_temp_df = Calculation.calc_temp_vs_frame(dist_path,
                                        left_max_pixel=131,
                                        right_max_pixel=381,
                                        laser_diam=setting.INITIAL_LASER_DIAMETER,
                                        heat_start_frame=45,
                                        heat_end_frame=85)
        fig = plt.figure(figsize=(9,4), dpi=150,facecolor='white')
        ax_right = fig.add_subplot(121)
        ax_left = fig.add_subplot(122)
        ax_right.plot(all_temp_df['left']['mean'])
        
        plt.show()
        all_temp_df.to_csv('test.csv')
    if True:
        XRD_path = 'model_data/XRD_test_input.csv'
        temp_path = 'model_data/rotated_(-4e-1)ERLAMBDAFeO06_  02(v3.0)_dist(20).csv'
        formatted_XRD_df = Calculation.format_XRD_df(XRD_path)
        all_temp_df = Calculation.calc_temp_vs_frame(temp_path,
                                                     heat_start_frame=46,
                                                     heat_end_frame=86,
                                                     right_max_pixel=131,
                                                     left_max_pixel=381)
        comp_all_temp_df = Calculation.get_all_complemented_temp_df(all_temp_df,
                                                                    formatted_XRD_df,
                                                                    XRD_frame_per_ms=10,
                                                                    temp_frame_per_ms=24.8)
        comp_all_temp_df.plot()
        plt.xlim(100,220)
        plt.ylim(0,4000)
        plt.show()
