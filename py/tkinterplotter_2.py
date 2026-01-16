import numpy as np
import tkinter as tk
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Radiobutton:
    """Create a list-based Radiobutton object."""

    def __init__(self, App, items='Radiobutton', cmd='', val=0, **kwargs):
        self.items = items.split(';')
        self.cmd = cmd
        self.val = tk.IntVar()
        self.val.set(val)
        for i, item in enumerate(self.items):
            r = ttk.Radiobutton(App.root, text=item, variable=self.val,
                                value=i, command=self.cb, **kwargs)
            r.grid(row=1,column=i,sticky='w')

    def cb(self):
        """Evaluate the cmd string in the Radiobutton context."""
        self.item = self.items[self.val.get()]
        exec(self.cmd)


class App:
    """Define the application class."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('IBM4 Multimeter Mode')

        Radiobutton(self,'ID;Set A0;Set A1;Set PWM;Ground all outputs;Read all inputs', 'print(self.val)')

    def run(self):
        """Run the main loop."""
        self.root.mainloop()




app=App()
print(app.root)
app.run()
