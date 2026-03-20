import mysql.connector
import re
from security import SecurityManager

class UserAccount:
    def __init__(self, nom=None, prenom=None, email=None, motdepasse=None):
        self.nom, self.prenom, self.email, self.motdepasse = nom, prenom, email, motdepasse
        self.db_config = {
            "host": "localhost", "user": "root", 
            "password": "root", "database": "budget_buddy"
        }

    def _execute(self, query, params=(), fetch_one=False, fetch_all=False):
        """Exécuteur SQL robuste."""
        conn = mysql.connector.connect(**self.db_config)
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if fetch_one: return cursor.fetchone()
            if fetch_all: return cursor.fetchall()
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Erreur SQL: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def validate_password_strength(password):
        if len(password) < 10: return False
        return all(re.search(r, password) for r in [r"[A-Z]", r"[a-z]", r"[0-9]", r"[!@#$%^&*]"])

    @staticmethod
    def validate_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.fullmatch(pattern, (email or "").strip()) is not None

    def register(self):
        h_pw, salt = SecurityManager.hash_password(self.motdepasse)
        q1 = "INSERT INTO utilisateur (nom, prenom, email, motdepasse, salt) VALUES (%s, %s, %s, %s, %s)"
        q2 = "INSERT INTO membres (email, motdepasse, salt) VALUES (%s, %s, %s)"
        return self._execute(q1, (self.nom, self.prenom, self.email, h_pw, salt)) and \
               self._execute(q2, (self.email, h_pw, salt))

    @classmethod
    def login(cls, email, password):
        user = cls()._execute("SELECT motdepasse, salt FROM membres WHERE email = %s", (email,), fetch_one=True)
        return True if user and SecurityManager.verify_password(password, user[0], user[1]) else False

    def get_balance(self):
        query = """
            SELECT COALESCE(SUM(CASE WHEN type = 'dépôts' THEN montant ELSE 0 END), 0) - 
                   COALESCE(SUM(CASE WHEN type IN ('retrait', 'transfert') THEN montant ELSE 0 END), 0) 
            FROM transaction WHERE user_email = %s
        """
        res = self._execute(query, (self.email,), fetch_one=True)
        return float(res[0]) if res and res[0] is not None else 0.0

    def process_transaction(self, ref, desc, montant, date, t_type, cat="Autre"):
        query = "INSERT INTO transaction (reference, description, montant, date, type, categorie, user_email) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        return self._execute(query, (ref, desc, montant, date, t_type, cat, self.email))

    def get_filtered_transactions(self):
        """Récupère les transactions triées par ID descendant (plus récent en haut)."""
        query = "SELECT date, description, montant, type, categorie, reference FROM transaction WHERE user_email = %s ORDER BY id DESC"
        return self._execute(query, (self.email,), fetch_all=True) or []

    def get_stats_by_category(self):
        query = "SELECT categorie, SUM(montant) FROM transaction WHERE type IN ('retrait', 'transfert') AND user_email = %s GROUP BY categorie"
        return self._execute(query, (self.email,), fetch_all=True) or []

    def get_stats_monthly(self):
        """Récupère les stats par mois pour le graphique."""
        query = "SELECT DATE_FORMAT(date, '%Y-%m') as mois, SUM(montant) FROM transaction WHERE user_email = %s GROUP BY mois ORDER BY mois DESC"
        return self._execute(query, (self.email,), fetch_all=True) or []

    def delete_transaction(self, reference):
        return self._execute("DELETE FROM transaction WHERE reference = %s AND user_email = %s", (reference, self.email))

    def update_transaction(self, ref, desc, montant, t_type, cat):
        query = "UPDATE transaction SET description = %s, montant = %s, type = %s, categorie = %s WHERE reference = %s AND user_email = %s"
        return self._execute(query, (desc, montant, t_type, cat, ref, self.email))