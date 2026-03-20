import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import uuid, csv, datetime
from user_account import UserAccount
from budgetchart import BudgetChart

class DashboardWindow(tk.Toplevel):
    def __init__(self, master, user_email):
        super().__init__(master)
        self.title("Budget Buddy Assistant"); self.geometry("1100x850")
        self.user = UserAccount(email=user_email)
        self.configure(bg="#F8F9FE"); self.editing_ref = None
        self.setup_styles(); self.build_ui(); self.refresh_all()

    def setup_styles(self):
        s = ttk.Style(self); s.theme_use("clam")
        s.configure("Treeview", background="white", rowheight=35, font=("Segoe UI", 10))
        s.configure("Treeview.Heading", background="#F6F9FC", font=("Segoe UI", 9, "bold"))

    def btn(self, master, text, cmd, bg, hover="#324CBB", side=None, fill=None):
        b = tk.Button(master, text=text, command=cmd, bg=bg, fg="white", font=("Segoe UI", 9, "bold"), 
                      relief="flat", cursor="hand2", padx=15)
        b.bind("<Enter>", lambda e: b.config(bg=hover)); b.bind("<Leave>", lambda e: b.config(bg=bg))
        if side: b.pack(side=side, padx=5, pady=5, fill=fill)
        return b

    def build_ui(self):
        # Header & Container
        h = tk.Frame(self, bg="#32325D", height=60); h.pack(fill="x")
        tk.Label(h, text="TABLEAU DE BORD", fg="white", bg="#32325D", font=("Segoe UI", 12, "bold")).pack(side="left", padx=20)
        self.btn(h, "DÉCONNEXION", self.logout, "#F5365C", "#D32F2F", "right")
        cnt = tk.Frame(self, bg="#F8F9FE"); cnt.pack(fill="both", expand=1, padx=20, pady=20)
        left = tk.Frame(cnt, bg="#F8F9FE"); left.pack(side="left", fill="both", expand=1, padx=(0, 10))
        # Sections UI
        self._ui_solde(left); self._ui_filters(left); self._ui_form(left); self._ui_table(left)
        self.chart_view = BudgetChart(cnt, highlightthickness=1, highlightbackground="#E9ECEF")
        self.chart_view.pack(side="right", fill="both", expand=1, padx=(10, 0))

    def _ui_solde(self, p):
        f = tk.Frame(p, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#E9ECEF")
        f.pack(fill="x", pady=(0, 15))
        tk.Label(f, text="SOLDE ACTUEL", bg="white", fg="#8898AA", font=("Segoe UI", 9, "bold")).pack(anchor="w")
        self.bal_lbl = tk.Label(f, text="-- €", bg="white", font=("Segoe UI", 28, "bold")); self.bal_lbl.pack(anchor="w")

    def _ui_filters(self, p):
        fb = tk.LabelFrame(p, text="🔍 FILTRES & TRI", bg="white", font=("Segoe UI", 8, "bold"), fg="#8898AA", padx=10, pady=5)
        fb.pack(fill="x", pady=(0, 15))
        # Variables des filtres
        self.f_type = tk.StringVar(value="Tous Types")
        self.f_cat = tk.StringVar(value="Toutes Catégories")
        self.f_sort = tk.StringVar(value="Montant") # Valeur par défaut
        r1 = tk.Frame(fb, bg="white"); r1.pack(fill="x")
        # Menus déroulants
        tk.OptionMenu(r1, self.f_type, "Tous Types", "retrait", "dépôts", "transfert").pack(side="left", padx=2)
        tk.OptionMenu(r1, self.f_cat, "Toutes Catégories", "Loisir", "Repas", "Facture", "Salaire", "Autre").pack(side="left", padx=2)
        tk.OptionMenu(r1, self.f_sort, "Montant", "Montant (Croissant)", "Montant (Décroissant)").pack(side="left", padx=2)
        r2 = tk.Frame(fb, bg="white"); r2.pack(fill="x", pady=5)
        self.f_start, self.f_end = tk.Entry(r2, width=12), tk.Entry(r2, width=12)
        tk.Label(r2, text="Du:", bg="white").pack(side="left"); self.f_start.pack(side="left", padx=2)
        tk.Label(r2, text="Au:", bg="white").pack(side="left"); self.f_end.pack(side="left", padx=2)
        # Bouton Filtrer
        self.btn(r2, "FILTRER", self.refresh_all, "#5E72E4", side="left")
        # NOUVEAU : Bouton pour réinitialiser uniquement le TRI (le remettre par défaut)
        self.btn(r2, "🔄 RÉCENT", self.reset_sort, "#2DCE89", "#28B377", side="left")
        # Bouton Reset complet
        self.btn(r2, "RESET TOUT", self.reset_filters, "#EDF2F7", "#CBD5E0", "left").config(fg="#4A5568")

    def _ui_form(self, p):
        f = tk.LabelFrame(p, text="➕ OPÉRATION", bg="white", font=("Segoe UI", 8, "bold"), fg="#8898AA", padx=20, pady=10)
        f.pack(fill="x")
        self.vars = {k: tk.StringVar(value=v) for k,v in [("desc",""), ("amt",""), ("type","retrait"), ("cat","Loisir")]}
        rf1 = tk.Frame(f, bg="white"); rf1.pack(fill="x")
        self.create_entry(rf1, "DESCRIPTION", self.vars["desc"], 20).pack(side="left", padx=(0, 10))
        self.create_entry(rf1, "MONTANT", self.vars["amt"], 10).pack(side="left")
        rf2 = tk.Frame(f, bg="white"); rf2.pack(fill="x", pady=5)
        for k in ["type", "cat"]:
            o = ["retrait", "dépôts", "transfert"] if k == "type" else ["Loisir", "Repas", "Facture", "Salaire", "Autre"]
            tk.OptionMenu(rf2, self.vars[k], *o).pack(side="left", padx=5)
        self.save_btn = self.btn(f, "ENREGISTRER", self.save, "#2DCE89", "#24A46D", "top", "x")

    def _ui_table(self, p):
        # Définition des 6 colonnes (ajout de 'C' pour Catégorie)
        self.tree = ttk.Treeview(p, columns=("D", "De", "M", "T", "C", "R"), show="headings", height=8)
        cols = [("D","DATE"), ("De","DESC"), ("M","MONTANT"), ("T","TYPE"), ("C","CATÉGORIE"), ("R","REF")]
        for i, t in cols:
            self.tree.heading(i, text=t)
            # Largeur plus grande pour Description et Catégorie
            w = 150 if i in ["De", "C"] else 90
            self.tree.column(i, width=w, anchor="center")
        self.tree.pack(fill="both", expand=1, pady=10)
        # Couleurs par type
        [self.tree.tag_configure(t, foreground=c) for t,c in [("dépôts","#2DCE89"), ("retrait","#F5365C"), ("transfert","#5E72E4")]]
        self.btn(p, "📥 EXPORTER CSV", self.export, "#11CDEF", "#05B6D4", "top", "x")
        self.tree.bind("<Button-3>", self.on_right_click)
        self.tree.bind("<Double-1>", self.load_for_edit)

    def create_entry(self, m, l, v, w):
        f = tk.Frame(m, bg="white")
        tk.Label(f, text=l, bg="white", fg="#8898AA", font=("Segoe UI", 7, "bold")).pack(anchor="w")
        tk.Entry(f, textvariable=v, width=w, highlightthickness=1, highlightbackground="#CAD1D7", relief="flat").pack(ipady=3)
        return f

    def refresh_all(self):
        try:
            # 1. Solde
            b = float(self.user.get_balance() or 0)
            self.bal_lbl.config(text=f"{b:.2f} €", fg="#F5365C" if b < 0 else "#2DCE89")
            if b < 0: messagebox.showwarning("Budget Buddy", f"Solde négatif : {b:.2f} €")
            # 2. Récupération & Filtrage
            data = self.user.get_filtered_transactions() or []
            filt = []
            f_type, f_cat = self.f_type.get().lower(), self.f_cat.get()
            for t in data:
                if (f_type != "tous types" and t[3].lower() != f_type): continue
                if (f_cat != "Toutes Catégories" and t[4] != f_cat): continue
                # (Ajouter ici vos filtres de dates f_start/f_end si besoin)
                filt.append(t)
            # 3. LOGIQUE DE TRI
            s_val = self.f_sort.get()
            if "Montant (Croissant)" in s_val:
                filt.sort(key=lambda x: float(x[2]))
            elif "Montant (Décroissant)" in s_val:
                filt.sort(key=lambda x: float(x[2]), reverse=True)
            # Si c'est "Date (Récent)", on ne fait RIEN, l'ordre SQL id DESC est conservé.
            # 4. Remplissage tableau
            self.tree.delete(*self.tree.get_children())
            for t in filt:
                sig = "+" if str(t[3]).lower() == "dépôts" else "-"
                self.tree.insert("", "end", values=(
                    t[0], t[1], f"{sig}{float(t[2]):.2f} €", 
                    str(t[3]).upper(), t[4], t[5]
                ), tags=(str(t[3]).lower(),))
            # 5. Graphique
            # On récupère toutes les transactions pour que le graphique puisse piocher dedans
            all_tx = self.user.get_filtered_transactions()
            # On envoie les 3 éléments au graphique
            self.chart_view.update_chart(
                self.user.get_stats_by_category(), 
                self.user.get_stats_monthly(), 
                all_tx
            )
        except Exception as e: print(f"Refresh Error: {e}")

    def save(self):
        d, a, t, c = [self.vars[k].get().strip() for k in ["desc", "amt", "type", "cat"]]
        if not d or not a: return messagebox.showwarning("Incomplet", "Champs requis.")
        try:
            if self.editing_ref:
                self.user.update_transaction(self.editing_ref, d, float(a), t, c)
                self.editing_ref = None; self.save_btn.config(text="ENREGISTRER", bg="#2DCE89")
            else:
                self.user.process_transaction(str(uuid.uuid4())[:8], d, float(a), datetime.datetime.now().strftime("%Y-%m-%d"), t, c)
            self.vars["desc"].set(""); self.vars["amt"].set(""); self.refresh_all()
        except: messagebox.showerror("Erreur", "Données invalides.")

    def reset_filters(self):
        self.f_type.set("Tous Types"); self.f_cat.set("Toutes Catégories"); self.f_sort.set("Montant")
        self.f_start.delete(0, 'end'); self.f_end.delete(0, 'end'); self.refresh_all()

    def export(self):
        if p := filedialog.asksaveasfilename(defaultextension=".csv"):
            with open(p, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["DATE", "DESCRIPTION", "MONTANT", "TYPE"])
                [writer.writerow(self.tree.item(i)["values"]) for i in self.tree.get_children()]

    def logout(self):
        if messagebox.askyesno("Quitter", "Déconnexion ?"): self.master.deiconify(); self.destroy()

    def on_right_click(self, e):
        if iid := self.tree.identify_row(e.y):
            self.tree.selection_set(iid); m = tk.Menu(self, tearoff=0)
            m.add_command(label="❌ Supprimer", command=self.confirm_delete); m.post(e.x_root, e.y_root)

    def confirm_delete(self):
        v = self.tree.item(self.tree.selection()[0])["values"]
        if messagebox.askyesno("Supprimer", f"Supprimer {v[1]} ?"):
            if self.user.delete_transaction(v[4]): self.refresh_all()

    def load_for_edit(self, e):
        if sel := self.tree.selection():
            v = self.tree.item(sel[0])['values']
            self.vars["desc"].set(v[1]); self.vars["type"].set(v[3].lower()); self.editing_ref = v[4]
            self.vars["amt"].set(v[2].replace('+', '').replace('-', '').replace(' €', '').strip())
            self.save_btn.config(text="MODIFIER L'OPÉRATION", bg="#FB6340")

    def reset_sort(self):
        """Remet le tri par défaut (plus récent en haut)."""
        self.f_sort.set("Date (Récent)")
        self.refresh_all()