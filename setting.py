
import numpy as np

"""
ソフトウェアの見た目に関する設定
"""
WINDOW_TITLE = "HLA" 
WINDOW_SIZE = "600x800"

"""
プロットに関する設定
"""
import matplotlib.pyplot as plt
plt.rcParams['ytick.major.width'] = 0.2#y軸主目盛り線の線幅
plt.rcParams['font.size'] = 5 #フォントの大きさ
plt.rcParams['axes.linewidth'] = 0.2# 軸の線幅edge linewidth
FIGSIZE = (5,5)
TEMP_VS_FRAME_FIGSIZE = (5,4) # 500* 300になる
DPI = 100
FACECOLOR = "white"
LASER_RANGE_COLOR = "white"
LASER_RANGE_ALPHA = 0.50
CLOSE_SHOW_DIST_PIXEL = 30

"""
calib fileから最大pixelを取得するとき
"""
LEFT_RANGE_MIN = 100
LEFT_RANGE_MAX = 200

RIGHT_RANGE_MIN = 300
RIGHT_RANGE_MAX = 400

"""
最大pixelの初期値
"""
LEFT_MAX_PIXEL = 150
RIGHT_MAX_PIXEL = 360
"""

実験条件に関する設定
ここの値が描画の初期値となる
"""
INITIAL_HEAT_START_FRAME = 0
INITIAL_HEAT_END_FRAME = 150
INITIAL_LASER_DIAMETER = float(7.8125)

"""
KClのピーク探査に関する初期設定
"""
PEAK_SEEK_RANGE_MIN = 10.5
PEAK_SEEK_RANGE_MAX = 11.5
XRAY_WAVELENGTH = 0.414506 # [Å]
FREQ_SHOW_FRAME = 50

"""
測定頻度を保管する処理の初期設定 ms / Frame
"""
XRD_FREQ = 10
TEMP_FREQ = 1/40.3 * 1000

"""
EoSの入力
"""
class EoS:
        @staticmethod
        def KCl_EoS_Dewaele2020(volume, temperature):
            V0 = 54.5 # [A3]
            K0 = 17.2 # [GPa]
            K0_dash = 5.82 
            aKT = 0.00224 # [GPa/K]
            eta = volume/V0
            first_item = 3 * K0 * eta **(-2/3) * (1 - eta **(1/3)) * np.exp(3/2 * (K0_dash - 1)*(1 - eta **(1/3)))
            second_item = aKT * (temperature - 300)
            pressure = first_item + second_item
            return pressure
        @staticmethod
        def test_EoS(volume,temperature):
            print('---test---')
    