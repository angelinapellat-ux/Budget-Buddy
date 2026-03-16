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
        """Vérifie : 10 caractères, Majuscule, Chiffre, Caractère spécial."""
        if len(password) < 10: return False
        if not re.search(r"[A-Z]", password): return False
        if not re.search(r"[0-9]", password): return False
        if not re.search(r"[!@#$%^&*]", password): return False
        return True

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        """Inscrit dans utilisateur et membres. Retourne True si OK."""
        conn = None
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            # Insertion Profil
            cursor.execute("INSERT INTO utilisateur (nom, prenom, email, motdepasse) VALUES (%s, %s, %s, %s)", 
                           (self.nom, self.prenom, self.email, self.motdepasse))
            # Insertion Authentification
            cursor.execute("INSERT INTO membres (email, motdepasse) VALUES (%s, %s)", 
                           (self.email, self.motdepasse))
            conn.commit()
            return True
        except mysql.connector.Error:
            return False
        finally:
            if conn and conn.is_connected(): conn.close()

    @staticmethod
    def login(email, password):
        """Vérifie les accès dans la table membres."""
        h_pwd = hashlib.sha256(password.encode()).hexdigest()
        config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'budget_buddy'}
        conn = None
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM membres WHERE email = %s AND motdepasse = %s", (email, h_pwd))
            return cursor.fetchone() is not None
        except: return False
        finally:
            if conn and conn.is_connected(): conn.close()
    
    def get_balance(self):
        """Calcule le solde total en soustrayant les retraits des dépôts."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            # On calcule la somme : dépôts (+) et retraits (-)
            query = """
                SELECT 
                SUM(CASE WHEN type = 'dépôts' THEN montant ELSE 0 END) - 
                SUM(CASE WHEN type = 'retrait' THEN montant ELSE 0 END) 
                FROM transaction
            """
            cursor.execute(query)
            result = cursor.fetchone()[0]
            return float(result) if result else 0.0
        except: return 0.0
        finally:
            if conn.is_connected(): conn.close()

    def process_transaction(self, ref, desc, montant, date, t_type):
        """Méthode de liaison pour insérer une transaction depuis le dashboard."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            query = "INSERT INTO transaction (reference, description, montant, date, type) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (ref, desc, montant, date, t_type))
            conn.commit()
            return True
        except: return False
        finally:
            if conn.is_connected(): conn.close()