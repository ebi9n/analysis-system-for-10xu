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
import inspect
import tkinter as tk
from tkinter import ttk
import setting
from plot_dist_color_map_control import plotDistColorMap
from calculation import Calculation
from plot_temperature_result import PlotTempResult
FIGSIZE = setting.FIGSIZE
DPI = setting.DPI

class PhaseTab(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.XRD_progress = False
        self.complement_progress = False
        self.EoS_progress = False
        self.setup_form()
        # 変数群を定義
    def setup_form(self):
        print('---test---')
        self.grid_columnconfigure(0, weight=1)
        peak_seek_frame = PeakSeekFrame(master=self)
        complement_freq_frame = ComplementFreqFrame(master=self)
        select_EoS_frame = SelectEoSFrame(master=self)
        start_calc_EoS_button = tk.Button(self,text='相図を描画',width=30,bg='#dddddd')
        peak_seek_frame.grid(row=0,column=0,pady=5)
        complement_freq_frame.grid(row=1,column=0,pady=5,sticky="ew")
        select_EoS_frame.grid(row=2,column=0,pady=5,sticky="ew")
        start_calc_EoS_button.grid(row=3,column=0,pady=15)

class PeakSeekFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="PeakSeekFrame", **kwargs):
        super().__init__(text='① 体積計算に使用するピークを探査',*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.XRD_progress = False
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0, weight=1)
        self.read_XRD_frame = ReadXRDFrame(master=self)
        self.entry_range_frame = EntryRangeFrame(master=self)
        self.show_seek_range_button = tk.Button(master=self,text='　　探査を開始　　',command=self.button_seek_range_modeless)
        self.show_progress_frame = ShowXRDProgressFrame(master=self)
        self.read_XRD_frame.grid(row=0,column=0,padx=5,pady=5)
        self.entry_range_frame.grid(row=1,column=0,padx=5,pady=5,sticky="ew")
        self.show_seek_range_button.grid(row=2,column=0,pady=5,sticky="ew")
        self.show_progress_frame.grid(row=3,column=0)
    def button_seek_range_modeless(self):
        self.seek_range_modeless = SeekRangeModeless(self)

class ReadXRDFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadXRDFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.setup_form()
    def setup_form(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self, text='XRDファイルの読み込み')
        self.label.grid(row=0, column=0, padx=10,sticky="w")
        
        # ファイル名を指定するテキストボックス
        self.textbox = tk.Entry(self, width=65)
        self.textbox.insert(0,'XRDファイルのpathを入力')
        self.textbox.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
        
        # ファイルパスを指定するボタン
        self.browse_button = tk.Button(self,text='ファイルを参照',command=self.button_select_file)
        self.browse_button.grid(row=1,column=1,padx=10, pady=(0,10))
        
        self.open_button = tk.Button(self,text='　開く　',command=self.button_open_XRDfile)
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))
    
    def button_select_file(self):
        self.XRD_filepath = self.browse_file()
        if self.XRD_filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,self.XRD_filepath)
    def button_open_XRDfile(self):
        if self.textbox.get() is not None:
            self.XRD_filepath = self.textbox.get()
            self.master.XRD_filepath = self.XRD_filepath
            print(self.master.XRD_filepath)

    @staticmethod
    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            print("選択されたファイル:", file_path)
            return file_path
class SeekRangeModeless(tk.Toplevel):
    def __init__(self,fig=None,all_temp_df = None,*args, **kwargs):
        super().__init__()
        self.fig = fig
        self.title("Seek Range")   # ウィンドウタイトル
        self.geometry("600x600")
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0,weight=1)

        #canvas = FigureCanvasTkAgg(master=self,figure=self.fig)
        
        #canvas.draw()
        #canvas.get_tk_widget().grid(row=0,column=0,padx=5,pady=5,sticky=tk.EW)

        #toolbar_frame = tk.Frame(master=self)
        #toolbar_frame.grid(row=1,column=0)
        #toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
        self.seek_select_frame = SeekSelectFrame(self)
        self.seek_select_frame.grid(row=1,column=0)
