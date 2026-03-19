import tkinter as tk
from tkinter import messagebox
import json, os
from user_account import UserAccount
from dashboard import DashboardWindow

CONFIG_FILE = "session_data.json"

class BudgetBuddyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Budget Buddy - Connexion")
        self.geometry("400x650")
        try: self.iconbitmap("asset/logo.ico")
        except: pass
        self.configure(bg="#F8F9FE")
        
        # Carte centrale
        self.card = tk.Frame(self, bg="white", highlightthickness=1, highlightbackground="#E9ECEF")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=580)
        
        self.show_login()

    def create_input(self, label, is_pwd=False):
        """Génère un champ de saisie stylisé avec gestion du focus."""
        f = tk.Frame(self.card, bg="white")
        f.pack(fill="x", padx=35, pady=8)
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        
        v = tk.StringVar()
        e = tk.Entry(f, textvariable=v, show="●" if is_pwd else "", bg="white", 
                     relief="flat", highlightthickness=1, highlightbackground="#CAD1D7", 
                     font=("Segoe UI", 10), fg="#32325D")
        e.pack(fill="x", ipady=8)
        
        # Effets visuels focus
        e.bind("<FocusIn>", lambda _: e.configure(highlightbackground="#5E72E4"))
        e.bind("<FocusOut>", lambda _: e.configure(highlightbackground="#CAD1D7"))
        return v

    def create_button(self, text, color, cmd, pady=20):
        """Génère un bouton avec effet de survol."""
        b = tk.Button(self.card, text=text, command=cmd, bg=color, fg="white", 
                      font=("Segoe UI", 10, "bold"), relief="flat", height=2, cursor="hand2")
        b.pack(fill="x", padx=35, pady=pady)
        b.bind("<Enter>", lambda _: b.config(bg='#32325D'))
        b.bind("<Leave>", lambda _: b.config(bg=color))
        return b

    def show_login(self):
        for w in self.card.winfo_children(): w.destroy()
        
        tk.Label(self.card, text="Bienvenue", font=("Segoe UI", 22, "bold"), bg="white", fg="#32325D").pack(pady=(40, 5))
        tk.Label(self.card, text="Connectez-vous pour continuer", font=("Segoe UI", 10), bg="white", fg="#8898AA").pack(pady=(0, 30))
        
        self.e_log = self.create_input("EMAIL")
        self.p_log = self.create_input("MOT DE PASSE", True)

        self.remember_var = tk.BooleanVar()
        tk.Checkbutton(self.card, text="Se souvenir de moi", variable=self.remember_var, 
                       bg="white", font=("Segoe UI", 9), cursor="hand2").pack(anchor="w", padx=35)

        # Auto-remplissage email
        saved = self.load_creds()
        if saved:
            self.e_log.set(saved); self.remember_var.set(True)

        self.create_button("SE CONNECTER", "#5E72E4", self.handle_login)
        
        tk.Button(self.card, text="Créer un compte", command=self.show_register, 
                  bg="white", fg="#5E72E4", relief="flat", font=("Segoe UI", 9, "bold")).pack()

    def show_register(self):
        for w in self.card.winfo_children(): w.destroy()
        tk.Label(self.card, text="Inscription", font=("Segoe UI", 20, "bold"), bg="white", fg="#32325D").pack(pady=30)
        
        self.n_reg = self.create_input("NOM")
        self.pr_reg = self.create_input("PRÉNOM")
        self.em_reg = self.create_input("EMAIL")
        self.pw_reg = self.create_input("MOT DE PASSE", True)
        
        self.create_button("CRÉER MON COMPTE", "#2DCE89", self.handle_register)
        tk.Button(self.card, text="Retour", command=self.show_login, bg="white", fg="#8898AA", relief="flat").pack()

    def handle_login(self):
        em, pw = self.e_log.get().strip(), self.p_log.get().strip()
        if not em or not pw: return messagebox.showwarning("Erreur", "Champs vides")

        if UserAccount.login(em, pw):
            self.save_creds(em) if self.remember_var.get() else (os.remove(CONFIG_FILE) if os.path.exists(CONFIG_FILE) else None)
            self.withdraw()
            DashboardWindow(self, em)
        else:
            messagebox.showerror("Accès refusé", "Identifiants incorrects")

    def handle_register(self):
        # 1. Récupération des données (data[2] est l'email)
        data = [
            self.n_reg.get().strip(), 
            self.pr_reg.get().strip(), 
            self.em_reg.get().strip(), 
            self.pw_reg.get().strip()
        ]

        # 2. Vérification "Champs vides"
        if not all(data): 
            return messagebox.showwarning("Erreur", "Tous les champs sont obligatoires.")

        # 3. VERIFICATION EMAIL (La partie qui te manquait)
        if not UserAccount.validate_email(data[2]):
            return messagebox.showerror("Format Invalide", "L'adresse email n'est pas correcte (ex: nom@domaine.com).")

        # 4. Vérification détaillée du Mot de Passe
        pwd = data[3]
        if len(pwd) < 10:
            return messagebox.showwarning("Sécurité", "Le mot de passe doit faire au moins 10 caractères.")
        if not any(c.isupper() for c in pwd):
            return messagebox.showwarning("Sécurité", "Ajoutez au moins une MAJUSCULE.")
        if not any(c.isdigit() for c in pwd):
            return messagebox.showwarning("Sécurité", "Ajoutez au moins un CHIFFRE.")
        # Utilise re.search pour les caractères spéciaux si tu as importé 're'
        import re
        if not re.search(r"[!@#$%^&*]", pwd):
            return messagebox.showwarning("Sécurité", "Ajoutez un caractère spécial (!@#$%^&*).")

        # 5. Tentative d'inscription
        if UserAccount(*data).register():
            messagebox.showinfo("Succès", "Compte créé avec succès !"); self.show_login()
        else:
            messagebox.showerror("Erreur", "Cet email est déjà utilisé par un autre utilisateur.")

    def save_creds(self, em):
        with open(CONFIG_FILE, "w") as f: json.dump({"email": em}, f)

    def load_creds(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f: return json.load(f).get("email")
            except: pass
        return None

if __name__ == "__main__":
    BudgetBuddyApp().mainloop()