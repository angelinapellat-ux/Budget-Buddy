import tkinter as tk
import re
from tkinter import messagebox
from user_account import UserAccount

class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Budget Buddy - Inscription")
        self.geometry("400x650")
        try: self.iconbitmap("asset/logo.ico")
        except: pass
        self.configure(bg="#F8F9FE")
        self.resizable(False, False)

        # Carte centrale
        self.card = tk.Frame(self, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#E9ECEF")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=600)

        tk.Label(self.card, text="Créer un compte", font=("Segoe UI", 18, "bold"), bg="white", fg="#32325D").pack(pady=(0, 20))

        # Génération des champs
        self.nom = self.create_input("NOM")
        self.prenom = self.create_input("PRÉNOM")
        self.email = self.create_input("EMAIL")
        self.pwd = self.create_input("MOT DE PASSE", True)
        self.pwd_conf = self.create_input("CONFIRMER LE MOT DE PASSE", True)

        # Bouton Inscription
        self.btn_reg = tk.Button(self.card, text="S'INSCRIRE MAINTENANT", command=self.handle_register, 
                                 bg="#2DCE89", fg="white", font=("Segoe UI", 10, "bold"), 
                                 relief="flat", height=2, cursor="hand2")
        self.btn_reg.pack(fill="x", pady=25)
        self.btn_reg.bind("<Enter>", lambda _: self.btn_reg.config(bg="#24B377"))
        self.btn_reg.bind("<Leave>", lambda _: self.btn_reg.config(bg="#2DCE89"))

        tk.Button(self.card, text="Annuler", command=self.destroy, bg="white", 
                  fg="#8898AA", relief="flat", font=("Segoe UI", 9)).pack()

    def create_input(self, label, is_pwd=False):
        f = tk.Frame(self.card, bg="white")
        f.pack(fill="x", pady=5)
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 7, "bold")).pack(anchor="w")
        
        v = tk.StringVar()
        e = tk.Entry(f, textvariable=v, show="●" if is_pwd else "", bg="white", 
                     relief="flat", highlightthickness=1, highlightbackground="#CAD1D7", font=("Segoe UI", 10))
        e.pack(fill="x", ipady=7)
        e.bind("<FocusIn>", lambda _: e.config(highlightbackground="#5E72E4"))
        e.bind("<FocusOut>", lambda _: e.config(highlightbackground="#CAD1D7"))
        return v

    def handle_register(self):
        n, pr, em, p, pc = self.nom.get().strip(), self.prenom.get().strip(), self.email.get().strip(), self.pwd.get().strip(), self.pwd_conf.get().strip()

        if not all([n, pr, em, p]):
            return messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
        
        # 1. Sécurité Email
        if not UserAccount.validate_email(em):
            return messagebox.showerror("Erreur Email", "Format d'email invalide (ex: jean@test.com).")

        # 2. Vérification correspondance
        if p != pc:
            return messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")

        # 3. Détail des erreurs de Mot de Passe
        if len(p) < 10:
            return messagebox.showwarning("Sécurité", "Le mot de passe doit contenir au moins 10 caractères.")
        if not re.search(r"[A-Z]", p):
            return messagebox.showwarning("Sécurité", "Il manque une lettre MAJUSCULE.")
        if not re.search(r"[a-z]", p):
            return messagebox.showwarning("Sécurité", "Il manque une lettre minuscule.")
        if not re.search(r"[0-9]", p):
            return messagebox.showwarning("Sécurité", "Il manque au moins un chiffre.")
        if not re.search(r"[!@#$%^&*]", p):
            return messagebox.showwarning("Sécurité", "Il manque un caractère spécial (!@#$%^&*).")

        if UserAccount(n, pr, em, p).register():
            messagebox.showinfo("Succès", f"Compte créé pour {pr} !")
            self.destroy()
        else:
            messagebox.showerror("Erreur", "Cet email est déjà enregistré.")