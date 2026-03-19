import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class BudgetChart(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        
        # Titre principal
        tk.Label(self, text="RÉPARTITION DES DÉPENSES", bg="white", 
                 font=("Segoe UI", 11, "bold"), fg="#32325D").pack(pady=10)
        
        # Conteneur pour le graphique (Camembert)
        self.chart_container = tk.Frame(self, bg="white")
        self.chart_container.pack(fill="both", expand=True)

        # Conteneur pour le récapitulatif textuel (Dépenses mensuelles)
        self.info_container = tk.Frame(self, bg="white", pady=10)
        self.info_container.pack(fill="x", side="bottom")

    def update_chart(self, stats_categories, stats_mensuelles):
        """
        stats_categories: [('Loisir', 500.0), ('Repas', 200.0)]
        stats_mensuelles: [('2026-03', 700.0)]
        """
        # --- 1. MISE À JOUR DU CAMEMBERT ---
        for w in self.chart_container.winfo_children():
            w.destroy()

        if not stats_categories or sum(float(s[1]) for s in stats_categories) == 0:
            tk.Label(self.chart_container, text="Aucune dépense enregistrée", 
                     bg="white", fg="#8898AA").pack(pady=40)
        else:
            fig, ax = plt.subplots(figsize=(4, 4), dpi=90)
            labels = [s[0] for s in stats_categories]
            tailles = [float(s[1]) for s in stats_categories]
            couleurs = ['#5E72E4', '#2DCE89', '#11CDEF', '#F5365C', '#FB6340', '#8965E0']

            ax.pie(tailles, labels=labels, autopct='%1.1f%%', startangle=140, 
                   colors=couleurs, textprops={'fontsize': 8, 'color': '#32325D'})
            ax.axis('equal') 

            canvas = FigureCanvasTkAgg(fig, self.chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            plt.close(fig)

        # --- 2. MISE À JOUR DU RÉCAP MENSUEL (TEXTE) ---
        for w in self.info_container.winfo_children():
            w.destroy()

        tk.Label(self.info_container, text="💰 TOTAL PAR MOIS", bg="white",
                 font=("Segoe UI", 8, "bold"), fg="#8898AA").pack()

        if stats_mensuelles:
            for mois, total in stats_mensuelles:
                lbl_text = f"📅 {mois} : {float(total):.2f} €"
                tk.Label(self.info_container, text=lbl_text, bg="white",
                         font=("Segoe UI", 9), fg="#32325D").pack()
        
        self.update_idletasks()