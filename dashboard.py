import tkinter as tk
from tkinter import messagebox
from user_account import UserAccount
import uuid
from datetime import datetime

class DashboardWindow(tk.Toplevel):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.title("Budget Buddy - Tableau de Bord")
        self.geometry("500x550")
        self.user_email = user_email
        
        # --- Zone d'affichage du Solde ---
        tk.Label(self, text=f"Compte : {user_email}", font=("Arial", 10, "italic")).pack(pady=10)
        
        self.balance_label = tk.Label(self, text="Solde : -- €", font=("Arial", 22, "bold"), fg="navy")
        self.balance_label.pack(pady=20)
        
        # --- Formulaire ---
        tk.Label(self, text="--- Ajouter une opération ---", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self, text="Description").pack()
        self.desc_var = tk.StringVar()
        tk.Entry(self, textvariable=self.desc_var).pack()
        
        tk.Label(self, text="Montant (€)").pack()
        self.amount_var = tk.DoubleVar()
        tk.Entry(self, textvariable=self.amount_var).pack()
        
        tk.Label(self, text="Type").pack()
        self.type_var = tk.StringVar(value="retrait")
        tk.OptionMenu(self, self.type_var, "retrait", "dépôts", "transfert").pack()
        
        tk.Button(self, text="Enregistrer", command=self.save_transaction, bg="#2196F3", fg="white", width=20).pack(pady=20)
        
        # Chargement initial du solde
        self.update_balance()

    def update_balance(self):
        """Récupère le solde calculé depuis MySQL."""
        user = UserAccount(email=self.user_email)
        current_balance = user.get_balance()
        self.balance_label.config(text=f"Solde : {current_balance:.2f} €")

    def save_transaction(self):
        """Génère la transaction et met à jour la base."""
        try:
            ref = str(uuid.uuid4())[:8].upper()
            desc = self.desc_var.get()
            amount = self.amount_var.get()
            t_type = self.type_var.get()
            date_now = datetime.now().strftime("%Y-%m-%d")

            if amount <= 0:
                messagebox.showwarning("Attention", "Le montant doit être supérieur à 0")
                return

            user = UserAccount(email=self.user_email)
            if user.process_transaction(ref, desc, amount, date_now, t_type):
                messagebox.showinfo("Succès", "Transaction enregistrée !")
                self.update_balance()
                # On vide le champ description
                self.desc_var.set("")
                self.amount_var.set(0.0)
            else:
                messagebox.showerror("Erreur", "Impossible d'enregistrer la transaction")
        except Exception as e:
            messagebox.showerror("Erreur", f"Données invalides : {e}")