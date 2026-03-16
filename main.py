import tkinter as tk
from tkinter import messagebox

# On importe les fenêtres et la logique depuis tes autres fichiers
from interface import RegisterWindow
from dashboard import DashboardWindow
from user_account import UserAccount

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy - Connexion")
        self.geometry("350x300")
        self.resizable(False, False)

        # Widgets de connexion
        tk.Label(self, text="Email").pack(pady=10)
        self.email_login = tk.StringVar()
        tk.Entry(self, textvariable=self.email_login).pack()

        tk.Label(self, text="Mot de passe").pack(pady=10)
        self.pwd_login = tk.StringVar()
        tk.Entry(self, textvariable=self.pwd_login, show="*").pack()

        tk.Button(self, text="Se connecter", command=self.login_action, width=15, bg="#2196F3", fg="white").pack(pady=10)
        tk.Button(self, text="S'inscrire", command=self.open_register).pack()

    def login_action(self):
        email = self.email_login.get()
        pwd = self.pwd_login.get()
        
        # On appelle la méthode statique de user_account.py
        if UserAccount.login(email, pwd):
            messagebox.showinfo("Succès", "Bienvenue sur votre gestionnaire !")
            self.withdraw() # On cache le login
            DashboardWindow(self, email) # On lance le Dashboard
        else:
            messagebox.showerror("Échec", "Email ou mot de passe incorrect.")

    def open_register(self):
        # On lance la fenêtre d'inscription de interface.py
        RegisterWindow(self)

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()