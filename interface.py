import tkinter as tk 
from tkinter import messagebox 
#from (base de donnée) import (ta fonction)
#from (sécuritée) import (ta fonction)

class LoginWindow(tk.Tk) :
    def __init__(self) : 
        super().__init__()
        self.title("Connexion - Gestion financière")

        tk.Label(self, text="Email").grid(row=0, column=0)
        tk.Label(self, text="Mot de passe").grid(row=1, column=0)

        