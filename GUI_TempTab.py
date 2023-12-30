import tkinter as tk
from tkinter import filedialog
import os, subprocess
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from natsort import natsorted
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import seaborn as sns
import threading

import tkinter as tk
from tkinter import ttk
import setting
from plot_dist_color_map_control import plotDistColorMap
from calculation import Calculation
from plot_temperature_result import PlotTempResult
FIGSIZE = setting.FIGSIZE
DPI = setting.DPI

class TempTab(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_form()
        self.dist_filepath = None
        self.draw_min_frame = None
        self.draw_max_frame = None
        self.left_max_pixel = None
        self.right_max_pixel = None
        self.beam_diam_pixel = None
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
    def update_canvas(self,
                      dist_filepath=None,
                      draw_min_frame = None,
                      draw_max_frame = None,
                      left_max_pixel = None,
                      right_max_pixel = None,
                      beam_diam_pixel = None):
        # optionFrameからすべての値を取得する
        if dist_filepath is not None:
            self.dist_filepath = dist_filepath
        self.update_options()
        print(self.beam_diam_pixel)
        self.show_dist_color_map_frame.update(dist_filepath=self.dist_filepath,
                                              draw_min_frame=self.draw_min_frame,
                                              draw_max_frame=self.draw_max_frame,
                                              left_max_frame=self.left_max_pixel,
                                              right_max_frame=self.right_max_pixel,
                                              beam_diam_pixel=self.beam_diam_pixel)
    def get_temp_result_param(self):
        self.plot_option_frame.update_value()
        if self.plot_option_frame.draw_min_frame is not None:
            self.draw_min_frame = self.plot_option_frame.draw_min_frame
        if self.plot_option_frame.draw_max_frame is not None:
            self.draw_max_frame = self.plot_option_frame.draw_max_frame
        if self.plot_option_frame.left_max_pixel is not None:
            self.left_max_pixel = self.plot_option_frame.left_max_pixel
        if self.plot_option_frame.right_max_pixel is not None:
            self.right_max_pixel = self.plot_option_frame.right_max_pixel
        if self.plot_option_frame.beam_diam_pixel is not None:
            self.beam_diam_pixel = self.plot_option_frame.beam_diam_pixel
        return self.dist_filepath,self.draw_min_frame,self.draw_max_frame,self.left_max_pixel,self.right_max_pixel,self.beam_diam_pixel
    def update_options(self):
        self.plot_option_frame.update_value()
        if self.plot_option_frame.draw_min_frame is not None:
            self.draw_min_frame = self.plot_option_frame.draw_min_frame
        if self.plot_option_frame.draw_max_frame is not None:
            self.draw_max_frame = self.plot_option_frame.draw_max_frame
        if self.plot_option_frame.left_max_pixel is not None:
            self.left_max_pixel = self.plot_option_frame.left_max_pixel
        if self.plot_option_frame.right_max_pixel is not None:
            self.right_max_pixel = self.plot_option_frame.right_max_pixel
        if self.plot_option_frame.beam_diam_pixel is not None:
            self.beam_diam_pixel = self.plot_option_frame.beam_diam_pixel

        
class ReadDistFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadDistFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.dist_filepath = None
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
        
        self.open_button = tk.Button(self,text='　開く　',command=self.button_draw_color_map)
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))
    
    def button_select_dist_file(self):
        self.dist_filepath = self.browse_dist_file()
        if self.dist_filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,self.dist_filepath)
    
    def button_draw_color_map(self):
        if self.textbox.get() is not None:
            dist_filepath = self.textbox.get()
            print(dist_filepath)
        self.master.update_canvas(dist_filepath=dist_filepath)
    
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
        self.fig = None
        self.canvas = None
        self.dist_filepath = None
        self.plot_dist_control = plotDistColorMap()
        self.draw_min_frame = setting.INITIAL_HEAT_START_FRAME
        self.draw_max_frame = setting.INITIAL_HEAT_END_FRAME
        self.left_max_pixel = setting.LEFT_MAX_PIXEL
        self.right_max_pixel = setting.RIGHT_MAX_PIXEL
        self.laser_beam_diam_pixel = setting.INITIAL_LASER_DIAMETER
        self.setup_form()
    def setup_form(self):
        # test用
        self.canvas = tk.Canvas(master=self, bg='white',height=500,width=500)
        self.canvas.grid(row=0,column=0)
    
    def update(self, dist_filepath=None,
                     draw_min_frame=None,
                     draw_max_frame=None,
                     left_max_frame=None,
                     right_max_frame=None,
                     beam_diam_pixel=None):
        # 再描画用
        del self.plot_dist_control
        self.plot_dist_control = plotDistColorMap()
        self.fig = self.plot_dist_control.fig
        self.dist_filepath = dist_filepath
        self.draw_min_frame = draw_min_frame
        self.draw_max_frame = draw_max_frame
        self.left_max_pixel = left_max_frame
        self.right_max_pixel = right_max_frame
        self.laser_beam_diam_pixel = beam_diam_pixel
        self.plot_dist_control.replot(self.dist_filepath,
                                      draw_min_frame=self.draw_min_frame,
                                      draw_max_frame=self.draw_max_frame,
                                      left_max_pixel=self.left_max_pixel,
                                      right_max_pixel=self.right_max_pixel,
                                      beam_diam_pixel=self.laser_beam_diam_pixel)
        self.canvas = FigureCanvasTkAgg(self.fig,master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0,column=0)

class PlotOptionFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="PlotOptionFrame", **kwargs):
        super().__init__(text='プロットのオプション',*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
        self.draw_min_frame = None
        self.draw_max_frame = None
        self.left_max_pixel = None
        self.right_max_pixel = None
        self.beam_diam_pixel = None
    def setup_form(self):
        self.max_pixel_enter_frame = MaxPixelEnterFrame(self)
        self.max_pixel_enter_frame.grid(row=0, column=0, padx=5,sticky=tk.EW)
        self.read_calib_frame = ReadCalibFrame(self)
        self.read_calib_frame.grid(row=1, column=0, padx=5,sticky=tk.EW)
        self.other_option_enter_frame = OtherOptionEnterFrame(self)
        self.other_option_enter_frame.grid(row=2,column=0,padx=5,sticky=tk.EW)

    def update_value(self):
        self.left_max_pixel = int(self.max_pixel_enter_frame.left_max_pixel_enter_frame.left_textbox.get())
        self.right_max_pixel = int(self.max_pixel_enter_frame.right_max_pixel_enter_frame.right_textbox.get())
        self.draw_min_frame = int(self.other_option_enter_frame.heat_start_enter_frame.left_textbox.get())
        self.draw_max_frame = int(self.other_option_enter_frame.heat_end_enter_frame.left_textbox.get())
        self.beam_diam_pixel = float(self.other_option_enter_frame.laser_diam_enter_frame.left_textbox.get())

    def enter_from_calib(self,left_max_pixel, right_max_pixel):
        self.max_pixel_enter_frame.left_max_pixel_enter_frame.left_textbox.delete(0,tk.END)
        self.max_pixel_enter_frame.right_max_pixel_enter_frame.right_textbox.delete(0,tk.END)
        self.max_pixel_enter_frame.left_max_pixel_enter_frame.left_textbox.insert(0,left_max_pixel)
        self.max_pixel_enter_frame.right_max_pixel_enter_frame.right_textbox.insert(0, right_max_pixel)

class DrawSelectFrame(tk.Frame):
    def __init__(self, *args,header_name="DrawSelectFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
        self.fig = None
        self.all_temp_df = None
        self.dlg_modeless = None
    def setup_form(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        replot_button = tk.Button(self,text='設定を反映して再描画',command=self.button_redraw)
        calc_button = tk.Button(self,text='設定を反映して温度を計算',command=self.button_calc_temp)
        replot_button.grid(row=0,column=0)
        calc_button.grid(row=0, column=1)
    def button_redraw(self):
        self.master.update_canvas()
    def button_calc_temp(self):
        
        # 値を取得する
        dist_path,heat_start_frame,heat_end_frame,left_max_pixel,right_max_pixel,laser_diam = self.master.get_temp_result_param()
        plot_temp_result = PlotTempResult()
        self.fig = plot_temp_result.replot(dist_filepath=dist_path,
                                                 left_max_pixel=left_max_pixel,
                                                 right_max_pixel=right_max_pixel,
                                                 laser_diam=laser_diam,
                                                 heat_start_frame=heat_start_frame,
                                                 heat_end_frame=heat_end_frame)
        self.all_temp_df = plot_temp_result.all_temp_df
        self.temp_result_modeless = TempResultModeless(master=self,fig=self.fig,all_temp_df=self.all_temp_df,dist_path = dist_path)
class TempResultModeless(tk.Toplevel):
    def __init__(self,fig=None,all_temp_df = None,master=None,dist_path=None,*args, **kwargs):
        super().__init__()
        self.fig = fig
        self.dist_path  = dist_path
        self.all_temp_df = all_temp_df
        self.title("Result View")   # ウィンドウタイトル
        self.geometry("600x600")
        self.setup_form()
    def setup_form(self):
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        canvas = FigureCanvasTkAgg(master=self,figure=self.fig)
        
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,padx=5,pady=5,sticky=tk.EW)

        toolbar_frame = tk.Frame(master=self)
        toolbar_frame.grid(row=1,column=0)
        toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        self.save_select_frame = SaveSelectFrame(master=self)
        self.save_select_frame.grid(row=2,column=0)
class SaveSelectFrame(tk.Frame):
    def __init__(self, *args,header_name="SaveSelectFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.fig = self.master.fig
        self.dist_path = self.master.dist_path
        self.all_temp_df = self.master.all_temp_df
        self.setup_form()

    def setup_form(self):
        save_fig_button = tk.Button(master=self, text='画像ファイルを保存',command=self.browse_save_fig)
        save_csv_button = tk.Button(master=self, text='csvファイルを保存',command=self.browse_save_csv)
        save_fig_button.grid(row=0, column=0)
        save_csv_button.grid(row=0, column=1)
    def browse_save_fig(self):
        initialfile = os.path.splitext(os.path.basename(self.dist_path))[0]
        save_fig_path = filedialog.asksaveasfilename(defaultextension='png',initialfile=initialfile)
        self.fig.savefig(save_fig_path)
    def browse_save_csv(self):
        initialfile = os.path.splitext(os.path.basename(self.dist_path))[0]
        save_csv_path = filedialog.asksaveasfilename(defaultextension='csv',initialfile=initialfile)
        self.all_temp_df.to_csv(save_csv_path)

class OtherOptionEnterFrame(tk.Frame):
    """
    中心位置を除くプロット設定を追記するフレーム
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
        self.heat_start_enter_frame = HeatStartEnterFrame(self)
        self.heat_end_enter_frame = HeatEndEnterFrame(self)
        self.laser_diam_enter_frame = LaserDiamEnterFrame(self)
        
        self.heat_start_enter_frame.grid(row=0,column=0,padx=5,sticky="w")
        self.heat_end_enter_frame.grid(row=0,column=1,padx=10)
        self.laser_diam_enter_frame.grid(row=0,column=2,padx=10)

class HeatStartEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="HeatStartEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.draw_min_frame = setting.INITIAL_HEAT_START_FRAME
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='加熱開始フレーム')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.insert(0,self.draw_min_frame)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='Frame')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")

class HeatEndEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="HeatEndEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.draw_max_frame = setting.INITIAL_HEAT_END_FRAME
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='加熱終了フレーム')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.insert(0,self.draw_max_frame)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='Frame')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")

class LaserDiamEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="LaserDiamEnterFrame", **kwargs):
        self.laser_beam_diam_pixel = setting.INITIAL_LASER_DIAMETER
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='レーザー直径')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.insert(0,self.laser_beam_diam_pixel)
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
        self.left_max_pixel_enter_frame = LeftMaxPixelEnterFrame(master=self)
        self.left_max_pixel_enter_frame.grid(row=0, column=0, padx=5,sticky="w")
        self.right_max_pixel_enter_frame = RightMaxPixelEnterFrame(master=self)
        self.right_max_pixel_enter_frame.grid(row=0, column=1, padx=60)
class LeftMaxPixelEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="LeftMaxPixelEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.left_max_pixel = setting.LEFT_MAX_PIXEL
        self.setup_form()
    def setup_form(self):
        self.left_label = tk.Label(self, text='左側の最大強度のPixel')
        self.left_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.left_textbox = tk.Entry(self, width=10)
        self.left_textbox.insert(0,self.left_max_pixel)
        self.left_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.left_pixel_label = tk.Label(self, text='Pixel')
        self.left_pixel_label.grid(row=1, column=1, padx=5, sticky="w")
    
class RightMaxPixelEnterFrame(tk.Frame):
    def __init__(self, *args, header_name="RightMaxPixelEnterFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.right_max_pixel = setting.RIGHT_MAX_PIXEL
        self.setup_form()
    def setup_form(self):
        self.right_label = tk.Label(self, text='右側の最大強度のPixel')
        self.right_label.grid(row=0, column=0,columnspan = 2, padx=5, sticky="w")
        self.right_textbox = tk.Entry(self, width=10)
        self.right_textbox.insert(0,self.right_max_pixel)
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
        self.open_button = tk.Button(self,text='　開く　',command=self.button_open_calib_file)
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))

    def button_select_calib_file(self):
        filepath = ReadDistFrame.browse_dist_file()
        if filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,filepath)
    
    def button_open_calib_file(self):
        if os.path.exists(self.textbox.get()):
            progress_modal = tk.Toplevel(master=self)
            progress_modal.title('now calculating...')
            modal_x = self.master.master.master.master.winfo_x() + self.master.master.master.master.winfo_reqwidth() // 2 -40
            modal_y = self.master.master.master.master.winfo_y() + self.master.master.master.master.winfo_reqheight() // 2 -40
            progress_modal.geometry(f'80x50+{modal_x}+{modal_y}')

            progress_modal.grab_set() #モーダルに
            progress_modal.focus_set() # フォーカスするように
            progress_modal.transient(self.master) 
            progress_label = tk.Label(progress_modal,text='現在計算中です…')
            progress_bar = ttk.Progressbar(progress_modal,
                                           maximum=100,
                                           mode="indeterminate",
                                           style="Horizontal.TProgressbar")
            progress_label.grid(row=0, column=0)
            progress_bar.grid(row=1, column=0)

            # 非同期処理を開始するスレッド
            thread = threading.Thread(target=self.calculate_max_pixel, args=(self.textbox.get(), progress_bar,progress_modal))
            thread.start()

    def calculate_max_pixel(self, file_path, progress_bar, progress_modal):
        # 重い処理を別スレッドで実行
        progress_bar.start()
        left_max_pixel, right_max_pixel = Calculation.get_max_pixel(file_path)
        # 処理が完了したらGUIの更新を行う
        self.master.after(100, lambda: self.update_gui(left_max_pixel, right_max_pixel, progress_bar,progress_modal))
    def update_gui(self, left_max_pixel, right_max_pixel, progress_bar,progress_modal):
        # GUIの更新をメインスレッドで実行
        progress_bar.stop()
        progress_bar.destroy()

        # ここで必要なGUIの更新を行う
        self.master.enter_from_calib(left_max_pixel, right_max_pixel)
        progress_modal.destroy()