import mysql.connector
import hashlib
import re

class UserAccount:
    def __init__(self, nom=None, prenom=None, email=None, motdepasse=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.motdepasse = self._hash_password(motdepasse) if motdepasse else None
        self.db_config = {
            'host': 'localhost', 
            'user': 'root', 
            'password': 'root', 
            'database': 'budget_buddy'
        }

    @staticmethod
    def validate_password_strength(password):
        if len(password) < 10: return False
        if not re.search(r"[A-Z]", password): return False
        if not re.search(r"[a-z]", password): return False
        if not re.search(r"[0-9]", password): return False
        if not re.search(r"[!@#$%^&*]", password): return False
        return True

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO utilisateur (nom, prenom, email, motdepasse) VALUES (%s, %s, %s, %s)", 
                           (self.nom, self.prenom, self.email, self.motdepasse))
            cursor.execute("INSERT INTO membres (email, motdepasse) VALUES (%s, %s)", 
                           (self.email, self.motdepasse))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def login(email, password):
        h_pwd = hashlib.sha256(password.encode()).hexdigest()
        config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'budget_buddy'}
        conn = None
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM membres WHERE email = %s AND motdepasse = %s", (email, h_pwd))
            return cursor.fetchone() is not None
        except Exception:
            return False
        finally:
            if conn and conn.is_connected(): conn.close()

    def get_balance(self):
        """Calcule le solde en déduisant retraits ET transferts."""
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = """
                SELECT 
                COALESCE(SUM(CASE WHEN type = 'dépôts' THEN montant ELSE 0 END), 0) - 
                COALESCE(SUM(CASE WHEN type IN ('retrait', 'transfert') THEN montant ELSE 0 END), 0) 
                FROM transaction
            """
            cursor.execute(query)
            res = cursor.fetchone()[0]
            return float(res) if res else 0.0
        finally:
            if conn and conn.is_connected(): conn.close()

    def process_transaction(self, ref, desc, montant, date, t_type, cat="Autre"):
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO transaction (reference, description, montant, date, type, categorie) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (ref, desc, montant, date, t_type, cat))
            conn.commit()
            return True
        finally:
            if conn and conn.is_connected(): conn.close()

    def get_filtered_transactions(self, t_type="Tous", date_debut=None, date_fin=None, tri_montant=None):
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "SELECT date, description, montant, type, categorie FROM transaction WHERE 1=1"
            params = []

            if t_type != "Tous":
                query += " AND type = %s"; params.append(t_type)
            if date_debut and date_fin:
                query += " AND date BETWEEN %s AND %s"; params.append(date_debut); params.append(date_fin)

            if tri_montant in ["ASC", "DESC"]:
                query += f" ORDER BY montant {tri_montant}"
            else:
                query += " ORDER BY id DESC"

            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            if conn and conn.is_connected(): conn.close()

    def get_stats_by_category(self):
        """Inclut les transferts dans les stats pour une vision globale des sorties d'argent."""
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "SELECT categorie, SUM(montant) FROM transaction WHERE type IN ('retrait', 'transfert') GROUP BY categorie"
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            if conn and conn.is_connected(): conn.close()