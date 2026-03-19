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
        self.editing_ref = None
    def setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview", background="white", rowheight=35, font=("Segoe UI", 10))
        s.configure(
            "Treeview.Heading", background="#F6F9FC", font=("Segoe UI", 9, "bold")
        )

    def btn(self, master, text, cmd, bg, hover="#324CBB", side=None, fill=None):
        """Utilitaire pour créer des boutons stylisés rapidement."""
        b = tk.Button(
            master,
            text=text,
            command=cmd,
            bg=bg,
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
        )
        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=bg))
        if side:
            b.pack(side=side, padx=5, pady=5, fill=fill)
        return b

    def build_ui(self):
        # Header
        h = tk.Frame(self, bg="#32325D", height=60)
        h.pack(fill="x")
        tk.Label(
            h,
            text="TABLEAU DE BORD",
            fg="white",
            bg="#32325D",
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=20)
        self.btn(h, "DÉCONNEXION", self.logout, "#F5365C", "#D32F2F", side="right")

        cnt = tk.Frame(self, bg="#F8F9FE")
        cnt.pack(fill="both", expand=True, padx=20, pady=20)
        left = tk.Frame(cnt, bg="#F8F9FE")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Solde Card
        card = tk.Frame(
            left,
            bg="white",
            padx=20,
            pady=15,
            highlightthickness=1,
            highlightbackground="#E9ECEF",
        )
        card.pack(fill="x", pady=(0, 15))
        tk.Label(
            card,
            text="SOLDE ACTUEL",
            bg="white",
            fg="#8898AA",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")
        self.bal_lbl = tk.Label(
            card, text="-- €", bg="white", font=("Segoe UI", 28, "bold")
        )
        self.bal_lbl.pack(anchor="w")

        # Filtres
        fb = tk.LabelFrame(
            left,
            text="🔍 FILTRES",
            bg="white",
            font=("Segoe UI", 8, "bold"),
            fg="#8898AA",
            padx=10,
            pady=5,
        )
        fb.pack(fill="x", pady=(0, 15))
        self.f_type, self.f_cat, self.f_sort = (
            tk.StringVar(value="Tous Types"),
            tk.StringVar(value="Toutes Catégories"),
            tk.StringVar(value="Montant"),
        )

        r1 = tk.Frame(fb, bg="white")
        r1.pack(fill="x")
        for v, opt in [
            (self.f_type, ["Tous Types", "retrait", "dépôts", "transfert"]),
            (
                self.f_cat,
                ["Toutes Catégories", "Loisir", "Repas", "Facture", "Salaire", "Autre"],
            ),
            (self.f_sort, ["Montant (Croissant)", "Montant (Décroissant)"]),
        ]:  # <--- Changé ici
            tk.OptionMenu(r1, v, *opt).pack(side="left", padx=2)

        r2 = tk.Frame(fb, bg="white")
        r2.pack(fill="x", pady=5)
        self.f_start, self.f_end = tk.Entry(r2, width=12), tk.Entry(r2, width=12)
        for t, e in [("Du:", self.f_start), ("Au:", self.f_end)]:
            tk.Label(r2, text=t, bg="white").pack(side="left", padx=2)
            e.pack(side="left", padx=2)
        self.btn(r2, "FILTRER", self.refresh_all, "#5E72E4", side="left")
        self.btn(
            r2, "RESET", self.reset_filters, "#EDF2F7", "#CBD5E0", side="left"
        ).config(fg="#4A5568")

        # Formulaire
        form = tk.LabelFrame(
            left,
            text="➕ OPÉRATION",
            bg="white",
            font=("Segoe UI", 8, "bold"),
            fg="#8898AA",
            padx=20,
            pady=10,
        )
        form.pack(fill="x")
        self.vars = {
            k: tk.StringVar(value=v)
            for k, v in [
                ("desc", ""),
                ("amt", ""),
                ("type", "retrait"),
                ("cat", "Loisir"),
            ]
        }

        rf1 = tk.Frame(form, bg="white")
        rf1.pack(fill="x")
        self.create_entry(rf1, "DESCRIPTION", self.vars["desc"], 20).pack(
            side="left", padx=(0, 10)
        )
        self.create_entry(rf1, "MONTANT", self.vars["amt"], 10).pack(side="left")

        rf2 = tk.Frame(form, bg="white")
        rf2.pack(fill="x", pady=5)
        for k in ["type", "cat"]:
            opts = (
                ["retrait", "dépôts", "transfert"]
                if k == "type"
                else ["Loisir", "Repas", "Facture", "Salaire", "Autre"]
            )
            tk.OptionMenu(rf2, self.vars[k], *opts).pack(side="left", padx=5)

        self.btn(
            form, "ENREGISTRER", self.save, "#2DCE89", "#24A46D", side="top", fill="x"
        )

        # Tableau
        self.tree = ttk.Treeview(
            left, columns=("D", "De", "M", "T", "R"), show="headings", height=8
        )
        for c, h in zip(
            ("D", "De", "M", "T", "R"), ("DATE", "DESC", "MONTANT", "TYPE", "REF")
        ):
            width = 120 if c == "R" else 90  # Plus large pour la référence
            self.tree.heading(c, text=h)
            self.tree.column(c, width=width, anchor="center")
        self.tree.pack(fill="both", expand=True, pady=10)
        for t, col in [
            ("dépôts", "#2DCE89"),
            ("retrait", "#F5365C"),
            ("transfert", "#5E72E4"),
        ]:
            self.tree.tag_configure(t, foreground=col)

        self.btn(
            left,
            "📥 EXPORTER CSV",
            self.export,
            "#11CDEF",
            "#05B6D4",
            side="top",
            fill="x",
        )
        # On lie le clic droit (Button-3 sur Windows/Linux, Button-2 sur Mac)
        self.tree.bind("<Button-3>", self.on_right_click)
        self.tree.bind("<Double-1>", self.load_for_edit)
        # Graphique
        self.chart_view = BudgetChart(
            cnt, highlightthickness=1, highlightbackground="#E9ECEF"
        )
        self.chart_view.pack(side="right", fill="both", expand=True, padx=(10, 0))

    def create_entry(self, master, label, var, width):
        f = tk.Frame(master, bg="white")
        tk.Label(
            f, text=label, bg="white", fg="#8898AA", font=("Segoe UI", 7, "bold")
        ).pack(anchor="w")
        tk.Entry(
            f,
            textvariable=var,
            width=width,
            highlightthickness=1,
            highlightbackground="#CAD1D7",
            relief="flat",
        ).pack(ipady=3)
        return f

    def refresh_all(self):
        # 1. Gestion du Solde
        try:
            bal = self.user.get_balance()
            bal = float(bal) if bal is not None else 0.0
            self.bal_lbl.config(
                text=f"{bal:.2f} €", fg="#F5365C" if bal < 0 else "#2DCE89"
            )

            if bal < 0:
                messagebox.showwarning(
                    "Alerte Découvert",
                    f"Attention ! Votre solde est négatif ({bal:.2f} €).",
                )
        except Exception as e:
            print(f"Erreur Solde: {e}")

        # 2. Récupération et Filtrage des données (Tableau)
        try:
            data = self.user.get_filtered_transactions()
            if not data:
                data = []

            filtered = [
                t
                for t in data
                if (self.f_type.get() == "Tous Types" or t[3] == self.f_type.get())
                and (
                    self.f_cat.get() == "Toutes Catégories" or t[4] == self.f_cat.get()
                )
                and (not self.f_start.get() or str(t[0]) >= self.f_start.get())
                and (not self.f_end.get() or str(t[0]) <= self.f_end.get())
            ]

            # 3. Tri
            s = self.f_sort.get()
            if "Montant" in s:
                filtered.sort(key=lambda x: float(x[2]), reverse=("Décroissant" in s))

            # 4. Mise à jour du Tableau (Treeview)
            self.tree.delete(*self.tree.get_children())
            for t in filtered:
                try:
                    sig = "+" if str(t[3]).lower() == "dépôts" else "-"
                    ref = t[5] if len(t) > 5 else "N/A"
                    self.tree.insert(
                        "",
                        "end",
                        values=(
                            t[0],
                            t[1],
                            f"{sig}{float(t[2]):.2f} €",
                            str(t[3]).upper(),
                            ref,
                        ),
                        tags=(str(t[3]).lower(),),
                    )
                except Exception as row_err:
                    print(f"Erreur ligne tableau: {row_err}")
        except Exception as e:
            print(f"Erreur Tableau: {e}")
            messagebox.showerror("Erreur", "Impossible de charger la liste.")

        # 5. Mise à jour du Graphique (Camembert + Texte Mensuel)
        try:
            # On récupère les deux sources de données
            stats_categories = self.user.get_stats_by_category()
            stats_mensuelles = self.user.get_stats_monthly()
            
            # On envoie les deux à la vue graphique modifiée
            self.chart_view.update_chart(stats_categories, stats_mensuelles)
        except Exception as e:
            print(f"Erreur lors de la mise à jour du graphique : {e}")

    def save(self):
        # 1. Récupération des valeurs
        d = self.vars["desc"].get().strip()
        a_str = self.vars["amt"].get().strip()
        t_type = self.vars["type"].get()
        cat = self.vars["cat"].get()

        # 2. Vérification des champs vides
        if not d or not a_str:
            return messagebox.showwarning("Incomplet", "Veuillez remplir la description et le montant.")

        # 3. Conversion du montant
        try:
            montant_float = float(a_str)
        except ValueError:
            return messagebox.showerror("Erreur", "Le montant doit être un nombre valide.")

        # --- LOGIQUE DE SAUVEGARDE ---
        if hasattr(self, 'editing_ref') and self.editing_ref:
            # MODE MODIFICATION
            success = self.user.update_transaction(
                self.editing_ref, d, montant_float, t_type, cat
            )
            # On réinitialise l'état du bouton et de la référence
            self.editing_ref = None
            self.save_btn.config(text="ENREGISTRER", bg="#2DCE89") # Retour au vert
        else:
            # MODE CRÉATION
            ref_generee = str(uuid.uuid4())[:8]
            date_du_jour = datetime.now().strftime("%Y-%m-%d")
            success = self.user.process_transaction(
                ref_generee, d, montant_float, date_du_jour, t_type, cat
            )

        # 5. Gestion du résultat
        if success:
            # Nettoyage du formulaire
            self.vars["desc"].set("")
            self.vars["amt"].set("")
            
            try:
                # Appelle la nouvelle version de refresh_all (Camembert + Texte)
                self.refresh_all()
            except Exception as e:
                print(f"Erreur lors du rafraîchissement : {e}")
                messagebox.showerror("Erreur Interface", "Enregistré, mais l'affichage a planté.")
        else:
            messagebox.showerror("Erreur", "L'opération a échoué en base de données.")

    def reset_filters(self):
        self.f_type.set("Tous Types")
        self.f_cat.set("Toutes Catégories")
        self.f_sort.set("Date (Récents)")
        self.f_start.delete(0, "end")
        self.f_end.delete(0, "end")
        self.refresh_all()

    def export(self):
        if p := filedialog.asksaveasfilename(defaultextension=".csv"):
            with open(p, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["DATE", "DESCRIPTION", "MONTANT", "TYPE"])
                for i in self.tree.get_children():
                    writer.writerow(self.tree.item(i)["values"])

    def logout(self):
        if messagebox.askyesno("Quitter", "Se déconnecter ?"):
            self.master.deiconify()
            self.destroy()

    def on_right_click(self, event):
        # On sélectionne la ligne sous le curseur
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return

        self.tree.selection_set(item_id)

        # Création du menu surgissant
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(
            label="❌ Supprimer cette opération", command=self.confirm_delete
        )
        menu.post(event.x_root, event.y_root)

    def confirm_delete(self):
        selected = self.tree.selection()
        if not selected:
            return

        # On récupère les valeurs de la ligne (la REF est à l'index 4)
        values = self.tree.item(selected[0])["values"]
        ref = values[4]
        desc = values[1]

        if messagebox.askyesno("Confirmation", f"Supprimer l'opération '{desc}' ?"):
            if self.user.delete_transaction(ref):
                messagebox.showinfo("Succès", "Opération supprimée.")
                self.refresh_all()
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer l'opération.")
    def load_for_edit(self, event):
        selected = self.tree.selection()
        if not selected: return
        
        values = self.tree.item(selected[0])['values']
        
        # On remplit le formulaire avec les valeurs de la ligne
        self.vars["desc"].set(values[1])
        # On nettoie le montant (enlever le '+' ou '-' et le '€')
        amt = values[2].replace('+', '').replace('-', '').replace(' €', '').strip()
        self.vars["amt"].set(amt)
        self.vars["type"].set(values[3].lower())
        # Note : Si tu n'affiches pas la catégorie dans le tableau, 
        # il faudra peut-être l'ajouter ou la laisser par défaut.
        
        self.editing_ref = values[4] # On stocke la ref pour le prochain "Enregistrer"