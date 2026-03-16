import tkinter as tk
from tkinter import messagebox
from user_account import UserAccount
from dashboard import DashboardWindow

class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inscription")
        self.geometry("400x450")
        self.resizable(False, False)

        tk.Label(self, text="Nom").pack(pady=5)
        self.nom_var = tk.StringVar()
        tk.Entry(self, textvariable=self.nom_var).pack()

        tk.Label(self, text="Prénom").pack(pady=5)
        self.prenom_var = tk.StringVar()
        tk.Entry(self, textvariable=self.prenom_var).pack()

        tk.Label(self, text="Email").pack(pady=5)
        self.email_var = tk.StringVar()
        tk.Entry(self, textvariable=self.email_var).pack()

        tk.Label(self, text="Mot de passe").pack(pady=5)
        self.pwd_var = tk.StringVar()
        tk.Entry(self, textvariable=self.pwd_var, show="*").pack()

        tk.Label(self, text="Confirmer").pack(pady=5)
        self.pwd_confirm_var = tk.StringVar()
        tk.Entry(self, textvariable=self.pwd_confirm_var, show="*").pack()

        tk.Button(self, text="Créer un compte", command=self.register, bg="#4CAF50", fg="white").pack(pady=20)

    def register(self):
        if self.pwd_var.get() != self.pwd_confirm_var.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas")
            return

        if not UserAccount.validate_password_strength(self.pwd_var.get()):
            messagebox.showerror("Sécurité", "Mot de passe trop faible (10 car. min, Maj, Chiffre, Spécial)")
            return

        new_user = UserAccount(self.nom_var.get(), self.prenom_var.get(), self.email_var.get(), self.pwd_var.get())
        if new_user.register():
            messagebox.showinfo("Succès", f"Compte créé pour {self.prenom_var.get()} !")
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Email déjà utilisé ou problème serveur.")

