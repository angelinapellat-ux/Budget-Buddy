import tkinter as tk
from tkinter import ttk, messagebox


#fenetre d'inscription
class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Inscription")
        self.geometry("400x350")
        self.resizable(False, False)

        #visuel
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

        #fonction pour vérifier la sécurité du mot de passe, hasher le mot de passe et insérer dans la base
        #
        # if success:
        #     messagebox.showinfo("OK", "Compte créé")
        #     self.destroy()
        # else:
        #     messagebox.showerror("Erreur", "Email déjà utilisé")

        messagebox.showinfo("Info", "Fonction d'inscription à implémenter par vos collègues.")


#fenetre de connexion
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

    def login(self):
        email = self.email_var.get()
        pwd = self.pwd_var.get()

        #fonction ici pour récupérer l'utilisateur par email et vérifier le hash du mot de passe
        #
        # if user:
        #     self.destroy()
        #     MainApp(user_id=user["id"])
        # else:
        #     messagebox.showerror("Erreur", "Identifiants incorrects")
       
        messagebox.showinfo("Info", "Fonction de connexion à implémenter par vos collègues.")

    def open_register(self):
        RegisterWindow(self)


#fenetre principale
class MainApp(tk.Tk):
    def __init__(self, user_id):
        super().__init__()
        self.title("Gestion Financière")
        self.geometry("600x400")

        tk.Label(self, text=f"Bienvenue utilisateur {user_id}", font=("Arial", 16)).pack(pady=20)
        tk.Label(self, text="Ici viendra l'interface principale").pack()

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
