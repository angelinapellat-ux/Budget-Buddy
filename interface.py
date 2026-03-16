import tkinter as tk
from tkinter import messagebox
from user_account import UserAccount

class RegisterWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Budget Buddy - Inscription")
        self.geometry("400x650")
        self.configure(bg="#F8F9FE")
        self.resizable(False, False)

        # Conteneur principal (Card)
        self.card = tk.Frame(self, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#E9ECEF")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=340, height=600)

        tk.Label(self.card, text="Créer un compte", font=("Segoe UI", 18, "bold"), bg="white", fg="#32325D").pack(pady=(0, 20))

        # Champs de saisie modernisés
        self.nom_var = self.create_modern_input("NOM")
        self.prenom_var = self.create_modern_input("PRÉNOM")
        self.email_var = self.create_modern_input("EMAIL")
        self.pwd_var = self.create_modern_input("MOT DE PASSE", is_pwd=True)
        self.pwd_confirm_var = self.create_modern_input("CONFIRMER LE MOT DE PASSE", is_pwd=True)

        # Bouton Inscription (Vert Émeraude)
        self.btn_reg = tk.Button(self.card, text="S'INSCRIRE MAINTENANT", command=self.register, 
                                 bg="#2DCE89", fg="white", font=("Segoe UI", 10, "bold"), 
                                 relief="flat", height=2, cursor="hand2")
        self.btn_reg.pack(fill="x", pady=25)
        
        # Effet de survol
        self.btn_reg.bind("<Enter>", lambda e: self.btn_reg.config(bg="#24B377"))
        self.btn_reg.bind("<Leave>", lambda e: self.btn_reg.config(bg="#2DCE89"))

        tk.Button(self.card, text="Annuler", command=self.destroy, bg="white", 
                  fg="#8898AA", relief="flat", font=("Segoe UI", 9)).pack()

    def create_modern_input(self, label, is_pwd=False):
        f = tk.Frame(self.card, bg="white")
        f.pack(fill="x", pady=5)
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 7, "bold")).pack(anchor="w")
        
        var = tk.StringVar()
        entry = tk.Entry(f, textvariable=var, show="●" if is_pwd else "", bg="white", 
                         relief="flat", highlightthickness=1, highlightbackground="#CAD1D7", font=("Segoe UI", 10))
        entry.pack(fill="x", ipady=7)
        
        # Effet Focus
        entry.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground="#5E72E4"))
        entry.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground="#CAD1D7"))
        
        return var

    def register(self):
        # 1. Validation de remplissage
        if not all([self.nom_var.get(), self.prenom_var.get(), self.email_var.get()]):
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
            return

        # 2. Validation correspondance MDP
        if self.pwd_var.get() != self.pwd_confirm_var.get():
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return

        # 3. Validation force du MDP
        if not UserAccount.validate_password_strength(self.pwd_var.get()):
            messagebox.showerror("Sécurité", "Mot de passe trop faible !\n\nCritères :\n- 10 caractères min.\n- Majuscule & Minuscule\n- Chiffre\n- Caractère spécial")
            return

        # 4. Enregistrement
        new_user = UserAccount(self.nom_var.get(), self.prenom_var.get(), self.email_var.get(), self.pwd_var.get())
        if new_user.register():
            messagebox.showinfo("Succès", f"Félicitations {self.prenom_var.get()}, votre compte est prêt !")
            self.destroy()
        else:
            messagebox.showerror("Erreur", "L'inscription a échoué. L'email est peut-être déjà utilisé.")