import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

class BudgetChart(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        
        # --- CACHE DES DONNÉES ---
        self.all_data_raw = [] # Stocke toutes les transactions pour le filtrage
        self.stats_cache_mois = {}
        self.selected_month = "GLOBAL"

        # 1. EN-TÊTE (Titre + Total)
        header = tk.Frame(self, bg="white")
        header.pack(fill="x", pady=5)
        
        tk.Label(header, text="RÉPARTITION DES DÉPENSES", bg="white", 
                 font=("Segoe UI", 10, "bold"), fg="#8898AA").pack()
        
        self.amount_lbl = tk.Label(header, text="0.00 €", bg="white",
                                   font=("Segoe UI", 22, "bold"), fg="#32325D")
        self.amount_lbl.pack()

        # 2. ZONE GRAPHIQUE (Donut muet)
        self.figure, self.ax = plt.subplots(figsize=(3.5, 3.5), dpi=100)
        self.figure.patch.set_facecolor('white')
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().config(bg="white")
        self.canvas.get_tk_widget().pack(fill="x")

        # 3. BARRE DE NAVIGATION (MOIS)
        self.nav_frame = tk.Frame(self, bg="white", pady=5)
        self.nav_frame.pack(fill="x")
        self.months_inner = tk.Frame(self.nav_frame, bg="white")
        self.months_inner.pack(anchor="center")

        # 4. ZONE LÉGENDE (Détails avec % et €)
        # Utilisation d'un Canvas + Scrollbar si la liste est longue
        self.legend_container = tk.Frame(self, bg="white", padx=20)
        self.legend_container.pack(fill="both", expand=True)

    def update_chart(self, stats_categories, stats_mensuelles, all_transactions=None):
        """
        stats_categories: servira pour l'affichage GLOBAL initial
        all_transactions: la liste complète [(date, desc, montant, type, cat, ref)...]
        """
        if all_transactions:
            self.all_data_raw = all_transactions
        
        if stats_mensuelles:
            self.stats_cache_mois = {str(m): float(t) for m, t in stats_mensuelles if m}
            self._update_month_buttons()
            
        self._render_ui()

    def _update_month_buttons(self):
        for w in self.months_inner.winfo_children(): w.destroy()
        self._create_nav_btn("GLOBAL", "GLOBAL")
        sorted_months = sorted(self.stats_cache_mois.keys(), reverse=True)
        for m_key in sorted_months[:5]: # On limite aux 5 derniers mois pour la place
            label = self._format_month_name(m_key)
            self._create_nav_btn(label, m_key)

    def _create_nav_btn(self, text, key):
        is_sel = (self.selected_month == key)
        bg = "#5E72E4" if is_sel else "#F4F5F7"
        fg = "white" if is_sel else "#525F7F"
        btn = tk.Button(self.months_inner, text=text, command=lambda: self.select_month(key),
                        bg=bg, fg=fg, font=("Segoe UI", 8, "bold"), relief="flat", padx=8)
        btn.pack(side="left", padx=2)

    def _format_month_name(self, mois_str):
        try: return datetime.strptime(mois_str, "%Y-%m").strftime("%b %y").upper()
        except: return mois_str

    def select_month(self, month_key):
        self.selected_month = month_key
        self._update_month_buttons()
        self._render_ui()

    def _get_filtered_stats(self):
        """Calcule les stats (catégorie: montant) selon le mois sélectionné."""
        stats = defaultdict(float)
        total = 0
        
        for t in self.all_data_raw:
            # t[0]=date, t[2]=montant, t[3]=type, t[4]=cat
            if t[3].lower() in ['retrait', 'transfert']:
                m_key = t[0][:7] if isinstance(t[0], str) else t[0].strftime("%Y-%m")
                if self.selected_month == "GLOBAL" or m_key == self.selected_month:
                    stats[t[4]] += float(t[2])
                    total += float(t[2])
        
        return dict(stats), total

    def _render_ui(self):
        self.ax.clear()
        for w in self.legend_container.winfo_children(): w.destroy()

        stats_dict, total_montant = self._get_filtered_stats()

        if not stats_dict:
            self.ax.text(0.5, 0.5, "Aucune dépense", ha='center', color='#8898AA')
            self.amount_lbl.config(text="0.00 €")
            self.canvas.draw()
            return

        # Données triées par montant pour la légende
        sorted_stats = sorted(stats_dict.items(), key=lambda x: x[1], reverse=True)
        labels = [s[0] for s in sorted_stats]
        values = [s[1] for s in sorted_stats]
        colors = ['#5E72E4', '#2DCE89', '#F5365C', '#FB6340', '#11CDEF', '#8965E0', '#A8B8D8']

        # 1. DESSIN DU DONUT (SANS TEXTE)
        self.ax.pie(values, startangle=140, colors=colors,
                    explode=[0.03]*len(labels),
                    wedgeprops={'width': 0.4, 'edgecolor': 'white'})
        self.ax.axis('equal')
        self.figure.tight_layout()
        self.canvas.draw()

        # 2. MISE À JOUR DU TOTAL (HAUT)
        self.amount_lbl.config(text=f"{total_montant:.2f} €")

        # 3. LÉGENDE DÉTAILLÉE (BAS)
        for i, (cat, val) in enumerate(sorted_stats):
            percent = (val / total_montant) * 100
            color = colors[i % len(colors)]
            
            row = tk.Frame(self.legend_container, bg="white", pady=4)
            row.pack(fill="x")
            
            # Carré couleur
            tk.Canvas(row, width=10, height=10, bg=color, highlightthickness=0).pack(side="left", padx=(0,10))
            
            # Label : Catégorie (XX%)
            tk.Label(row, text=f"{cat} ({percent:.1f}%)", bg="white", 
                     font=("Segoe UI", 10), fg="#525F7F").pack(side="left")
            
            # Montant à droite
            tk.Label(row, text=f"{val:.2f} €", bg="white", 
                     font=("Segoe UI", 10, "bold"), fg="#32325D").pack(side="right")