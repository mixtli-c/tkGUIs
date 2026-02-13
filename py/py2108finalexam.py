import tkinter as tk
import random

class App:
    def __init__(self, root=tk.Tk()):
        List = open("filename.txt").readlines()
        self.students={}
        self.devices={}

