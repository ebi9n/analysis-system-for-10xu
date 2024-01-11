import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import messagebox

import tkinter as tk
from tkinter import ttk
import GUI_TempTab as TempTab
import GUI_PhaseTab as PhaseTab
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
        self.phase_tab = PhaseTab.PhaseTab(master= self.tabs)
        self.tabs.add(self.phase_tab, text='圧力計算')
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
    