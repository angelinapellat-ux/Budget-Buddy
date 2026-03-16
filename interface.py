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

        #Visuel
        tk.Label(self, text="Nom").pack(pady=5)
        self.nom_var = tk.StringVar()
        tk.Entry(self, textvariable=self.nom_var).pack()

        tk.Label(self, text="Prénom").pack(pady=5)
        self.prenom_var = tk.StringVar()
        tk.Entry(self, textvariable=slef.prenom_var).pack()

        tk.Label(self, text="Email").pack(pady=5)
        self.prenom_var = tk.StringVar()
        tk.Entry(self, textvariable=slef.email_var).pack()