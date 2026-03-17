import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import uuid, csv, matplotlib.pyplot as plt
from datetime import datetime
from user_account import UserAccount
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from budgetchart import BudgetChart

class DashboardWindow(tk.Toplevel):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.title("Budget Buddy Assistant")
        self.geometry("1100x850") # Légèrement agrandi pour les filtres
        self.user = UserAccount(email=user_email)
        self.user_email = user_email
        self.configure(bg="#F8F9FE")

        self.setup_styles()
        self.build_ui()
        self.refresh_all()

    def setup_styles(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Treeview", background="white", rowheight=35, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background="#F6F9FC", font=("Segoe UI", 9, "bold"))
        s.map("Treeview", background=[("selected", "#5E72E4")])

    def add_hover_effect(self, widget, hover_color, normal_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))

    def build_ui(self):
        # --- HEADER ---
        h = tk.Frame(self, bg="#32325D", height=70)
        h.pack(fill="x")
        tk.Label(h, text="TABLEAU DE BORD", fg="white", bg="#32325D", font=("Segoe UI", 14, "bold")).pack(side="left", padx=30)
        
        btn_out = tk.Button(h, text="DÉCONNEXION", command=self.logout, bg="#F5365C", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", padx=15, cursor="hand2")
        btn_out.pack(side="right", padx=30)
        self.add_hover_effect(btn_out, "#D32F2F", "#F5365C")

        main_container = tk.Frame(self, bg="#F8F9FE")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # --- COLONNE GAUCHE ---
        left = tk.Frame(main_container, bg="#F8F9FE")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Card Solde
        card = tk.Frame(left, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        card.pack(fill="x", pady=(0, 20))
        self.bal_lbl = tk.Label(card, text="-- €", bg="white", font=("Segoe UI", 28, "bold"))
        self.bal_lbl.pack(anchor="w")

        # --- SECTION FILTRES ---
        f_box = tk.LabelFrame(left, text="🔍 FILTRES & RECHERCHE", bg="white", font=("Segoe UI", 8, "bold"), fg="#8898AA", padx=10, pady=10)
        f_box.pack(fill="x", pady=(0, 15))

        self.f_type = tk.StringVar(value="Tous Types")
        self.f_cat = tk.StringVar(value="Toutes Catégories")
        self.f_sort = tk.StringVar(value="Date (Récents)")

        row_f1 = tk.Frame(f_box, bg="white")
        row_f1.pack(fill="x")
        tk.OptionMenu(row_f1, self.f_type, "Tous Types", "retrait", "dépôts", "transfert").pack(side="left", padx=2)
        tk.OptionMenu(row_f1, self.f_cat, "Toutes Catégories", "Loisir", "Repas", "Facture", "Salaire", "Autre").pack(side="left", padx=2)
        tk.OptionMenu(row_f1, self.f_sort, "Date (Récents)", "Montant (Croissant)", "Montant (Décroissant)").pack(side="left", padx=2)

        row_f2 = tk.Frame(f_box, bg="white")
        row_f2.pack(fill="x", pady=(5, 0))
        tk.Label(row_f2, text="Du:", bg="white", font=("Segoe UI", 8)).pack(side="left")
        self.f_start = tk.Entry(row_f2, width=11); self.f_start.pack(side="left", padx=2)
        tk.Label(row_f2, text="Au:", bg="white", font=("Segoe UI", 8)).pack(side="left")
        self.f_end = tk.Entry(row_f2, width=11); self.f_end.pack(side="left", padx=2)
        
        btn_apply = tk.Button(row_f2, text="FILTRER", command=self.refresh_all, bg="#5E72E4", fg="white", font=("Segoe UI", 8, "bold"), padx=10)
        btn_apply.pack(side="left", padx=10)
        self.add_hover_effect(btn_apply, "#324CBB", "#5E72E4")

        # Formulaire d'ajout
        form = tk.Frame(left, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        form.pack(fill="x")
        self.vars = {k: tk.StringVar() for k in ["desc", "amt", "type", "cat"]}
        self.vars["type"].set("retrait"); self.vars["cat"].set("Loisir")

        r1 = tk.Frame(form, bg="white")
        r1.pack(fill="x")
        self.create_entry(r1, "Description", self.vars["desc"], 15).pack(side="left", padx=(0, 10))
        self.create_entry(r1, "Montant (€)", self.vars["amt"], 8).pack(side="left")

        r2 = tk.Frame(form, bg="white")
        r2.pack(fill="x", pady=10)
        tk.OptionMenu(r2, self.vars["type"], "retrait", "dépôts", "transfert").pack(side="left", padx=(0, 10))
        tk.OptionMenu(r2, self.vars["cat"], "Loisir", "Repas", "Facture", "Salaire", "Autre").pack(side="left")

        btn_save = tk.Button(form, text="ENREGISTRER L'OPÉRATION", command=self.save, bg="#5E72E4", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", height=2, cursor="hand2")
        btn_save.pack(fill="x", pady=(10, 0))
        self.add_hover_effect(btn_save, "#324CBB", "#5E72E4")

        # Tableau
        self.tree = ttk.Treeview(left, columns=("Date", "Desc", "Montant", "Type"), show="headings", height=6)
        for c in ("Date", "Desc", "Montant", "Type"):
            self.tree.heading(c, text=c.upper())
            self.tree.column(c, width=100, anchor="center")
        self.tree.pack(fill="x", pady=(20, 10))
        
        self.tree.tag_configure("dépôts", foreground="#2DCE89")
        self.tree.tag_configure("retrait", foreground="#F5365C")
        self.tree.tag_configure("transfert", foreground="#5E72E4")

        # Bouton Export
        btn_export = tk.Button(left, text="📥 EXPORTER EN CSV", command=self.export, bg="#11CDEF", fg="white", font=("Segoe UI", 11, "bold"), relief="flat", height=2, cursor="hand2")
        btn_export.pack(fill="x")
        self.add_hover_effect(btn_export, "#05B6D4", "#11CDEF")

        # Colonne Droite
        self.chart_view = BudgetChart(main_container, highlightthickness=1, highlightbackground="#E9ECEF")
        self.chart_view.pack(side="right", fill="both", expand=True, padx=(10, 0))

    def create_entry(self, master, label, var, width):
        f = tk.Frame(master, bg="white")
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Entry(f, textvariable=var, width=width, relief="flat", highlightthickness=1, highlightbackground="#CAD1D7").pack(ipady=5)
        return f

    def refresh_all(self):
        # 1. Solde
        bal = self.user.get_balance()
        self.bal_lbl.config(text=f"{bal:.2f} €", fg="#F5365C" if bal < 0 else "#2DCE89")
        
        # 2. Récupération & Filtrage
        data = self.user.get_filtered_transactions()
        filtered = []
        
        for t in data:
            # t: (date, desc, montant, type, categorie)
            keep = True
            if self.f_type.get() != "Tous Types" and t[3] != self.f_type.get(): keep = False
            if self.f_cat.get() != "Toutes Catégories" and t[4] != self.f_cat.get(): keep = False
            
            # Dates
            start, end = self.f_start.get(), self.f_end.get()
            if start and t[0] < start: keep = False
            if end and t[0] > end: keep = False
            
            if keep: filtered.append(t)

        # 3. Tri
        s = self.f_sort.get()
        if s == "Montant (Croissant)": filtered.sort(key=lambda x: x[2])
        elif s == "Montant (Décroissant)": filtered.sort(key=lambda x: x[2], reverse=True)
        else: filtered.sort(key=lambda x: x[0], reverse=True)

        # 4. Affichage
        self.tree.delete(*self.tree.get_children())
        for t in filtered:
            signe = "+" if t[3] == "dépôts" else "-"
            self.tree.insert("", "end", values=(t[0], t[1], f"{signe}{t[2]:.2f} €", t[3].upper()), tags=(t[3],))

        # 5. Graphique
        stats = self.user.get_stats_by_category()
        self.chart_view.update_chart(stats)

    def save(self):
        try:
            d, a = self.vars["desc"].get(), float(self.vars["amt"].get())
            if d and a > 0:
                if self.user.process_transaction(str(uuid.uuid4())[:8], d, a, datetime.now().strftime("%Y-%m-%d"), self.vars["type"].get(), self.vars["cat"].get()):
                    self.vars["desc"].set(""); self.vars["amt"].set("")
                    self.refresh_all()
        except: messagebox.showerror("Erreur", "Saisie invalide")

    def export(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if path:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["DATE", "DESCRIPTION", "MONTANT", "TYPE", "CATEGORIE"])
                # On exporte la liste filtrée actuellement affichée (via refresh_all logic)
                for item in self.tree.get_children():
                    writer.writerow(self.tree.item(item)['values'])
            messagebox.showinfo("Export", "Réussi !")

    def logout(self):
        self.master.deiconify()
        self.destroy()