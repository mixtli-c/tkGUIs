import tkinter as tk
from tkinter import Menu

# Initialize the main window
root = tk.Tk()
root.title("Simple Text Editor")

# Create a menu bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Add items to the menu bar
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New")
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Create a frame for the text area and status bar
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a text widget for the text area
text_area = tk.Text(main_frame)
text_area.pack(expand=True, fill=tk.BOTH)

# Create a status bar
status_bar = tk.Label(main_frame, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Set a minimum size for the window to ensure the menu is always visible
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()
