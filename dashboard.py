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
        self.geometry("1100x850")
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

    def btn(self, master, text, cmd, bg, hover="#324CBB", side=None, fill=None):
        """Utilitaire pour créer des boutons stylisés rapidement."""
        b = tk.Button(master, text=text, command=cmd, bg=bg, fg="white", font=("Segoe UI", 9, "bold"), 
                      relief="flat", cursor="hand2", padx=15)
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        if side: b.pack(side=side, padx=5, pady=5, fill=fill)
        return b

    def build_ui(self):
        # Header
        h = tk.Frame(self, bg="#32325D", height=60)
        h.pack(fill="x")
        tk.Label(h, text="TABLEAU DE BORD", fg="white", bg="#32325D", font=("Segoe UI", 12, "bold")).pack(side="left", padx=20)
        self.btn(h, "DÉCONNEXION", self.logout, "#F5365C", "#D32F2F", side="right")

        cnt = tk.Frame(self, bg="#F8F9FE")
        cnt.pack(fill="both", expand=True, padx=20, pady=20)
        left = tk.Frame(cnt, bg="#F8F9FE")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Solde Card
        card = tk.Frame(left, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        card.pack(fill="x", pady=(0, 15))
        tk.Label(card, text="SOLDE ACTUEL", bg="white", fg="#8898AA", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.bal_lbl = tk.Label(card, text="-- €", bg="white", font=("Segoe UI", 28, "bold"))
        self.bal_lbl.pack(anchor="w")

        # Filtres
        fb = tk.LabelFrame(left, text="🔍 FILTRES", bg="white", font=("Segoe UI", 8, "bold"), fg="#8898AA", padx=10, pady=5)
        fb.pack(fill="x", pady=(0, 15))
        self.f_type, self.f_cat, self.f_sort = tk.StringVar(value="Tous Types"), tk.StringVar(value="Toutes Catégories"), tk.StringVar(value="Date (Récents)")
        
        r1 = tk.Frame(fb, bg="white")
        r1.pack(fill="x")
        for v, opt in [(self.f_type, ["Tous Types", "retrait", "dépôts", "transfert"]), (self.f_cat, ["Toutes Catégories", "Loisir", "Repas", "Facture", "Salaire", "Autre"]), (self.f_sort, ["Date (Récents)", "Montant (Croissant)", "Montant (Décroissant)"])]:
            tk.OptionMenu(r1, v, *opt).pack(side="left", padx=2)

        r2 = tk.Frame(fb, bg="white")
        r2.pack(fill="x", pady=5)
        self.f_start, self.f_end = tk.Entry(r2, width=12), tk.Entry(r2, width=12)
        for t, e in [("Du:", self.f_start), ("Au:", self.f_end)]:
            tk.Label(r2, text=t, bg="white").pack(side="left", padx=2)
            e.pack(side="left", padx=2)
        self.btn(r2, "FILTRER", self.refresh_all, "#5E72E4", side="left")
        self.btn(r2, "RESET", self.reset_filters, "#EDF2F7", "#CBD5E0", side="left").config(fg="#4A5568")

        # Formulaire
        form = tk.LabelFrame(left, text="➕ OPÉRATION", bg="white", font=("Segoe UI", 8, "bold"), fg="#8898AA", padx=20, pady=10)
        form.pack(fill="x")
        self.vars = {k: tk.StringVar(value=v) for k, v in [("desc",""), ("amt",""), ("type","retrait"), ("cat","Loisir")]}
        
        rf1 = tk.Frame(form, bg="white")
        rf1.pack(fill="x")
        self.create_entry(rf1, "DESCRIPTION", self.vars["desc"], 20).pack(side="left", padx=(0,10))
        self.create_entry(rf1, "MONTANT", self.vars["amt"], 10).pack(side="left")

        rf2 = tk.Frame(form, bg="white")
        rf2.pack(fill="x", pady=5)
        for k in ["type", "cat"]:
            opts = ["retrait", "dépôts", "transfert"] if k == "type" else ["Loisir", "Repas", "Facture", "Salaire", "Autre"]
            tk.OptionMenu(rf2, self.vars[k], *opts).pack(side="left", padx=5)
        
        self.btn(form, "ENREGISTRER", self.save, "#2DCE89", "#24A46D", side="top", fill="x")

        # Tableau
        self.tree = ttk.Treeview(left, columns=("D", "De", "M", "T"), show="headings", height=8)
        for c, h in zip(("D", "De", "M", "T"), ("DATE", "DESC", "MONTANT", "TYPE")):
            self.tree.heading(c, text=h); self.tree.column(c, width=90, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        for t, col in [("dépôts", "#2DCE89"), ("retrait", "#F5365C"), ("transfert", "#5E72E4")]:
            self.tree.tag_configure(t, foreground=col)

        self.btn(left, "📥 EXPORTER CSV", self.export, "#11CDEF", "#05B6D4", side="top", fill="x")

        # Graphique
        self.chart_view = BudgetChart(cnt, highlightthickness=1, highlightbackground="#E9ECEF")
        self.chart_view.pack(side="right", fill="both", expand=True, padx=(10, 0))

    def create_entry(self, master, label, var, width):
        f = tk.Frame(master, bg="white")
        tk.Label(f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Entry(f, textvariable=var, width=width, highlightthickness=1, highlightbackground="#CAD1D7", relief="flat").pack(ipady=3)
        return f

    def refresh_all(self):
        bal = self.user.get_balance()
        self.bal_lbl.config(text=f"{bal:.2f} €", fg="#F5365C" if bal < 0 else "#2DCE89")
        
        data = self.user.get_filtered_transactions()
        filtered = [t for t in data if (self.f_type.get() == "Tous Types" or t[3] == self.f_type.get()) and
                    (self.f_cat.get() == "Toutes Catégories" or t[4] == self.f_cat.get()) and
                    (not self.f_start.get() or t[0] >= self.f_start.get()) and (not self.f_end.get() or t[0] <= self.f_end.get())]

        s = self.f_sort.get()
        filtered.sort(key=lambda x: x[2] if "Montant" in s else x[0], reverse=("Décroissant" in s or "Récents" in s))

        self.tree.delete(*self.tree.get_children())
        for t in filtered:
            sig = "+" if t[3] == "dépôts" else "-"
            self.tree.insert("", "end", values=(t[0], t[1], f"{sig}{t[2]:.2f} €", t[3].upper()), tags=(t[3],))
        self.chart_view.update_chart(self.user.get_stats_by_category())

    def save(self):
        try:
            d, a = self.vars["desc"].get().strip(), self.vars["amt"].get().strip()
            if not d or not a: return messagebox.showwarning("Incomplet", "Champs requis")
            if self.user.process_transaction(str(uuid.uuid4())[:8], d, float(a), datetime.now().strftime("%Y-%m-%d"), self.vars["type"].get(), self.vars["cat"].get()):
                self.vars["desc"].set(""); self.vars["amt"].set(""); self.refresh_all()
        except: messagebox.showerror("Erreur", "Montant invalide")

    def reset_filters(self):
        self.f_type.set("Tous Types"); self.f_cat.set("Toutes Catégories"); self.f_sort.set("Date (Récents)")
        self.f_start.delete(0, 'end'); self.f_end.delete(0, 'end'); self.refresh_all()

    def export(self):
        if p := filedialog.asksaveasfilename(defaultextension=".csv"):
            with open(p, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["DATE", "DESCRIPTION", "MONTANT", "TYPE"])
                for i in self.tree.get_children(): writer.writerow(self.tree.item(i)['values'])

    def logout(self):
        if messagebox.askyesno("Quitter", "Se déconnecter ?"): self.master.deiconify(); self.destroy()