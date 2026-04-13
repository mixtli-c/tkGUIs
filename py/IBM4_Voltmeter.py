import numpy as np
import tkinter as tk
from tkinter import ttk
import sys
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import IBM4_Lib

class App:
    """Define the application class."""
    def __init__(self,root):
        self.root = root
        self.root.resizable(False, False)
        ### The following grid_columnconfigure statemets make all the columns to belong to the same group, will have the
        ### size of the largest widget
        #self.root.grid_columnconfigure(0, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(1, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(2, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(3, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(4, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(5, weight=1, uniform="fred")
        #self.root.grid_columnconfigure(6, weight=1, uniform="fred")
        self.root.title('IBM4 Live Voltmeter')
        self.p = None

        ### Initialising IBM4
        self.the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

        ### Initialising dictionary and variables
        self.__channels = ['A2','A3','A4','A5','D2']
        self.channelplus = self.__channels[0]
        self.channelmin = self.__channels[1]
        self.output_val = tk.StringVar(value='--.----')

        ### Frame 1: Combobox
        self.frame1 = ttk.LabelFrame(self.root,text="Select Channels")
        ttk.Combobox(self.frame1, textvariable=self.channelplus,values=self.__channels).grid(row=1,column=0,columnspan=15,sticky='we')
        ttk.Label(self.frame1,text='vs').grid(row=1,column=1,columnspan=8,sticky='we')
        ttk.Combobox(self.frame1, textvariable=self.channelmin,values=self.__channels).grid(row=1,column=2,columnspan=15,sticky='we')
        self.frame1.grid(row=1,column=0,columnspan=15,sticky='we')

        ### Frame 2: Output label
        self.frame2 = ttk.LabelFrame(self.root,text="Voltage")
        self.output = ttk.Label(self.frame2,textvariable=self.output_val)
        self.frame2.grid(row=2,column=1,columnspan=3,sticky='we')

        ### Frame 3: Output label
        self.frame3 = ttk.LabelFrame(self.root,text="Voltage")
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame3)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.frame3.grid(row=3,column=1,rowspan=10,sticky='we')

        # RUN and LIVEPLOT buttons
        self.run_button = ttk.Button(self.root, text="Run", command=self.run_begin).grid(row=15,column=0)
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_mode).grid(row=15,column=2)
        self.stop_button.config(state=tk.DISABLED)

    def run_mode(self):
        print('Now running: '+self.radio.item)
        action = self.radio.val.get()
        ## ADAPTED FROM ROBS MULTIMETER MODE
        if action == 0:
            self.the_dev.IDNPrompt()
        elif action == 1:
            self.the_dev.WriteVoltage('A0', float(self.voutval.get()))
        elif action == 2:
            self.the_dev.WriteVoltage('A1', float(self.voutval.get()))
        elif action == 3:
            self.the_dev.WritePWM(float(self.pwmpc.get()))
        elif action == 4:
            self.the_dev.ZeroIBM4()
        elif action == 5:
            ch_vals = self.the_dev.ReadAverageVoltageAllChnnl()
            print('AI voltages: ',ch_vals)
        elif action == 6:
            chns = self.diffch.get().split(',')
            diff_res = self.the_dev.DiffReadMultiple(chns[0], chns[1])
            print('Differential Read Value = %(v1)0.3f +/- %(v2)0.3f (V)'%{"v1":diff_res[0], "v2":diff_res[1]})
        #del the_dev # destructor for the IBM4 object, closes comms

    def run_begin(self):
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        try:
            if self.my_thread.is_alive():
                print("Closing previous thread.")
                self.my_thread.join()
                print("Thread closed, starting acquisition.")
            else:
                print("Starting acquisition.")
        except:
            print("Starting acquisition.")
        self.run = True
        self.my_thread = th.Thread(target=self.run_mode)
        self.my_thread.start()

    def stop_mode(self):
        self.run_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        try:
            self.p.terminate()
        except:
            print("No subprocess to terminate?")

        self.run=False

        print("Terminating acquisition.")
        self.my_thread.join(timeout=.1)


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
