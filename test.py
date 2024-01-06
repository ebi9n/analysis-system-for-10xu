import tkinter as tk

def open_toplevel():
    top = tk.Toplevel()
    print("Toplevel master:", top.master)

root = tk.Tk()
button = tk.Button(root, text="Open Toplevel", command=open_toplevel)
button.pack()

root.mainloop()