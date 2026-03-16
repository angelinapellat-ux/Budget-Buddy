import mysql.connector
import hashlib

class UserAccount:
    def __init__(self, nom=None, prenom=None, email=None, motdepasse=None):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.motdepasse = self._hash_password(motdepasse) if motdepasse else None
        
        # Paramètres de connexion MySQL
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'root', # Vérifie ton mot de passe MySQL
            'database': 'budget_buddy'
        }

    def _hash_password(self, password):
        """Hachage SHA-256 pour sécuriser le mot de passe."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        """Remplit les tables 'utilisateur' et 'membres' simultanément."""
        try:
            conn = mysql.connector.connect(**self.db_config)
            cursor = conn.cursor()
            
            # 1. Insertion dans la table utilisateur
            query_user = "INSERT INTO utilisateur (nom, prenom, email, motdepasse) VALUES (%s, %s, %s, %s)"
            cursor.execute(query_user, (self.nom, self.prenom, self.email, self.motdepasse))
            
            # 2. Insertion dans la table membres (connexion)
            query_member = "INSERT INTO membres (email, motdepasse) VALUES (%s, %s)"
            cursor.execute(query_member, (self.email, self.motdepasse))
            
            conn.commit()
            print(f"Compte créé avec succès pour {self.prenom} !")
            
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'inscription : {err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    @staticmethod
    def login(email, password):
        """Vérifie les identifiants dans la table 'membres'."""
        h_pwd = hashlib.sha256(password.encode()).hexdigest()
        config = {'host': 'localhost', 'user': 'root', 'password': 'root', 'database': 'budget_buddy'}
        
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM membres WHERE email = %s AND motdepasse = %s", (email, h_pwd))
            if cursor.fetchone():
                return True
            return False
        finally:
            if conn.is_connected():
                conn.close()