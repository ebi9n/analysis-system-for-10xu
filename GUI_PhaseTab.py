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
from plot_seek_range_fig import PlotSeekRangeFig
from plot_phase_diagram import PlotPhaseDiagram
from calculation import Calculation
from plot_temperature_result import PlotTempResult
FIGSIZE = setting.FIGSIZE
DPI = setting.DPI

class PhaseTab(tk.Frame):
    def __init__(self, master=None,*args, **kwargs):
        super().__init__(master, **kwargs)
        self.XRD_progress = False
        
        self.complement_progress = False
        self.EoS_progress = False
        self.XRD_filepath = None
        self.select_EoS_name = None
        self.volume_arr = None
        self.all_complemented_temp_df = None

        self.setup_form()
        # 変数群を定義
    def setup_form(self):
        print('---test---')
        self.grid_columnconfigure(0, weight=1)
        self.peak_seek_frame = PeakSeekFrame(master=self)
        complement_freq_frame = ComplementFreqFrame(master=self)
        self.select_EoS_frame = SelectEoSFrame(master=self)
        start_calc_EoS_button = tk.Button(self,text='相図を描画',width=30,bg='#dddddd',command=self.button_calc_phase)
        self.peak_seek_frame.grid(row=0,column=0,pady=20,sticky="ew")
        complement_freq_frame.grid(row=1,column=0,pady=20,sticky="ew")
        self.select_EoS_frame.grid(row=2,column=0,pady=20,sticky="ew")
        start_calc_EoS_button.grid(row=3,column=0,pady=30)
    def button_calc_phase(self):
        self.select_EoS_name = self.select_EoS_frame.combobox.get()
        self.phase_diagram_modeless = PhaseDiagramModeless(master=self,
                                                           volume_arr=self.volume_arr,
                                                           all_complemented_temp_df= self.all_complemented_temp_df,
                                                           EoS_name=self.select_EoS_name)
    
        
class PhaseDiagramModeless(tk.Toplevel):
    def __init__(self,
                 master=None,
                 volume_arr=None,
                 all_complemented_temp_df=None,
                 EoS_name=None,
                 *args, **kwargs):
        super().__init__(master, **kwargs)
        self.volume_arr = volume_arr
        self.all_complemented_temp_df = all_complemented_temp_df
        self.EoS_name = EoS_name
        self.fig = None
        self.EoS = getattr(setting.EoS,self.EoS_name)
        self.setup_form()
        
    def setup_form(self):
        self.grid_columnconfigure(0,weight=1)
        self.result_df = Calculation.get_all_result_df(volume_arr=self.volume_arr,
                                                       all_complemented_temp_df=self.all_complemented_temp_df,
                                                       EoS=self.EoS)
        self.plot_phase_diagram = PlotPhaseDiagram()
        self.fig = self.plot_phase_diagram.get_phase_diagram(result_df=self.result_df)

        canvas = FigureCanvasTkAgg(master=self,figure=self.fig)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,padx=5,pady=5,sticky=tk.EW)
        self.save_select_frame = SaveSelectFrame(master=self)
        self.save_select_frame.grid(row=1,column=0,padx=5,pady=5,sticky=tk.EW)
    def save_result_csv(self):
        save_path = filedialog.asksaveasfilename(defaultextension='csv')
        self.result_df.to_csv(save_path)
    def save_fig(self):
        save_path = filedialog.asksaveasfilename(defaultextension='csv')
        self.fig.savefig(save_path)

