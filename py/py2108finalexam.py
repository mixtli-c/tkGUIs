import tkinter as tk
import random

class App:
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.root.resizable(False, False)

        self.root.title('IBM4 Multimeter Mode')
        self.students=set()
        self.devices=set()
        self.ssid_dev={}
        self.filedatavars = {'SSIDs':'./AY2026_PY2108.txt','Devices':'./AF_Devices.txt'}
        self.SSIDdatavars = {'Please enter student ID (SSID)':''}

        ### Frame 1: Load files
        self.frame1 = ttk.Frame(self.root)

        self.file_entries = LabelEntry(self.frame1,datavars=self.filedatavars)
        self.loadSSID_button = ttk.Button(self.frame1, text="Load", command=self.load_ssids)
        self.loadSSID_button.grid(row=1,column=3)
        self.loadDEV_button = ttk.Button(self.frame1, text="Load", command=self.load_devs)
        self.loadDEV_button.grid(row=3,column=3)

        self.frame1.grid(row=1,column=0,columnspan=15,sticky='we')

        ### Frame 2: Input SSID
        self.frame2 = ttk.Frame(self.root)

        self.SSID_entry = LabelEntry(self.frame2,datavars=self.SSIDdatavars,stacking='v')
        self.assign_button = ttk.Button(self.frame2, text="Assign Device", command=self.assign_dev)
        self.assign_button.grid(row=2,column=2)

        self.frame2.grid(row=5,column=0,columnspan=15,sticky='we')

        ### Frame 3: Text output
        self.frame3 = ttk.Frame(self.root)

        # Add windows where we are going to write the std output.
        self.console_text = tk.Text(self.frame2, state='disabled', height=10)
        self.console_text.grid(row=2,column=0,rowspan=10,columnspan=15,sticky='we')

        self.frame3.grid(row=20,column=0,columnspan=15,sticky='we')

        # We redirect sys.stdout -> TextRedirector
        self.redirect_sysstd()

    def load_ssids(self):
        self.students=set(open(self.filedatavars['SSIDS']).readlines())

    def load_devs(self):
        self.devices=set(open(self.filedatavars['Devices']).readlines())

    def assign_dev(self):

    def redirect_sysstd(self):
        # We specify that sys.stdout point to TextRedirector
        sys.stdout = TextRedirector(self.console_text, "stdout")
        sys.stderr = TextRedirector(self.console_text, "stderr")

class LabelEntry:
    def __init__(self,place,datavars={'Entry':'0'},stacking='h'):
        i=1
        for k,v in datavars.items():
            keyval = v
            #print(keyval)
            datavars[k]=tk.StringVar(value=keyval)
            if stacking == 'h'
                ttk.Label(place, text=k+':').grid(row=1,column=i,sticky='e')
                ttk.Entry(place, textvariable=datavars[k], width=10).grid(row=1,column=i+1,sticky='w')
            if stacking == 'v'
                ttk.Label(place, text=k+':').grid(row=i,column=1,sticky='e')
                ttk.Entry(place, textvariable=datavars[k], width=10).grid(row=i+1,column=2,sticky='w')
            i+=2

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

if __name__ == "__main__":
    app = App()
    app.root.mainloop()
