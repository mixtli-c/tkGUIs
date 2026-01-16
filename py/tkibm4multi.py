import numpy as np
import tkinter as tk
import sys
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import IBM4_Lib

class App:
    """Define the application class."""
    def __init__(self,root):
        self.root = root
        self.root.title('IBM4 Multimeter Mode')

        self.radio = Radiobutton(self,'ID;Set A0;Set A1;Set PWM;Ground all outputs;Read all inputs', 'print(self.mssg)')
        # Add windows where we are going to write the std output.
        self.console_text = tk.Text(self.root, state='disabled', height=10)
        self.console_text.grid(row=2,column=0,rowspan=10,columnspan=10)

        # We redirect sys.stdout -> TextRedirector
        self.redirect_sysstd()

        # We add a button to test our setup
        self.test_button = tk.Button(self.root, text="Run", command=self.run_mode)
        self.test_button.grid(row=12,column=1)

        self.entryval = tk.StringVar()
        tk.Label(text='Parameter').grid(row=12,column=)
        tk.Entry(root, textvariable=self.entryval, width=10).grid(row=12,column=4)

    def redirect_sysstd(self):
        # We specify that sys.stdout point to TextRedirector
        sys.stdout = TextRedirector(self.console_text, "stdout")
        sys.stderr = TextRedirector(self.console_text, "stderr")

    def run_mode(self):
        print('Now running: '+self.radio.item)
        action = self.radio.val.get()
        ## ADAPTED FROM ROBS MULTIMETER MODE, NOT YET USABLE
        the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default
        if action == 0:
            the_dev.IDNPrompt()
        elif action == 1:
            self.WriteVoltage('A0', float(self.entryval))
        elif action == 3:
            self.VoltOutputPrompt('A1')
        elif action == 4:
            self.PWMPrompt()
        elif action == 5:
            self.GroundIBM4Prompt()
        elif action == 6:
            self.ReadInputsPrompt()
        elif action == 7:
            self.DiffReadPrompt()
        del the_dev # destructor for the IBM4 object, closes comms


class Radiobutton:
    """Create a list-based Radiobutton object."""

    def __init__(self, App, items='Radiobutton', cmd='', val=0, **kwargs):
        self.items = items.split(';')
        self.cmd = cmd
        self.val = tk.IntVar()
        self.val.set(val)
        for i, item in enumerate(self.items):
            r = tk.Radiobutton(App.root, text=item, variable=self.val,
                                value=i, command=self.cb, **kwargs)
            r.grid(row=1,column=i,sticky='w')
            #r.pack(side=tk.LEFT)
    def cb(self):
        """Evaluate the cmd string in the Radiobutton context."""
        self.item = self.items[self.val.get()]
        self.mssg = 'Mode '+self.item+' selected'
        exec(self.cmd)

class TextRedirector(object):
    def __init__(self, widget, tag):
        self.widget = widget
        self.tag = tag

    def write(self, text):
        self.widget.configure(state='normal') # Edit mode
        self.widget.insert(tk.END, text, (self.tag,)) # insert new text at the end of the widget
        self.widget.configure(state='disabled') # Static mode
        self.widget.see(tk.END) # Scroll down
        self.widget.update_idletasks() # Update the console

    def flush(self):
        pass

root = tk.Tk()
app = App(root)
root.mainloop()
