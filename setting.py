

"""
ソフトウェアの見た目に関する設定
"""
WINDOW_TITLE = "HLA" 
WINDOW_SIZE = "600x800"

"""
プロットに関する設定
"""
import matplotlib.pyplot as plt
plt.rcParams['ytick.major.width'] = 1.0#y軸主目盛り線の線幅
plt.rcParams['font.size'] = 8 #フォントの大きさ
plt.rcParams['axes.linewidth'] = 1.0# 軸の線幅edge linewidth
FIGSIZE = (5,5)
DPI = 100
FIGSIZE = (5,5)
DPI = 100
FACECOLOR = "white"
LASER_RANGE_COLOR = "white"
LASER_RANGE_ALPHA = 0.50
CLOSE_SHOW_DIST_PIXEL = 30

"""
calibファイルの最大pixelを取得するときの初期設定
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