class SaveSelectFrame(tk.Frame):
    def __init__(self, *args,header_name="SaveSelectFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        save_fig_button = tk.Button(master=self, text='画像ファイルを保存',command=self.button_save_fig)
        save_csv_button = tk.Button(master=self, text='csvファイルを保存',command=self.button_save_csv)
        save_fig_button.grid(row=0, column=0)
        save_csv_button.grid(row=0, column=1)
    def button_save_fig(self):
        self.master.save_fig()
    def button_save_csv(self):
        self.master.save_result_csv()

class PeakSeekFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="PeakSeekFrame", **kwargs):
        super().__init__(text='① 体積計算に使用するピークを探査',*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.XRD_progress = False
        self.volume_arr = None
        self.peak_seek_range_min = None
        self.peak_seek_range_max = None
        self.seek_range_modeless = None
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0, weight=1)
        
        self.read_XRD_frame = ReadXRDFrame(master=self)
        self.entry_range_frame = EntryRangeFrame(master=self)
        self.show_seek_range_button = tk.Button(master=self,text='　　探査を開始　　',command=self.button_seek_range_modeless)
        self.show_progress_frame = ShowXRDProgressFrame(master=self)
        self.read_XRD_frame.grid(row=0,column=0,padx=5,pady=5,sticky="ew")
        self.entry_range_frame.grid(row=1,column=0,padx=5,pady=5,sticky="ew")
        self.show_seek_range_button.grid(row=2,column=0,pady=5,sticky="ew")
        self.show_progress_frame.grid(row=3,column=0)
    def button_seek_range_modeless(self):
        self.get_range_value()
        self.seek_range_modeless = SeekRangeModeless(self.on_seek_range_modeless_close,master=self,
                                                     XRD_filepath=self.XRD_filepath,
                                                     peak_seek_range_min=self.peak_seek_range_min,
                                                     peak_seek_range_max=self.peak_seek_range_max)
    def get_range_value(self):
        if self.entry_range_frame.min_textbox.get() and self.entry_range_frame.max_textbox.get():
            peak_seek_range_min = float(self.entry_range_frame.min_textbox.get())
            peak_seek_range_max = float(self.entry_range_frame.max_textbox.get())
        self.peak_seek_range_min = peak_seek_range_min
        self.peak_seek_range_max = peak_seek_range_max
    def change_XRD_progress(self):
        self.master.XRD_progress = True
        self.XRD_progress = True
        self.show_progress_frame.change_progress_color(self.XRD_progress)
    def on_seek_range_modeless_close(self, modeless_instance):
        # ここで SeekRangeModeless が閉じたときの処理を行う
        print("SeekRangeModeless closed")
        if self.seek_range_modeless.complete_bool:
            self.master.volume_arr = self.seek_range_modeless.volume_arr
            self.change_XRD_progress()
            self.master.XRD_filepath = self.XRD_filepath
            print(self.master.volume_arr)

class ReadXRDFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadXRDFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.volume_arr = None
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
        
    
    def button_select_file(self):
        self.XRD_filepath = self.browse_file()
        if self.XRD_filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,self.XRD_filepath)
            self.XRD_filepath = self.textbox.get()
            self.master.XRD_filepath = self.XRD_filepath
            print(self.master.XRD_filepath)
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
    def __init__(self,
                 on_close_callback,
                 fig=None,
                 XRD_filepath=None,
                 peak_seek_range_min=None,
                 peak_seek_range_max=None,
                 *args, **kwargs):
        super().__init__()
        self.on_close_callback = on_close_callback
        self.fig = None
        self.complete_bool = False
        self.XRD_filepath = XRD_filepath
        self.peak_seek_range_min = peak_seek_range_min
        self.peak_seek_range_max = peak_seek_range_max
        self.title("Seek Range")   # ウィンドウタイトル
        self.geometry("600x600")
        self.setup_form()
    def destroy(self):
        if self.on_close_callback:
            self.on_close_callback(self)  # ここでコールバックを呼び出す
        super().destroy()
    
    def setup_form(self):
        self.grid_columnconfigure(0,weight=1)
        # figを取得
        plot_seek_range_fig = PlotSeekRangeFig()
        seek_range_fig = plot_seek_range_fig.get_seek_range_fig(XRD_filepath=self.XRD_filepath,
                                                                peak_seek_range_min=self.peak_seek_range_min,
                                                                peak_seek_range_max=self.peak_seek_range_max)
        self.fig = seek_range_fig
        canvas = FigureCanvasTkAgg(master=self,figure=self.fig)
        
        canvas.draw()
        canvas.get_tk_widget().grid(row=0,column=0,padx=5,pady=5,sticky=tk.EW)

        self.seek_select_frame = SeekSelectFrame(self)
        self.seek_select_frame.grid(row=1,column=0)
    def start_seek_peak(self):
        self.volume_arr = Calculation.calc_lattice_volume(XRD_filepath=self.XRD_filepath,
                                                     peak_seek_range_min=self.peak_seek_range_min,
                                                     peak_seek_range_max=self.peak_seek_range_max)
        volume_arr = self.volume_arr
        self.complete_bool = True
        self.destroy()
        plt.close("all")
    def cancel_seek_peak(self):
        plt.close("all")
        self.destroy()

