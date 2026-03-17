import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import uuid, csv
from datetime import datetime
from user_account import UserAccount
from budgetchart import BudgetChart

class DashboardWindow(tk.Toplevel):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.title("Budget Buddy Assistant")
        self.geometry("1100x820")
        self.user = UserAccount(email=user_email)
        self.configure(bg="#F8F9FE")
        self.setup_styles()
        self.build_ui()
        self.refresh_all()

    def setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview", background="white", rowheight=35, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background="#F6F9FC", font=("Segoe UI", 9, "bold"))

    def btn(self, master, text, cmd, bg, fg="white", font=("Segoe UI", 9, "bold"), hover="#324CBB"):
        b = tk.Button(master, text=text, command=cmd, bg=bg, fg=fg, font=font, relief="flat", cursor="hand2", padx=15)
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        return b

    def build_ui(self):
        # Header
        h = tk.Frame(self, bg="#32325D", height=60)
        h.pack(fill="x")
        tk.Label(h, text="TABLEAU DE BORD", fg="white", bg="#32325D", font=("Segoe UI", 12, "bold")).pack(side="left", padx=20)
        self.btn(h, "DÉCONNEXION", self.logout, "#F5365C", hover="#D32F2F").pack(side="right", padx=20, pady=10)

        cnt = tk.Frame(self, bg="#F8F9FE")
        cnt.pack(fill="both", expand=True, padx=20, pady=20)
        left = tk.Frame(cnt, bg="#F8F9FE")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Solde Card
        card = tk.Frame(left, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        card.pack(fill="x", pady=(0, 15))
        self.bal_lbl = tk.Label(card, text="-- €", bg="white", font=("Segoe UI", 24, "bold"))
        self.bal_lbl.pack(anchor="w")

        # Filtres
        fb = tk.LabelFrame(left, text="🔍 FILTRES", bg="white", font=("Segoe UI", 8, "bold"), fg="#8898AA", padx=10, pady=5)
        fb.pack(fill="x", pady=(0, 15))
        self.f_type, self.f_cat, self.f_sort = tk.StringVar(value="Tous Types"), tk.StringVar(value="Toutes Catégories"), tk.StringVar(value="Date (Récents)")
        
        r1 = tk.Frame(fb, bg="white")
        r1.pack(fill="x")
        for var, opt in [(self.f_type, ["Tous Types", "retrait", "dépôts", "transfert"]), (self.f_cat, ["Toutes Catégories", "Loisir", "Repas", "Facture", "Salaire", "Autre"]), (self.f_sort, ["Date (Récents)", "Montant (Croissant)", "Montant (Décroissant)"])]:
            tk.OptionMenu(r1, var, *opt).pack(side="left", padx=2)

        r2 = tk.Frame(fb, bg="white")
        r2.pack(fill="x", pady=5)
        self.f_start, self.f_end = tk.Entry(r2, width=10), tk.Entry(r2, width=10)
        for lbl, ent in [("Du:", self.f_start), ("Au:", self.f_end)]:
            tk.Label(r2, text=lbl, bg="white", font=("Segoe UI", 8)).pack(side="left", padx=2)
            ent.pack(side="left", padx=2)
        
        self.btn(r2, "FILTRER", self.refresh_all, "#5E72E4").pack(side="left", padx=5)
        self.btn(r2, "RESET", self.reset_filters, "#EDF2F7", fg="#4A5568", hover="#CBD5E0").pack(side="left")

        # Formulaire
        form = tk.Frame(left, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        form.pack(fill="x")
        self.vars = {k: tk.StringVar() for k in ["desc", "amt", "type", "cat"]}
        self.vars["type"].set("retrait"); self.vars["cat"].set("Loisir")
        
        rf = tk.Frame(form, bg="white")
        rf.pack(fill="x")
        self.create_entry(rf, "Description", self.vars["desc"], 15).pack(side="left", padx=(0, 10))
        self.create_entry(rf, "Montant", self.vars["amt"], 8).pack(side="left")
        
        self.btn(form, "ENREGISTRER", self.save, "#2DCE89", hover="#24A46D").pack(fill="x", pady=(10, 0))

        # Tableau
        self.tree = ttk.Treeview(left, columns=("D", "De", "M", "T"), show="headings", height=6)
        for c, h in zip(("D", "De", "M", "T"), ("DATE", "DESC", "MONTANT", "TYPE")):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=80, anchor="center")
        self.tree.pack(fill="x", pady=15)
        for t, col in [("dépôts", "#2DCE89"), ("retrait", "#F5365C"), ("transfert", "#5E72E4")]:
            self.tree.tag_configure(t, foreground=col)

        self.btn(left, "📥 EXPORTER CSV", self.export, "#11CDEF", hover="#05B6D4").pack(fill="x")

        # Graphique
        self.chart_view = BudgetChart(cnt, highlightthickness=1, highlightbackground="#E9ECEF")
        self.chart_view.pack(side="right", fill="both", expand=True, padx=(10, 0))

    def create_entry(self, master, label, var, width):
        f = tk.Frame(master, bg="white")
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Entry(f, textvariable=var, width=width, relief="flat", highlightthickness=1, highlightbackground="#CAD1D7").pack(ipady=3)
        return f

    def reset_filters(self):
        self.f_type.set("Tous Types"); self.f_cat.set("Toutes Catégories"); self.f_sort.set("Date (Récents)")
        self.f_start.delete(0, 'end'); self.f_end.delete(0, 'end')
        self.refresh_all()

    def refresh_all(self):
        bal = self.user.get_balance()
        self.bal_lbl.config(text=f"{bal:.2f} €", fg="#F5365C" if bal < 0 else "#2DCE89")
        
        filtered = [t for t in self.user.get_filtered_transactions() if 
                    (self.f_type.get() == "Tous Types" or t[3] == self.f_type.get()) and
                    (self.f_cat.get() == "Toutes Catégories" or t[4] == self.f_cat.get()) and
                    (not self.f_start.get() or t[0] >= self.f_start.get()) and
                    (not self.f_end.get() or t[0] <= self.f_end.get())]

        s = self.f_sort.get()
        filtered.sort(key=lambda x: x[2] if "Montant" in s else x[0], reverse=("Décroissant" in s or "Récents" in s))

        self.tree.delete(*self.tree.get_children())
        for t in filtered[:20]:
            sig = "+" if t[3] == "dépôts" else "-"
            self.tree.insert("", "end", values=(t[0], t[1], f"{sig}{t[2]:.2f} €", t[3].upper()), tags=(t[3],))
        self.chart_view.update_chart(self.user.get_stats_by_category())

    def save(self):
        try:
            if self.user.process_transaction(str(uuid.uuid4())[:8], self.vars["desc"].get(), float(self.vars["amt"].get()), datetime.now().strftime("%Y-%m-%d"), self.vars["type"].get(), self.vars["cat"].get()):
                self.vars["desc"].set(""); self.vars["amt"].set(""); self.refresh_all()
        except: messagebox.showerror("Erreur", "Saisie invalide")

    def export(self):
        if path := filedialog.asksaveasfilename(defaultextension=".csv"):
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["DATE", "DESC", "MONTANT", "TYPE"])
                for i in self.tree.get_children(): writer.writerow(self.tree.item(i)['values'])
            messagebox.showinfo("Export", "Succès !")

    def logout(self):
        self.master.deiconify()
        self.destroy()