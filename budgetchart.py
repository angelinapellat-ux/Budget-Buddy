import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import uuid, csv, matplotlib.pyplot as plt

class BudgetChart(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="white")
        self.label = tk.Label(self, text="RÉPARTITION DES DÉPENSES", bg="white", font=("Segoe UI", 11, "bold"), fg="#32325D")
        self.label.pack(pady=20)
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

    def update_chart(self, stats):
        """Logique de dessin du graphique uniquement."""
        for w in self.container.winfo_children():
            w.destroy()
            
        if not stats:
            tk.Label(self.container, text="Aucune donnée à afficher", bg="white", fg="#8898AA").pack(pady=50)
            return

        # Création de la figure Matplotlib
        fig, ax = plt.subplots(figsize=(4, 4), dpi=100)
        ax.pie(
            [float(s[1]) for s in stats],
            labels=[s[0] for s in stats],
            autopct="%1.1f%%",
            colors=["#5E72E4", "#2DCE89", "#11CDEF", "#FB6340", "#F5365C"],
            startangle=140
        )
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, self.container)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)