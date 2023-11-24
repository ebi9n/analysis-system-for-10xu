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