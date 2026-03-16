import mysql.connector

class TransactionManager:
    def __init__(self):
        self.db_config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'budget_buddy'}

    def add_transaction(self, ref, desc, montant, date, type_t):
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO transaction (reference, description, montant, date, type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (ref, desc, montant, date, type_t))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            if conn and conn.is_connected(): conn.close()