class SeekSelectFrame(tk.Frame):
    def __init__(self, *args, header_name="EntryRangeFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        OK_button = tk.Button(self,text='この範囲で探査')
        cancel_button = tk.Button(self,text='探査をキャンセル')
        OK_button.grid(row=0,column=0)
        cancel_button.grid(row=0,column=1)
class EntryRangeFrame(tk.Frame):
    def __init__(self, *args, header_name="EntryRangeFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.setup_form()
    def setup_form(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        min_range_frame = tk.Frame(self)
        max_range_frame = tk.Frame(self)
        min_range_frame.grid(row=0,column=0,padx=5,sticky="w")
        max_range_frame.grid(row=0,column=1,padx=5,sticky="e")

        self.min_label = tk.Label(min_range_frame, text='探査2θの下限 (deg)')
        self.min_label.grid(row=0, column=0,columnspan=2, padx=5, sticky="w")
        self.min_textbox = tk.Entry(min_range_frame, width=20)
        self.min_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.min_deg_label = tk.Label(min_range_frame, text='deg')
        self.min_deg_label.grid(row=1, column=1, padx=5, sticky="w")

        self.max_label = tk.Label(max_range_frame, text='探査2θの上限 (deg)')
        self.max_label.grid(row=0, column=0,columnspan=2, padx=5, sticky="w")
        self.max_textbox = tk.Entry(max_range_frame, width=20)
        self.max_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.max_deg_label = tk.Label(max_range_frame, text='deg')
        self.max_deg_label.grid(row=1, column=1, padx=5, sticky="w")

class ShowXRDProgressFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowProgress", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.XRD_progress = False
        self.setup_form()
    def setup_form(self):
        label = tk.Label(self,text='状況：')
        progress_label = self.change_progress_color(self,self.XRD_progress)
        label.grid(row=0,column=0,padx=5)
        progress_label.grid(row=0,column=1,padx=5)
    @ staticmethod
    def change_progress_color(master,progress):
        if progress:
            return tk.Label(master,text='完了',foreground='#00ff22')
        else:
            return tk.Label(master,text='未完了',foreground='#ff0000')
class ComplementFreqFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="ComplementFreqFrame", **kwargs):
        super().__init__(text='② 測定頻度の違いを補完',*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0, weight=1)
        self.read_temp_frame = ReadTempFrame(self)
        self.entry_freq_frame = EntryFreqFrame(self)
        self.start_complement_button = tk.Button(self,text='補完を開始')
        self.show_temp_progress_frame = ShowTempProgressFrame(self)
        self.read_temp_frame.grid(row=0,column=0,sticky="ew")
        self.entry_freq_frame.grid(row=1,column=0,sticky="ew")
        self.start_complement_button.grid(row=2,column=0,sticky="ew")
        self.show_temp_progress_frame.grid(row=3,column=0)
class ReadTempFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadXRDFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.setup_form()
    def setup_form(self):
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self, text='温度ファイルの読み込み')
        self.label.grid(row=0, column=0, padx=10,sticky="w")
        
        # ファイル名を指定するテキストボックス
        self.textbox = tk.Entry(self, width=65)
        self.textbox.insert(0,'温度ファイルのpathを入力')
        self.textbox.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
        
        # ファイルパスを指定するボタン
        self.browse_button = tk.Button(self,text='ファイルを参照')
        self.browse_button.grid(row=1,column=1,padx=10, pady=(0,10))
        
        self.open_button = tk.Button(self,text='　開く　')
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))
class EntryFreqFrame(tk.Frame):
    def __init__(self, *args, header_name="EntryFreqFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        min_range_frame = tk.Frame(self)
        max_range_frame = tk.Frame(self)
        min_range_frame.grid(row=0,column=0,padx=5,sticky="w")
        max_range_frame.grid(row=0,column=1,padx=5,sticky="e")

        self.min_label = tk.Label(min_range_frame, text='XRDの測定頻度(Frame Per Sec)')
        self.min_label.grid(row=0, column=0,columnspan=2, padx=5, sticky="w")
        self.min_textbox = tk.Entry(min_range_frame, width=20)
        self.min_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.min_deg_label = tk.Label(min_range_frame, text='FPS')
        self.min_deg_label.grid(row=1, column=1, padx=5, sticky="w")

        self.max_label = tk.Label(max_range_frame, text='温度の測定頻度(Frame Per Sec)')
        self.max_label.grid(row=0, column=0,columnspan=2, padx=5, sticky="w")
        self.max_textbox = tk.Entry(max_range_frame, width=20)
        self.max_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.max_deg_label = tk.Label(max_range_frame, text='FPS')
        self.max_deg_label.grid(row=1, column=1, padx=5, sticky="w")
class ShowTempProgressFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowProgress", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.temp_progress = False
        self.setup_form()
    def setup_form(self):
        label = tk.Label(self,text='状況：')
        progress_label = self.change_progress_color(self,self.temp_progress)
        label.grid(row=0,column=0,padx=5)
        progress_label.grid(row=0,column=1,padx=5)
    @ staticmethod
    def change_progress_color(master,progress):
        if progress:
            return tk.Label(master,text='完了',foreground='#00ff22')
        else:
            return tk.Label(master,text='未完了',foreground='#ff0000')

class SelectEoSFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="PeakSeekFrame", **kwargs):
        super().__init__(text='③ 状態方程式の選択',*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0,weight=1)
        self.select_EoS = tk.StringVar()
        self.EoS_tuple = self.get_class_methods(setting.EoS)
        self.combobox = ttk.Combobox(self, state="readonly",values=self.EoS_tuple,width=25)
        self.progress_frame = ShowEoSProgressFrame(self)
        
        self.combobox.grid(row=0,column=0)
        self.progress_frame.grid(row=1,column=0)
        
    @staticmethod
    def get_class_methods(cls):
        return tuple([func for func in dir(cls) if inspect.isfunction(getattr(cls, func))])

class ShowEoSProgressFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowProgress", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.EoS_progress = False
        self.setup_form()
    def setup_form(self):
        label = tk.Label(self,text='状況：')
        progress_label = self.change_progress_color(self,self.EoS_progress)
        label.grid(row=0,column=0,padx=5)
        progress_label.grid(row=0,column=1,padx=5)
    @ staticmethod
    def change_progress_color(master,progress):
        if progress:
            return tk.Label(master,text='完了',foreground='#00ff22')
        else:
            return tk.Label(master,text='未完了',foreground='#ff0000')
if __name__ == '__main__':
    app = tk.Tk()
    app.geometry(setting.WINDOW_SIZE)
    tabs = ttk.Notebook(app)
    tabs.pack(expand=True,fill='both')
    phase_tab = PhaseTab()
    tabs.add(phase_tab,text='相図')
    app.mainloop()