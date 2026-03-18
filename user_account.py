import mysql.connector
import re
from security import SecurityManager

class UserAccount:
    def __init__(self, nom=None, prenom=None, email=None, motdepasse=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.motdepasse = motdepasse
        # Centralisation de la config DB
        self.db_config = {
            'host': 'localhost', 'user': 'root', 
            'password': 'root', 'database': 'budget_buddy'
        }

    def _get_connection(self):
        """Utilitaire interne pour créer une connexion proprement."""
        return mysql.connector.connect(**self.db_config)

    @staticmethod
    def validate_password_strength(password):
        """Vérifie la robustesse du mot de passe via Regex."""
        if len(password) < 10: return False
        return all([re.search(r, password) for r in [r"[A-Z]", r"[a-z]", r"[0-9]", r"[!@#$%^&*]"]])

    def register(self):
        """Inscrit l'utilisateur en hachant le mot de passe avec un sel unique."""
        conn = None
        try:
            hashed_pw, salt = SecurityManager.hash_password(self.motdepasse)
            conn = self._get_connection()
            cursor = conn.cursor()

            # Insertion double table (utilisateur + membres)
            cursor.execute("INSERT INTO utilisateur (nom, prenom, email, motdepasse, salt) VALUES (%s, %s, %s, %s, %s)",
                           (self.nom, self.prenom, self.email, hashed_pw, salt))
            cursor.execute("INSERT INTO membres (email, motdepasse, salt) VALUES (%s, %s, %s)",
                           (self.email, hashed_pw, salt))

            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur inscription : {e}"); return False
        finally:
            if conn: conn.close()

    @staticmethod
    def login(email, password):
        """Vérifie les identifiants en comparant les hashs via SecurityManager."""
        config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'budget_buddy'}
        conn = None
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT motdepasse, salt FROM membres WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and SecurityManager.verify_password(password, user['motdepasse'], user['salt']):
                return True
            return False
        except Exception as e:
            print(f"Erreur login : {e}"); return False
        finally:
            if conn: conn.close()

    def get_balance(self):
        """Calcule le solde net (Dépôts - [Retraits + Transferts])."""
        conn = self._get_connection()
        try:
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
        finally: conn.close()

    def process_transaction(self, ref, desc, montant, date, t_type, cat="Autre"):
        """Enregistre une nouvelle transaction."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO transaction (reference, description, montant, date, type, categorie) VALUES (%s, %s, %s, %s, %s, %s)",
                           (ref, desc, montant, date, t_type, cat))
            conn.commit()
            return True
        finally: conn.close()

    def get_filtered_transactions(self):
        """Récupère toutes les transactions pour le traitement côté Dashboard."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT date, description, montant, type, categorie FROM transaction ORDER BY id DESC")
            return cursor.fetchall()
        finally: conn.close()

    def get_stats_by_category(self):
        """Agrège les dépenses par catégorie pour le graphique Matplotlib."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = "SELECT categorie, SUM(montant) FROM transaction WHERE type IN ('retrait', 'transfert') GROUP BY categorie"
            cursor.execute(query)
            return cursor.fetchall()
        finally: conn.close()