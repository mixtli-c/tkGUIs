import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
root = tk.Tk()
data, = plt.plot([0,5,3,4,-5,3])
canvas = FigureCanvasTkAgg(plt.gcf(), master=root)
invert = lambda: (data.set_ydata(-data.get_ydata()), canvas.draw())
tk.Button(master=root, text="Invert", command=invert).pack()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
root.protocol("WM_DELETE_WINDOW", lambda: (root.quit(), root.destroy()))
root.mainloop()
