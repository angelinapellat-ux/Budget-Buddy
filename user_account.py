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
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "budget_buddy",
        }

    def _get_connection(self):
        """Utilitaire interne pour créer une connexion proprement."""
        return mysql.connector.connect(**self.db_config)

    @staticmethod
    def validate_password_strength(password):
        """Vérifie la robustesse du mot de passe via Regex."""
        if len(password) < 10:
            return False
        return all(
            [
                re.search(r, password)
                for r in [r"[A-Z]", r"[a-z]", r"[0-9]", r"[!@#$%^&*]"]
            ]
        )

    @staticmethod
    def validate_email(email):
        """Vérifie le format de l'email avec une regex standardisée."""
        # Cette regex vérifie : texte + @ + texte + . + extension (2 lettres min)
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not email:
            return False
        return re.fullmatch(pattern, email.strip()) is not None

    def register(self):
        """Inscrit l'utilisateur en hachant le mot de passe avec un sel unique."""
        conn = None
        try:
            hashed_pw, salt = SecurityManager.hash_password(self.motdepasse)
            conn = self._get_connection()
            cursor = conn.cursor()

            # Insertion double table (utilisateur + membres)
            cursor.execute(
                "INSERT INTO utilisateur (nom, prenom, email, motdepasse, salt) VALUES (%s, %s, %s, %s, %s)",
                (self.nom, self.prenom, self.email, hashed_pw, salt),
            )
            cursor.execute(
                "INSERT INTO membres (email, motdepasse, salt) VALUES (%s, %s, %s)",
                (self.email, hashed_pw, salt),
            )

            conn.commit()
            return True
        except Exception as e:
            print(f"Erreur inscription : {e}")
            return False
        finally:
            if conn:
                conn.close()

    @staticmethod
    def login(email, password):
        """Vérifie les identifiants en comparant les hashs via SecurityManager."""
        config = {
            "host": "localhost",
            "user": "root",
            "password": "root",
            "database": "budget_buddy",
        }
        conn = None
        try:
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT motdepasse, salt FROM membres WHERE email = %s", (email,)
            )
            user = cursor.fetchone()

            if user and SecurityManager.verify_password(
                password, user["motdepasse"], user["salt"]
            ):
                return True
            return False
        except Exception as e:
            print(f"Erreur login : {e}")
            return False
        finally:
            if conn:
                conn.close()

    def get_balance(self):
        """Calcule le solde net UNIQUEMENT pour l'utilisateur connecté."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                COALESCE(SUM(CASE WHEN type = 'dépôts' THEN montant ELSE 0 END), 0) - 
                COALESCE(SUM(CASE WHEN type IN ('retrait', 'transfert') THEN montant ELSE 0 END), 0) 
                FROM transaction
                WHERE user_email = %s
            """
            cursor.execute(query, (self.email,))
            res = cursor.fetchone()

            # Sécurité : si res est None ou res[0] est None, on renvoie 0.0
            if res and res[0] is not None:
                return float(res[0])
            return 0.0
        except Exception as e:
            print(f"❌ Erreur Balance : {e}")
            return 0.0
        finally:
            conn.close()

    def process_transaction(self, ref, desc, montant, date, t_type, cat="Autre"):
        """Enregistre une nouvelle transaction."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # CRUCIAL : on ajoute user_email dans l'INSERT
            query = """
                INSERT INTO transaction (reference, description, montant, date, type, categorie, user_email) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (ref, desc, montant, date, t_type, cat, self.email))
            conn.commit()
            return True
        finally:
            conn.close()

    def get_filtered_transactions(self):
        """Récupère toutes les transactions pour le traitement côté Dashboard."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # CRUCIAL : on ajoute le WHERE user_email = %s
            query = """
                SELECT date, description, montant, type, categorie, reference 
                FROM transaction 
                WHERE user_email = %s 
                ORDER BY id DESC
            """
            cursor.execute(
                query, (self.email,)
            )  # self.email contient l'email de la session
            return cursor.fetchall()
        finally:
            conn.close()

    def get_stats_by_category(self):
        """Agrège les dépenses par catégorie pour l'utilisateur connecté."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # AJOUT DU FILTRE user_email
            query = """
                SELECT categorie, SUM(montant) 
                FROM transaction 
                WHERE type IN ('retrait', 'transfert') AND user_email = %s
                GROUP BY categorie
            """
            cursor.execute(query, (self.email,))
            return cursor.fetchall()
        finally:
            conn.close()

    def get_stats_monthly(self):
        """Regroupe TOUS les mouvements par mois (dépenses et revenus)."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # On retire le filtre 'type IN (...)' pour inclure les dépôts
            query = """
                SELECT DATE_FORMAT(date, '%Y-%m') as mois, SUM(montant) 
                FROM transaction 
                WHERE user_email = %s
                GROUP BY mois 
                ORDER BY mois DESC
            """
            cursor.execute(query, (self.email,))
            res = cursor.fetchall()

            print(f"\n--- TEST FINAL BDD ---")
            print(f"Résultats trouvés: {res}")

            return res
        except Exception as e:
            print(f"Erreur SQL: {e}")
            return []
        finally:
            conn.close()

    def delete_transaction(self, reference):
        """Supprime une transaction spécifique de l'utilisateur."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = "DELETE FROM transaction WHERE reference = %s AND user_email = %s"
            cursor.execute(query, (reference, self.email))
            conn.commit()
            return cursor.rowcount > 0  # Retourne True si une ligne a été supprimée
        except Exception as e:
            print(f"Erreur suppression : {e}")
            return False
        finally:
            conn.close()

    def update_transaction(self, ref, desc, montant, t_type, cat):
        """Met à jour une transaction existante."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            query = """
                UPDATE transaction 
                SET description = %s, montant = %s, type = %s, categorie = %s 
                WHERE reference = %s AND user_email = %s
            """
            cursor.execute(query, (desc, montant, t_type, cat, ref, self.email))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erreur SQL Update : {e}")
            return False
        finally:
            conn.close()
