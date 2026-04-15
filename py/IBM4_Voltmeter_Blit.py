import numpy as np
import tkinter as tk
from tkinter import ttk
import sys
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import IBM4_Lib
import threading as th

class App:
    """Define the application class."""
    def __init__(self,root=tk.Tk()):
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

        ### Initialising IBM4
        self.the_dev = IBM4_Lib.Ser_Iface() # find the first connected IBM4, open in DC mode by default

        ### Initialising dictionary and variables
        self.__channels = ['A2','A3','A4','A5','D2','GND']
        self.channelplus = tk.StringVar(value=self.__channels[0])
        self.channelmin = tk.StringVar(value=self.__channels[1])
        self.output_val = tk.StringVar(value='-.---')
        self.plot_data=[]
        self.run = None
        self.wait = tk.DoubleVar(value=2)
        self.xsize = 400
        self.xaxis = []

        ### Figure for the canvas
        self.fig = Figure(figsize = (5, 5),dpi = 100)
        self.vplot = self.fig.add_subplot(111)
        self.vplot.axis([1,self.xsize,0,3.5])
        self.line, = self.vplot.plot(self.xaxis,self.plot_data)
        #print(self.line,self.line[0])

        ### Frame 1: Combobox
        self.frame1 = ttk.LabelFrame(self.root,text="Select Channels")
        self.cbox1 = ttk.Combobox(self.frame1, textvariable=self.channelplus,values=self.__channels)
        self.cbox1.grid(row=1,column=0,columnspan=5,sticky='we')
        #self.cbox1.set(self.channelplus)
        ttk.Label(self.frame1,text='vs').grid(row=1,column=5,sticky='we')
        self.cbox2 = ttk.Combobox(self.frame1, textvariable=self.channelmin,values=self.__channels)
        self.cbox2.grid(row=1,column=6,columnspan=5,sticky='we')
        #self.cbox2.set(self.channelmin)
        self.frame1.grid(row=1,column=0,columnspan=15,sticky='we')

        ### Frame 1A: Repetition Rate
        self.frame1a = ttk.LabelFrame(self.root,text="Sample rate (Hz)")
        tk.Entry(self.frame1a, textvariable=self.wait, width=5).pack(fill=tk.BOTH, expand=1)
        self.frame1a.grid(row=2,column=0,columnspan=2,sticky='we')

        ### Frame 2: Output label
        self.frame2 = ttk.LabelFrame(self.root,text="Voltage")
        ttk.Label(self.frame2,textvariable=self.output_val).pack(fill=tk.BOTH, expand=1)
        self.frame2.grid(row=4,column=0,columnspan=2,sticky='we')

        ### Frame 3: Output plot
        self.frame3 = ttk.LabelFrame(self.root,text="Plot")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame3)
        self.canvas.draw()
        self.vplot.add_line(self.line)
        self.background = self.canvas.copy_from_bbox(self.vplot.bbox)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
        self.frame3.grid(row=10,column=0,rowspan=10,columnspan=10,sticky='we')

        # RUN and LIVEPLOT buttons
        self.run_button = ttk.Button(self.root, text="Run", command=self.run_begin)
        self.run_button.grid(row=30,column=0)
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_mode)
        self.stop_button.grid(row=30,column=2)
        self.stop_button.config(state=tk.DISABLED)

    def run_mode(self):
        self.plot_data=[]
        self.xaxis=[]
        i=1
        while self.run:
            tstart = time.monotonic()
            if self.channelplus.get()==self.__channels[5] and self.channelmin.get()==self.__channels[5]:
                self.channelplus.set(self.__channels[0])

            if self.channelplus.get()==self.__channels[5] or self.channelmin.get()==self.__channels[5]:
                if self.channelplus.get() ==self.__channels[5]:
                    voltage = self.the_dev.ReadAverageVoltage(self.channelmin.get())
                    voltage = -voltage
                    self.plot_data.append(voltage)
                    self.output_val.set(f'{voltage:.3f}')
                else:
                    voltage = self.the_dev.ReadAverageVoltage(self.channelplus.get())
                    self.plot_data.append(voltage)
                    self.output_val.set(f'{voltage:.3f}')
            else:
                diff_res = self.the_dev.DiffReadMultiple(self.channelplus.get(), self.channelmin.get())
                voltage = diff_res[0]
                self.plot_data.append(voltage)
                self.output_val.set(f'{voltage:.3f}')

            if len(self.plot_data) > self.xsize:
                self.plot_data = self.plot_data[-self.xsize:]
                self.line.set_ydata(self.plot_data)
            else:
                self.xaxis.append(i)
                i+=1
                self.line.set_data(self.xaxis,self.plot_data)

            #blit new data into old frame
            self.canvas.restore_region(self.background)
            self.vplot.draw_artist(self.line,)
            self.canvas.blit(self.vplot.bbox)

            tend = time.monotonic()
            deltat = tend-tstart
            self.output_val.set(f'{deltat:.3f}') # outputs deltat for performance testing

            if deltat < 1/self.wait.get():
                time.sleep(1/self.wait.get()-deltat)


    def run_begin(self):
        self.run_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        try:
            if self.my_thread.is_alive():
                #print("Closing previous thread.")
                self.my_thread.join()
                #print("Thread closed, starting acquisition.")
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

        self.run=False

        print("Terminating acquisition.")
        self.my_thread.join(timeout=.1)


if __name__ == "__main__":
    app = App()
    app.root.mainloop()
