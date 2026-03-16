import mysql.connector

class TransactionManager:
    def __init__(self):
        self.db_config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'budget_buddy'}

    def add_transaction(self, ref, desc, montant, date, type_t):
        """Ajoute une transaction selon tes colonnes : reference, description, montant, date, type."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO transaction (reference, description, montant, date, type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (ref, desc, montant, date, type_t))
            conn.commit()
            print("Transaction enregistrée en base de données.")
        finally:
            if conn.is_connected():
                conn.close()