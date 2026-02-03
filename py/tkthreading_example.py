import tkinter as tk
import threading as th
import time

class App:

    def __init__(self):
        self.root = tk.Tk()

        self.run = True
        self.counter = 0

    def build(self):
        self.counter_label = tk.Label(text=self.counter)
        self.counter_label.pack()

        self.stop_button = tk.Button(text='stop', command=self.stop_counter)
        self.stop_button.pack()
        self.start_button = tk.Button(text='start', command=self.run_counter)
        self.start_button.pack()

    def start_counter(self):
        while self.run:
            self.counter += 1
            self.counter_label.configure(text=self.counter)
            time.sleep(1)

    def run_counter(self):
        self.run=True
        self.my_thread = th.Thread(target=self.start_counter) # create new thread that runs the self.start_counter() function
        self.my_thread.start() # start the threading

    def stop_counter(self):
        self.counter_label.configure(text="counter stopped")
        self.run = False # set the variable to false so that the while loop inside the threading stops
        self.my_thread.join() # this destoy the created threading

    def start_loop(self):
        self.root.mainloop() # starts the tkinter mainloop

app = App()
app.build()

#app.run_counter()

app.start_loop()
