import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class BudgetChart(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        # Titre
        tk.Label(self, text="RÉPARTITION DES DÉPENSES", bg="white", 
                 font=("Segoe UI", 11, "bold"), fg="#32325D").pack(pady=20)
        
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

    def update_chart(self, stats):
        """Nettoie et redessine le graphique avec les stats SQL."""
        for w in self.container.winfo_children():
            w.destroy()
            
        # On vérifie si on a des données et si la somme n'est pas nulle
        if not stats or sum(float(s[1]) for s in stats) == 0:
            tk.Label(self.container, text="Aucune donnée à afficher", 
                     bg="white", fg="#8898AA").pack(pady=50)
            return

        # Configuration de la figure (allégée)
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        
        # Données
        values = [float(s[1]) for s in stats]
        labels = [s[0] for s in stats]
        colors = ["#5E72E4", "#2DCE89", "#11CDEF", "#FB6340", "#F5365C"]

        ax.pie(values, labels=labels, autopct="%1.1f%%", 
               colors=colors, startangle=140)
        
        fig.tight_layout()
        
        # Intégration Tkinter
        canvas = FigureCanvasTkAgg(fig, self.container)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Fermeture de la figure pour libérer la mémoire vive
        plt.close(fig)