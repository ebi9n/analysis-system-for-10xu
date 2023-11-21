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

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_form()

    def setup_form(self):
        self.geometry("600x800")
        self.title('HLA')
       
        # タブを生成する
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill='both')
        self.temp_tab = TempTab(master=self.tabs)
        self.tabs.add(self.temp_tab, text='温度計算')
        self.XRD_tab = XRDTab(master= self.tabs)
        self.tabs.add(self.XRD_tab, text='XRD時系列')

class TempTab(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_form()

    def setup_form(self):
        
        self.read_dist_frame = ReadDistFrame(master=self)
        self.show_dist_color_map_frame = ShowColorMapFrame(master=self)
        self.read_dist_frame.grid(row=0, column=0)
        self.show_dist_color_map_frame.grid(row=1,column=0)

class ReadDistFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadDistFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.label = tk.Label(self, text='distファイルの読み込み')
        self.label.grid(row=0, column=0, padx=10,sticky="w")
        
        # ファイル名を指定するテキストボックス
        self.textbox = tk.Entry(self, width=65)
        self.textbox.insert(0,'dist ファイルのpathを入力')
        self.textbox.grid(row=1, column=0, padx=10, pady=(0,10), sticky="ew")
        
        # ファイルパスを指定するボタン
        self.browse_button = tk.Button(self,text='ファイルを参照',command=self.browse_dist_file)
        self.browse_button.grid(row=1,column=1,padx=10, pady=(0,10))
        
        # ファイルを開くボタン
        self.open_button = tk.Button(self,text='　開く　')
        self.open_button.grid(row=1,column=2,padx=10, pady=(0,10))
    
    @staticmethod
    def browse_dist_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        temp_dist_path = file_path
        if file_path:
            print("選択されたファイル:", file_path)
    
class ShowColorMapFrame(tk.Frame):
    def __init__(self, *args, header_name="ShowColorMapFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()
        
    def setup_form(self):
        self.label = tk.Label(self, text='test')
        self.label.grid(row=0, column=0, padx=10,sticky="w")

class XRDTab(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.setup_form()
    def setup_form(self):
        self.read_XRDdat_frame = ReadXRDdatFrame(master=self)
        self.read_XRDdat_frame.grid(row=0, column=0)

class ReadXRDdatFrame(tk.Frame):
    def __init__(self, *args, header_name="ReadDistFrame", **kwargs):
        super().__init__(*args, **kwargs)
        self.header_name = header_name
        self.setup_form()

    def setup_form(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.test_label = tk.Label(self, text='test')
        self.test_label.grid(row=0, column=0, padx=20)

if __name__ == '__main__':
    app = App()
    app.mainloop()