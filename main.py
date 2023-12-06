import tkinter as tk
from tkinter import filedialog
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from natsort import natsorted
from tkinter import ttk
from tkinter import messagebox

import tkinter as tk
from tkinter import ttk
import GUI_XRDTab as XRDTab
import GUI_TempTab as TempTab
import setting


WINDOW_TITLE = setting.WINDOW_TITLE
WINDOW_SIZE = setting.WINDOW_SIZE
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.setup_form()

    def setup_form(self):
        self.geometry(WINDOW_SIZE)
        self.title(WINDOW_TITLE)
       
        # タブを生成する
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill='both')
        self.temp_tab = TempTab.TempTab(master=self.tabs)
        self.tabs.add(self.temp_tab, text='温度計算')
        self.XRD_tab = XRDTab.XRDTab(master= self.tabs)
        self.tabs.add(self.XRD_tab, text='XRD時系列')
        self.protocol("WM_DELETE_WINDOW", self.delete_window)
    
    def delete_window(self):
        print("ウィンドウのxボタンが押された")

        # 終了確認のメッセージ表示
        ret = messagebox.askyesno(
            title = "終了確認",
            message = "プログラムを終了しますか？")

        if ret == True:
            # 「はい」がクリックされたとき
            plt.close("all")
            self.destroy()
    

if __name__ == '__main__':
    app = App()
    app.mainloop()
    