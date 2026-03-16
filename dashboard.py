import tkinter as tk
from tkinter import messagebox, ttk
import uuid
from datetime import datetime
from user_account import UserAccount

# Imports pour l'intégration graphique
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardWindow(tk.Toplevel):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.title("Budget Buddy Pro")
        self.geometry("1100x700")
        self.configure(bg="#F8F9FE")
        self.user_email = user_email

        self.setup_styles()

        # --- Header ---
        self.header = tk.Frame(self, bg="#32325D", height=70)
        self.header.pack(fill="x")
        tk.Label(self.header, text="TABLEAU DE BORD", fg="white", bg="#32325D", 
                 font=("Segoe UI", 14, "bold")).pack(side="left", padx=30)
        
        tk.Button(self.header, text="DÉCONNEXION", command=self.logout, bg="#F5365C", 
                  fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=15).pack(side="right", padx=30)

        self.main_container = tk.Frame(self, bg="#F8F9FE")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Colonnes
        self.left_col = tk.Frame(self.main_container, bg="#F8F9FE", width=500)
        self.left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.right_col = tk.Frame(self.main_container, bg="white", highlightthickness=1, highlightbackground="#E9ECEF")
        self.right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.build_left_panel()
        self.build_right_panel()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", rowheight=35, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#F6F9FC", font=("Segoe UI", 9, "bold"), borderwidth=0)
        style.map("Treeview", background=[('selected', '#5E72E4')])

    def build_left_panel(self):
        # Card Solde
        solde_card = tk.Frame(self.left_col, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        solde_card.pack(fill="x", pady=(0, 20))
        tk.Label(solde_card, text=f"COMPTE : {self.user_email}", bg="white", fg="#8898AA", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        self.balance_label = tk.Label(solde_card, text="-- €", bg="white", font=("Segoe UI", 28, "bold"))
        self.balance_label.pack(anchor="w")

        # Formulaire
        form = tk.Frame(self.left_col, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        form.pack(fill="x")

        row = tk.Frame(form, bg="white")
        row.pack(fill="x")
        self.desc_var = tk.StringVar()
        self.amount_var = tk.DoubleVar()
        self.create_entry(row, "Description", self.desc_var, 15).pack(side="left", padx=(0, 10))
        self.create_entry(row, "Montant (€)", self.amount_var, 8).pack(side="left")

        row2 = tk.Frame(form, bg="white")
        row2.pack(fill="x", pady=10)
        
        self.type_var = tk.StringVar(value="retrait")
        self.cat_var = tk.StringVar(value="Loisir")
        
        # AJOUT DU TYPE TRANSFERT ICI
        tk.OptionMenu(row2, self.type_var, "retrait", "dépôts", "transfert").pack(side="left", padx=(0, 10))
        tk.OptionMenu(row2, self.cat_var, "Loisir", "Repas", "Facture", "Salaire", "Autre").pack(side="left")

        tk.Button(form, text="ENREGISTRER L'OPÉRATION", command=self.save_transaction, 
                  bg="#5E72E4", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", height=2).pack(fill="x", pady=(10, 0))

        # Tableau (Historique)
        self.tree = ttk.Treeview(self.left_col, columns=("Date", "Desc", "Montant"), show="headings", height=10)
        self.tree.heading("Date", text="DATE")
        self.tree.heading("Desc", text="DESCRIPTION")
        self.tree.heading("Montant", text="MONTANT")
        self.tree.column("Date", width=100)
        self.tree.column("Montant", anchor="e")
        self.tree.pack(fill="both", expand=True, pady=(20, 0))
        
        # STYLES DE COULEURS POUR CHAQUE TYPE
        self.tree.tag_configure("depot", foreground="#2DCE89")    # Vert
        self.tree.tag_configure("retrait", foreground="#F5365C")  # Rouge
        self.tree.tag_configure("transfert", foreground="#5E72E4") # Bleu Indigo

    def build_right_panel(self):
        tk.Label(self.right_col, text="RÉPARTITION DES DÉPENSES", bg="white", font=("Segoe UI", 11, "bold"), fg="#32325D").pack(pady=20)
        self.chart_frame = tk.Frame(self.right_col, bg="white")
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.update_balance()
        self.load_history()
        self.refresh_chart()

    def create_entry(self, master, label, var, width):
        container = tk.Frame(master, bg="white")
        tk.Label(container, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Entry(container, textvariable=var, width=width, relief="flat", highlightthickness=1, highlightbackground="#CAD1D7").pack(ipady=5)
        return container

    def refresh_chart(self):
        for widget in self.chart_frame.winfo_children(): widget.destroy()
        user = UserAccount(email=self.user_email)
        stats = user.get_stats_by_category()

        if not stats:
            tk.Label(self.chart_frame, text="Aucune donnée à afficher", bg="white", fg="#8898AA").pack(expand=True)
            return

        labels = [s[0] for s in stats]
        sizes = [float(s[1]) for s in stats]
        colors = ['#5E72E4', '#2DCE89', '#11CDEF', '#FB6340', '#F5365C']

        fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
        fig.patch.set_facecolor('white')
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def update_balance(self):
        user = UserAccount(email=self.user_email)
        bal = user.get_balance()
        color = "#F5365C" if bal < 0 else "#2DCE89"
        self.balance_label.config(text=f"{bal:.2f} €", fg=color)
        if bal < 0:
            messagebox.showwarning("Alerte Découvert", f"Attention : Solde négatif ({bal:.2f} €)")

    def load_history(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        user = UserAccount(email=self.user_email)
        transactions = user.get_filtered_transactions()
        
        for t in transactions[:15]:
            t_type = t[3]
            # LOGIQUE DE SIGNES ET TAGS POUR LE TYPE TRANSFERT
            if t_type == "dépôts":
                tag, signe = "depot", "+"
            elif t_type == "transfert":
                tag, signe = "transfert", "-"
            else:
                tag, signe = "retrait", "-"
                
            val = f"{signe}{t[2]:.2f} €"
            self.tree.insert("", "end", values=(t[0], t[1], val), tags=(tag,))

    def save_transaction(self):
        try:
            desc, amount = self.desc_var.get(), self.amount_var.get()
            t_type = self.type_var.get()
            cat = self.cat_var.get()
            
            if not desc or amount <= 0: return
            
            user = UserAccount(email=self.user_email)
            ref = str(uuid.uuid4())[:8].upper()
            date_now = datetime.now().strftime("%Y-%m-%d")
            
            if user.process_transaction(ref, desc, amount, date_now, t_type, cat):
                self.desc_var.set(""); self.amount_var.set(0.0)
                self.update_balance()
                self.load_history()
                self.refresh_chart()
        except:
            messagebox.showerror("Erreur", "Données invalides.")

    def logout(self):
        self.master.deiconify()
        self.destroy()