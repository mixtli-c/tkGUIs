"""
plotter with a tkinter gui
"""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import random
import datetime as dt
fig = Figure(figsize = (5, 5),
                 dpi = 100)
plot1 = fig.add_subplot(111)
#g, = plot1.plot([i for i in range(20)])

def plot():

    # the figure that will contain the plot

    # list of squares
    p = random.randint(1,3)
    y = [i**p for i in range(20)]
    plot1.clear()
    # adding the subplot
    # plotting the graph
    #g.set_ydata(y)
    plot1.plot(y,label=dt.datetime.now().strftime("%H:%M:%S.%f") + ", p = %i" %p)
    plot1.legend()
    # creating the Tkinter canvas
    # containing the Matplotlib figure

    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack()

    #    creating the Matplotlib toolbar
    #toolbar = NavigationToolbar2Tk(canvas,
    #                               window)
    #toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

# the main Tkinter window
window = tk.Tk()
canvas = FigureCanvasTkAgg(fig,
                               master = window)
# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("500x500")

# button that displays the plot
plot_button = tk.Button(master = window,
                     command = plot,
                     height = 2,
                     width = 10,
                     text = "Plot")

# place the button
# in main window
plot_button.pack()

# run the gui
window.mainloop()
