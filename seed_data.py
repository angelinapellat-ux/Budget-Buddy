import mysql.connector
from datetime import datetime, timedelta

def seed():
    # VERIFIE LE MOT DE PASSE ICI (celui de ta capture d'écran)
    config = {
        'host': 'localhost', 
        'user': 'root', 
        'password': 'root', # Mets '' si tu n'as pas de mot de passe
        'database': 'budget_buddy'
    }
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        data = [
            ("REF001", "Salaire", 2500.00, "dépôts"),
            ("REF002", "Loyer", 800.00, "retrait"),
            ("REF003", "Courses", 150.00, "retrait"),
            ("REF004", "Vente Leboncoin", 50.00, "dépôts"),
            ("REF005", "Restaurant", 45.00, "retrait")
        ]

        query = "INSERT INTO transaction (reference, description, montant, date, type) VALUES (%s, %s, %s, %s, %s)"
        
        today = datetime.now()
        for i, (ref, desc, montant, t_type) in enumerate(data):
            date_tx = (today - timedelta(days=i)).strftime("%Y-%m-%d")
            cursor.execute(query, (ref, desc, montant, date_tx, t_type))

        conn.commit()
        print("✅ Données insérées ! Relance ton Dashboard pour voir le changement.")
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    seed()