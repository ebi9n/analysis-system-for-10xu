import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from natsort import natsorted
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns

import tkinter as tk
from tkinter import ttk
import setting

FIGSIZE = setting.FIGSIZE
DPI = setting.DPI

class TempTab(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_form()
        # 変数群を定義
    def setup_form(self):
        
        self.read_dist_frame = ReadDistFrame(master=self)
        self.show_dist_color_map_frame = ShowColorMapFrame(master=self)
        self.plot_option_frame = PlotOptionFrame(master=self)
        self.draw_select_frame = DrawSelectFrame(master=self)

        self.read_dist_frame.grid(row=0, column=0)
        self.show_dist_color_map_frame.grid(row=1,column=0)
        self.plot_option_frame.grid(row=2,column=0,padx=0,sticky=tk.EW)
        self.draw_select_frame.grid(row=3,column=0,padx=0,pady=20,sticky=tk.EW)

class ReadDistFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadDistFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self, text='distファイルの読み込み')
        self.label.grid(row=0, column=0, padx=10,sticky="w")
        
        # ファイル名を指定するテキストボックス
        self.textbox = tk.Entry(self, width=65)
        self.textbox.insert(0,'dist ファイルのpathを入力')
        self.textbox.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
        
        # ファイルパスを指定するボタン
        self.browse_button = tk.Button(self,text='ファイルを参照',command=self.button_select_dist_file)
        self.browse_button.grid(row=1,column=1,padx=10, pady=(0,10))
        
        self.open_button = tk.Button(self,text='　開く　')
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))
    
    def button_select_dist_file(self):
        filepath = self.browse_dist_file()
        if filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,filepath)

    @staticmethod
    def browse_dist_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        temp_dist_path = file_path
        if file_path:
            print("選択されたファイル:", file_path)
            return temp_dist_path
    
class ShowColorMapFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowColorMapFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
        self.fig = None
        self.canvas = None
    def setup_form(self):
        # test用
        self.fig = plt.figure(figsize=FIGSIZE,dpi=DPI)
        canvas = FigureCanvasTkAgg(self.fig,master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

class PlotOptionFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="PlotOptionFrame", **kwargs):
        super().__init__(text='プロットのオプション',*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
        
    def setup_form(self):
        max_pixel_enter_frame = MaxPixelEnterFrame(self)
        max_pixel_enter_frame.grid(row=0, column=0, padx=5,sticky=tk.EW)
        read_calib_frame = ReadCalibFrame(self)
        read_calib_frame.grid(row=1, column=0, padx=5,sticky=tk.EW)
        other_option_enter_frame = OtherOptionEnterFrame(self)
        other_option_enter_frame.grid(row=2,column=0,padx=5,sticky=tk.EW)

class DrawSelectFrame(tk.Frame):
    def __init__(self, *args,header_name="DrawSelectFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        replot_button = tk.Button(self,text='設定を反映して再描画')
        calc_button = tk.Button(self,text='設定を反映して温度を計算')
        replot_button.grid(row=0,column=0)
        calc_button.grid(row=0, column=1)
        
class OtherOptionEnterFrame(tk.Frame):
    """
    レーザー径を除くプロット設定を追記するフレーム
    """
    def __init__(self, *args,header_name="PlotOptionFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
        
    def setup_form(self):
        """
        - レーザー開始,終了フレーム(初期値はレーザー開始=0,終了=末尾のフレーム数にする)
        - レーザーの径(直径で入力)
        """
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        heat_start_enter_frame = HeatStartEnterFrame(self)
        heat_end_enter_frame = HeatEndEnterFrame(self)
        laser_diam_enter_frame = LaserDiamEnterFrame(self)

        heat_start_enter_frame.grid(row=0,column=0,padx=5,sticky="w")
        heat_end_enter_frame.grid(row=0,column=1,padx=10)
        laser_diam_enter_frame.grid(row=0,column=2,padx=10)

class HeatStartEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="HeatStartEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='加熱開始フレーム')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='Frame')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")

class HeatEndEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="HeatEndEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='加熱終了フレーム')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='Frame')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")

class LaserDiamEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="LaserDiamEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.left_label = tk.Label(self, text='レーザー直径')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='μm')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")

class MaxPixelEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="MaxPixelEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        left_max_pixel_enter_frame = LeftMaxPixelEnterFrame(master=self)
        left_max_pixel_enter_frame.grid(row=0, column=0, padx=5,sticky="w")
        right_max_pixel_enter_frame = RightMaxPixelEnterFrame(master=self)
        right_max_pixel_enter_frame.grid(row=0, column=1, padx=60)
class LeftMaxPixelEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="LeftMaxPixelEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='左側の最大強度のPixel')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='Pixel')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")
    
class RightMaxPixelEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="RightMaxPixelEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.right_label = tk.Label(self, text='右側の最大強度のPixel')
        self.right_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.right_textbox = tk.Entry(self, width=10)
        self.right_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.right_pixel_label = tk.Label(self, text='Pixel')
        self.right_pixel_label.grid(row=1, column=1, padx=5, sticky="w")

class ReadCalibFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadDistFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        calib_label = tk.Label(self, text='calibファイルから読み込む場合') #textサイズを小さくしよう
        calib_label.grid(row=0, column=0, padx=5,sticky="w")
        
        # ファイル名を指定するテキストボックス
        self.textbox = tk.Entry(self, width=65)
        self.textbox.insert(0,'calibファイルのpathを入力')
        self.textbox.grid(row=1, column=0, padx=5, pady=(0,10), sticky="ew")
        
        # ファイルパスを指定するボタン
        self.browse_button = tk.Button(self,text='ファイルを参照',command=self.button_select_calib_file)
        self.browse_button.grid(row=1,column=1,padx=10, pady=(0,10))
        
        # ファイルを開くボタン
        self.open_button = tk.Button(self,text='　開く　')
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))

    def button_select_calib_file(self):
        filepath = ReadDistFrame.browse_dist_file()
        if filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,filepath)