class SeekSelectFrame(tk.Frame):
    def __init__(self, *args, header_name="EntryRangeFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        OK_button = tk.Button(self,text='この範囲で探査',command=self.button_start_seek)
        cancel_button = tk.Button(self,text='探査をキャンセル',command=self.button_cancel)
        OK_button.grid(row=0,column=0)
        cancel_button.grid(row=0,column=1)
    def button_start_seek(self):
        self.master.start_seek_peak()
    def button_cancel(self):
        self.master.cancel_seek_peak()

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
        self.progress_label = None
        self.setup_form()
    def setup_form(self):
        self.label = tk.Label(self,text='状況：')
        self.progress_label = tk.Label(self,text='未完了',foreground='#ff0000')
        self.label.grid(row=0,column=0,padx=5)
        self.progress_label.grid(row=0,column=1,padx=5)
    def change_progress_color(self,progress):
        if progress:
            self.progress_label.destroy()
            self.progress_label = tk.Label(self,text='完了',foreground='#00ff00')
            self.progress_label.grid(row=0,column=1,padx=5)
        

class ComplementFreqFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="ComplementFreqFrame", **kwargs):
        super().__init__(text='② 測定頻度の違いを補完',*args, **kwargs)
        self.header_name = header_name
        self.temp_filepath = None
        self.XRD_FPS = None
        self.temp_FPS = None
        self.XRD_filepath = None
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0, weight=1)
        self.read_temp_frame = ReadTempFrame(self)
        self.entry_freq_frame = EntryFreqFrame(self)
        self.start_complement_button = tk.Button(self,text='補完を開始',command=self.button_start_complement)
        self.show_temp_progress_frame = ShowTempProgressFrame(self)
        self.read_temp_frame.grid(row=0,column=0,sticky="ew")
        self.entry_freq_frame.grid(row=1,column=0,sticky="ew")
        self.start_complement_button.grid(row=2,column=0,sticky="ew")
        self.show_temp_progress_frame.grid(row=3,column=0)
    def button_start_complement(self):
        self.get_parameters()
        all_temp_df = Calculation.read_temp_df_from_csv(self.temp_filepath)
        formatted_XRD_df = Calculation.format_XRD_df(self.XRD_filepath)
        all_complemented_temp_df = Calculation.get_all_complemented_temp_df(all_temp_df=all_temp_df,
                                                                            formatted_XRD_df=formatted_XRD_df,
                                                                            XRD_frame_per_ms=self.XRD_FPS,
                                                                            temp_frame_per_ms=self.temp_FPS)
        self.master.all_complemented_temp_df = all_complemented_temp_df
        self.show_temp_progress_frame.temp_progress = True
        self.show_temp_progress_frame.change_progress_color(self.show_temp_progress_frame.temp_progress)
    def get_parameters(self):
        if self.entry_freq_frame.XRD_textbox.get():
            self.XRD_FPS = float(self.entry_freq_frame.XRD_textbox.get())
        if self.entry_freq_frame.temp_textbox.get():
            self.temp_FPS = float(self.entry_freq_frame.temp_textbox.get())
        self.XRD_filepath = self.master.XRD_filepath
        
class ReadTempFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadXRDFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.XRD_filepath = None
        self.temp_filepath = None
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
        self.browse_button = tk.Button(self,text='ファイルを参照',command=self.button_select_file)
        self.browse_button.grid(row=1,column=1,padx=10, pady=(0,10))
    
    def button_select_file(self):
        self.temp_filepath = ReadXRDFrame.browse_file()
        if self.temp_filepath:
            self.textbox.delete(0, tk.END)
            self.textbox.insert(0,self.temp_filepath)
            self.master.temp_filepath = self.temp_filepath
            print(self.master.temp_filepath)
        
