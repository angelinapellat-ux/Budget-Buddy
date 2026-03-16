import tkinter as tk 
from tkinter import messagebox 
#from (base de donnée) import (ta fonction)
#from (sécuritée) import (ta fonction)

class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inscription")
        self.geometry("400x350")
        self.resizable(False, False)