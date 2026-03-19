import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

class BudgetChart(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        
        # --- CACHE DES DONNÉES ---
        self.stats_cache_mois = {}
        self.stats_cache_categories = [] # Sauvegarde pour éviter que le graphique disparaisse
        self.selected_month = "Tous les mois"
        
        # Titre principal
        tk.Label(self, text="RÉPARTITION DES DÉPENSES", bg="white", 
                 font=("Segoe UI", 11, "bold"), fg="#32325D").pack(pady=10)
        
        # Conteneur pour le graphique
        self.chart_container = tk.Frame(self, bg="white")
        self.chart_container.pack(fill="both", expand=True)

        # Zone Calendrier (Boutons)
        self.calendar_container = tk.Frame(self, bg="white", pady=10)
        self.calendar_container.pack(fill="x")

        # Label pour le montant total
        self.amount_lbl = tk.Label(self, text="0.00 €", bg="white",
                                   font=("Segoe UI", 16, "bold"), fg="#5E72E4")
        self.amount_lbl.pack(pady=5)

    def _format_month_name(self, mois_str):
        """Utilise datetime pour transformer '2026-03' en 'MARS 26'."""
        if mois_str == "Tous les mois":
            return "GLOBAL"
        try:
            # Conversion string -> objet datetime
            date_obj = datetime.strptime(mois_str, "%Y-%m")
            # Formatage : %b (mois abrégé), %y (année courte)
            # On met en majuscule pour le style
            return date_obj.strftime("%b %y").upper()
        except:
            return mois_str

    def update_chart(self, stats_categories, stats_mensuelles):
        """Réceptionne les données et rafraîchit l'affichage."""
        # Mise à jour du cache uniquement si on reçoit de nouvelles données
        if stats_categories:
            self.stats_cache_categories = stats_categories
        
        if stats_mensuelles is not None:
            # On stocke les mois en string 'YYYY-MM' pour le dictionnaire
            self.stats_cache_mois = {str(m): float(t) for m, t in stats_mensuelles if m}

        self._render_ui()

    def _render_ui(self):
        """Dessine le graphique et les boutons à partir du cache."""
        # 1. RENDU DU GRAPHIQUE
        for w in self.chart_container.winfo_children():
            w.destroy()

        if not self.stats_cache_categories:
            tk.Label(self.chart_container, text="Aucune dépense enregistrée", 
                     bg="white", fg="#8898AA").pack(pady=40)
        else:
            fig, ax = plt.subplots(figsize=(4, 4), dpi=90)
            labels = [s[0] for s in self.stats_cache_categories]
            tailles = [float(s[1]) for s in self.stats_cache_categories]
            couleurs = ['#5E72E4', '#2DCE89', '#11CDEF', '#F5365C', '#FB6340', '#8965E0']
            ax.pie(tailles, labels=labels, autopct='%1.1f%%', startangle=140, 
                   colors=couleurs, textprops={'fontsize': 8, 'color': '#32325D'})
            ax.axis('equal') 
            canvas = FigureCanvasTkAgg(fig, self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

        # 2. RENDU DU CALENDRIER
        for w in self.calendar_container.winfo_children():
            w.destroy()

        # Tri chronologique des clés 'YYYY-MM' grâce à datetime
        mois_tries = sorted(
            self.stats_cache_mois.keys(), 
            key=lambda x: datetime.strptime(x, "%Y-%m"), 
            reverse=True
        )
        mois_list = ["Tous les mois"] + mois_tries
        
        grid_frame = tk.Frame(self.calendar_container, bg="white")
        grid_frame.pack()

        for i, mois_key in enumerate(mois_list):
            is_selected = (mois_key == self.selected_month)
            btn = tk.Button(
                grid_frame, 
                text=self._format_month_name(mois_key),
                command=lambda m=mois_key: self.select_month(m),
                font=("Segoe UI", 8, "bold"),
                bg="#5E72E4" if is_selected else "#F4F5F7",
                fg="white" if is_selected else "#525F7F",
                activebackground="#5E72E4",
                activeforeground="white",
                relief="flat", padx=10, pady=5, cursor="hand2"
            )
            btn.grid(row=i//4, column=i%4, padx=3, pady=3, sticky="nsew")

        self.update_total_display()

    def select_month(self, month_key):
        """Change le mois sélectionné sans recharger les données SQL."""
        self.selected_month = month_key
        # On redessine tout à partir du cache (évite la disparition du graphique)
        self._render_ui()

    def update_total_display(self):
        """Met à jour uniquement le label du montant."""
        if self.selected_month == "Tous les mois":
            total = sum(self.stats_cache_mois.values())
            self.amount_lbl.config(text=f"{total:.2f} €", fg="#2DCE89")
        elif self.selected_month in self.stats_cache_mois:
            total = self.stats_cache_mois[self.selected_month]
            self.amount_lbl.config(text=f"{total:.2f} €", fg="#5E72E4")