class EntryFreqFrame(tk.Frame):
    def __init__(self, *args, header_name="EntryFreqFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
    def setup_form(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        XRD_frame = tk.Frame(self)
        temp_frame = tk.Frame(self)
        XRD_frame.grid(row=0,column=0,padx=5,sticky="w")
        temp_frame.grid(row=0,column=1,padx=5,sticky="e")

        self.XRD_label = tk.Label(XRD_frame, text='XRDの測定頻度(ms / frame)')
        self.XRD_label.grid(row=0, column=0,columnspan=2, padx=5, sticky="w")
        self.XRD_textbox = tk.Entry(XRD_frame, width=20)
        self.XRD_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.XRD_freq_label = tk.Label(XRD_frame, text='ms / frame')
        self.XRD_freq_label.grid(row=1, column=1, padx=5, sticky="w")

        self.temp_label = tk.Label(temp_frame, text='温度の測定頻度(ms / frame)')
        self.temp_label.grid(row=0, column=0,columnspan=2, padx=5, sticky="w")
        self.temp_textbox = tk.Entry(temp_frame, width=20)
        self.temp_textbox.grid(row=1, column=0, padx=5, sticky="w")
        self.temp_freq_label = tk.Label(temp_frame, text='ms / frame')
        self.temp_freq_label.grid(row=1, column=1, padx=5, sticky="w")

class ShowTempProgressFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowProgress", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.temp_progress = False
        self.progress_label = None
        self.setup_form()
    def setup_form(self):
        self.label = tk.Label(self,text='状況：')
        self.progress_label = tk.Label(self,text='未完了',foreground='#ff0000')
        self.label.grid(row=0,column=0,padx=5)
        self.progress_label.grid(row=0,column=1,padx=5)
    def change_progress_color(self,progress):
        if progress:
            self.progress_label.destroy()
            self.progress_label = tk.Label(self,text='完了',foreground='#00ff00')
            self.progress_label.grid(row=0,column=1,padx=5)

class SelectEoSFrame(tk.LabelFrame):
    def __init__(self, *args,header_name="PeakSeekFrame", **kwargs):
        super().__init__(text='③ 状態方程式の選択',*args, **kwargs)
        self.header_name = header_name
        self.EoS_name = None
        self.setup_form()
    def setup_form(self):
        self.grid_columnconfigure(0,weight=1)
        self.select_EoS = tk.StringVar()
        self.EoS_tuple = self.get_class_methods(setting.EoS)
        self.combobox = ttk.Combobox(self, state="readonly",values=self.EoS_tuple,width=25)
        self.progress_frame = ShowEoSProgressFrame(self)
        self.combobox.bind('<<ComboboxSelected>>',self.on_combobox_selected)
        self.combobox.grid(row=0,column=0)
        self.progress_frame.grid(row=1,column=0)
        
    @staticmethod
    def get_class_methods(cls):
        return tuple([func for func in dir(cls) if inspect.isfunction(getattr(cls, func))])

    def on_combobox_selected(self,event):
        self.progress_frame.EoS_progress = True
        self.progress_frame.change_progress_color(self.progress_frame.EoS_progress)
    
class ShowEoSProgressFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowProgress", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.EoS_progress = False
        self.progress_label = None
        self.setup_form()
    def setup_form(self):
        self.label = tk.Label(self,text='状況：')
        self.progress_label = tk.Label(self,text='未完了',foreground='#ff0000')
        self.label.grid(row=0,column=0,padx=5)
        self.progress_label.grid(row=0,column=1,padx=5)
    def change_progress_color(self,progress):
        if progress:
            self.progress_label.destroy()
            self.progress_label = tk.Label(self,text='完了',foreground='#00ff00')
            self.progress_label.grid(row=0,column=1,padx=5)
if __name__ == '__main__':
    app = tk.Tk()
    app.focus_force()

    app.geometry(setting.WINDOW_SIZE)
    tabs = ttk.Notebook(app)
    tabs.pack(expand=True,fill='both')
    phase_tab = PhaseTab(master=tabs)
    tabs.add(phase_tab,text='相図')
    app.mainloop()