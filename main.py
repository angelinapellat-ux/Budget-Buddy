import tkinter as tk
from tkinter import messagebox
import json
import os
from user_account import UserAccount
from dashboard import DashboardWindow

CONFIG_FILE = ".session_data.json"

class BudgetBuddyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Panel de Connexion")
        self.geometry("400x650")
        self.iconbitmap("asset/logo.ico")
        self.configure(bg="#F8F9FE") # Fond gris clair moderne
        
        # Style de la carte centrale (Card Design)
        self.card = tk.Frame(self, bg="white", highlightthickness=1, highlightbackground="#E9ECEF")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=580)
        
        self.show_login()

    def show_login(self):
        """Affiche l'interface de connexion."""
        for w in self.card.winfo_children(): w.destroy()
        
        tk.Label(self.card, text="Bienvenue", font=("Segoe UI", 22, "bold"), bg="white", fg="#32325D").pack(pady=(40, 5))
        tk.Label(self.card, text="Connectez-vous pour continuer", font=("Segoe UI", 10), bg="white", fg="#8898AA").pack(pady=(0, 30))
        
        self.e_log = self.create_input("EMAIL", "ex: jean@mail.com")
        self.p_log = self.create_input("MOT DE PASSE", "••••••••", True)

        # Se souvenir de moi
        self.remember_var = tk.BooleanVar()
        check = tk.Checkbutton(self.card, text="Se souvenir de moi", variable=self.remember_var, 
                               bg="white", activebackground="white", fg="#525F7F", 
                               font=("Segoe UI", 9), cursor="hand2")
        check.pack(anchor="w", padx=35, pady=10)

        # Chargement des identifiants sauvegardés
        saved_data = self.load_credentials()
        if saved_data:
            self.e_log.set(saved_data.get("email", ""))
            self.p_log.set(saved_data.get("password", ""))
            self.remember_var.set(True)

        self.create_button("SE CONNECTER", "#5E72E4", self.handle_login)
        
        tk.Label(self.card, text="Pas encore de compte ?", bg="white", fg="#8898AA", font=("Segoe UI", 9)).pack(pady=(20, 0))
        tk.Button(self.card, text="Créer un compte gratuitement", command=self.show_register, 
                  bg="white", fg="#5E72E4", relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2").pack()

    def show_register(self):
        """Affiche l'interface d'inscription."""
        for w in self.card.winfo_children(): w.destroy()
        
        tk.Label(self.card, text="Inscription", font=("Segoe UI", 20, "bold"), bg="white", fg="#32325D").pack(pady=30)
        
        self.n_reg = self.create_input("NOM")
        self.pr_reg = self.create_input("PRÉNOM")
        self.em_reg = self.create_input("EMAIL")
        self.pw_reg = self.create_input("MOT DE PASSE", "", True)
        
        self.create_button("CRÉER MON COMPTE", "#2DCE89", self.handle_register)
        
        tk.Button(self.card, text="Retour à la connexion", command=self.show_login, 
                  bg="white", fg="#8898AA", relief="flat", font=("Segoe UI", 9)).pack(pady=10)

    def create_input(self, label, placeholder="", is_pwd=False):
        """Génère un champ de saisie stylisé."""
        f = tk.Frame(self.card, bg="white")
        f.pack(fill="x", padx=35, pady=8)
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        v = tk.StringVar()
        e = tk.Entry(f, textvariable=v, show="●" if is_pwd else "", bg="#FFFFFF", 
                     relief="flat", highlightthickness=1, highlightbackground="#CAD1D7", 
                     font=("Segoe UI", 10), fg="#32325D")
        e.pack(fill="x", ipady=8)
        
        e.bind("<FocusIn>", lambda event: e.configure(highlightbackground="#5E72E4"))
        e.bind("<FocusOut>", lambda event: e.configure(highlightbackground="#CAD1D7"))
        return v

    def create_button(self, text, color, command):
        """Génère un bouton stylisé avec effet de survol."""
        btn = tk.Button(self.card, text=text, command=command, bg=color, fg="white", 
                        font=("Segoe UI", 10, "bold"), relief="flat", height=2, cursor="hand2", bd=0)
        btn.pack(fill="x", padx=35, pady=20)
        
        btn.bind("<Enter>", lambda e: btn.config(background='#32325D'))
        btn.bind("<Leave>", lambda e: btn.config(background=color))
        return btn

    def handle_login(self):
        email = self.e_log.get()
        password = self.p_log.get()
        
        if UserAccount.login(email, password):
            if self.remember_var.get():
                self.save_credentials(email, password)
            else:
                if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
            
            self.withdraw() # Cache la fenêtre de login
            DashboardWindow(self, email)
        else: 
            messagebox.showerror("Accès refusé", "L'email ou le mot de passe est incorrect.")

    def handle_register(self):
        if not all([self.n_reg.get(), self.pr_reg.get(), self.em_reg.get()]):
            messagebox.showwarning("Incomplet", "Veuillez remplir tous les champs.")
            return

        if not UserAccount.validate_password_strength(self.pw_reg.get()):
            messagebox.showwarning("Sécurité", "Mot de passe trop faible (10 car., Maj, Min, Chiffre, Symbole)")
            return
            
        user = UserAccount(self.n_reg.get(), self.pr_reg.get(), self.em_reg.get(), self.pw_reg.get())
        if user.register():
            messagebox.showinfo("Succès", "Votre compte a été créé ! Connectez-vous maintenant.")
            self.show_login()
        else:
            messagebox.showerror("Erreur", "L'inscription a échoué (Email déjà utilisé ?)")

    def save_credentials(self, email, password):
        with open(CONFIG_FILE, "w") as f: 
            json.dump({"email": email, "password": password}, f)

    def load_credentials(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f: return json.load(f)
            except: return None
        return None

if __name__ == "__main__":
    app = BudgetBuddyApp()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        # On ignore l'erreur et on ferme proprement
        pass