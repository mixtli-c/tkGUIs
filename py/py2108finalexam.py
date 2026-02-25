import tkinter as tk
import tkinter.ttk as ttk
import random
import sys

class App:
    def __init__(self, root=tk.Tk()):
        self.root = root
        self.root.resizable(False, False)
        self.root.title('PY2018 Final Exam - Device Assignment')

        style = ttk.Style(root)
        style.theme_use('alt')

        self.ssid_dev={}
        self.filedatavars = {'SSIDs':'./AY2026_PY2108.txt','Devices':'./AF_Devices.txt'}
        self.SSIDdatavars = {'Please enter student ID (SSID)':''}
        self.students=set(ele.replace("\n","") for ele in open(self.filedatavars['SSIDs']).readlines())
        self.devices=set(ele.replace("\n","") for ele in open(self.filedatavars['Devices']).readlines())

        ### Menu
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Add items to the menu bar
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save", command=self.save_data)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.close_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        ### Frame 1: Load files
        self.frame1 = ttk.Frame(self.root)

        self.file_entries = LabelEntry(self.frame1,datavars=self.filedatavars,stacking='hv')
        self.loadSSID_button = ttk.Button(self.frame1, text="Load", command=self.load_ssids)
        self.loadSSID_button.grid(row=1,column=3)
        self.loadDEV_button = ttk.Button(self.frame1, text="Load", command=self.load_devs)
        self.loadDEV_button.grid(row=2,column=3)

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
        self.console_text = tk.Text(self.frame3, state='disabled', height=10)
        self.console_text.grid(row=2,column=0,rowspan=10,columnspan=15,sticky='we')

        self.frame3.grid(row=20,column=0,columnspan=15,sticky='we')

        # We redirect sys.stdout -> TextRedirector
        self.redirect_sysstd()
        #print(style.theme_names())

    def load_ssids(self):
        self.students=set(ele.replace("\n","") for ele in open(self.filedatavars['SSIDs'].get()).readlines())
        #print(self.students)

    def load_devs(self):
        self.devices=set(ele.replace("\n","") for ele in open(self.filedatavars['Devices'].get()).readlines())
        #print(self.devices)

    def assign_dev(self):
        self.loadSSID_button.config(state=tk.DISABLED)
        self.loadDEV_button.config(state=tk.DISABLED)
        try:
            ssid = self.SSIDdatavars['Please enter student ID (SSID)'].get()
            if ssid not in self.students:
                raise Exception('Not in student list.')
            print("Choosing device.")
            device = random.choice(list(self.devices))
            print("Device chosen.")
            print(f'Device {device} assigned to student {ssid}.')
            self.ssid_dev[ssid]=device
            self.devices = self.devices-{device}
            self.students = self.students-{ssid}

        except Exception as e:
            print('ERROR:',e)
            print('Try again.')

    def save_data(self):
        #data = []
        with open('assignments.txt', 'w') as f:
            for k,v in self.ssid_dev.items():
                f.write(f"{k}\t{self.ssid_dev[k]}\n")

            #print(self.ssid_dev, file=f)

    def close_app(self):
        self.save_data()
        self.root.quit()

    def redirect_sysstd(self):
        # We specify that sys.stdout point to TextRedirector
        sys.stdout = TextRedirector(self.console_text, "stdout")
        sys.stderr = TextRedirector(self.console_text, "stderr")

class LabelEntry:
    def __init__(self,place,datavars={'Entry':'0'},stacking='h'):
        i=1
        j=1
        for k,v in datavars.items():
            keyval = v
            #print(keyval)
            datavars[k]=tk.StringVar(value=keyval)
            if stacking == 'h':
                ttk.Label(place, text=k+':').grid(row=1,column=i,sticky='e')
                ttk.Entry(place, textvariable=datavars[k], width=30).grid(row=1,column=i+1,sticky='w')
            if stacking == 'hv':
                ttk.Label(place, text=k+':').grid(row=j,column=1,sticky='e')
                ttk.Entry(place, textvariable=datavars[k], width=30).grid(row=j,column=2,sticky='w')
            if stacking == 'v':
                ttk.Label(place, text=k+':').grid(row=i,column=0,sticky='w')
                ttk.Entry(place, textvariable=datavars[k], width=30).grid(row=i+1,column=0,sticky='w')
            i+=2
            j+=1

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
