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

        tk.Label(self, text="Mot de passe").pack(pady=5)
        self.pwd_var = tk.StringVar()
        tk.Entry(self, textvariable=self.pwd_var, show="*").pack()

        tk.Label(self, text="Confirmer le mot de passe").pack(pady=5)
        self.pwd_confirm_var = tk.StringVar()
        tk.Entry(self, textvariable=self.pwd_confirm_var, show="*").pack()

        tk.Button(self, text="Créer un compte", command=self.register).pack(pady=20)

        def register(self):
        nom = self.nom_var.get()
        prenom = self.prenom_var.get()
        email = self.email_var.get()
        pwd = self.pwd_var.get()
        pwd_confirm = self.pwd_confirm_var.get()

        if pwd != pwd_confirm:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return

         # Appeler votre fonction pour vérifier la sécurité du mot de passe, hasher le mot de passe et insérer dans la base

         # if success:
         #     messagebox.showinfo("OK", "Compte créé")
         #     self.destroy()
         # else:
         #     messagebox.showerror("Erreur", "Email déjà utilisé")
       
#fenetre connection
class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Connexion - Gestion Financière")
        self.geometry("350x250")
        self.resizable(False, False)
        
        tk.Label(self, text="Email").pack(pady=10)
        self.email_var = tk.StringVar()
        tk.Entry(self, textvariable=self.email_var).pack()

        tk.Label(self, text="Mot de passe").pack(pady=10)
        self.pwd_var = tk.StringVar()
        tk.Entry(self, textvariable=self.pwd_var, show="*").pack()

        tk.Button(self, text="Se connecter", command=self.login).pack(pady=15)
        tk.Button(self, text="Créer un compte", command=self.open_register).pack()