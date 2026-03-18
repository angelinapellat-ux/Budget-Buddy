import hashlib
import secrets
import hmac

# LE POIVRE : Clé secrète unique au code source
SECRET_PEPPER = "Budg3t_Buddy_S3cur1ty_2024!"

class SecurityManager:
    @staticmethod
    def hash_password(password, salt=None):
        """Hachage sécurisé : Mot de passe + Sel + Poivre."""
        # Génère un sel unique de 32 caractères hexadécimaux si nécessaire
        salt = salt or secrets.token_hex(16)
        
        # Concaténation et hachage SHA-256
        data = (password + salt + SECRET_PEPPER).encode()
        hash_res = hashlib.sha256(data).hexdigest()
        
        return hash_res, salt

    @staticmethod
    def verify_password(input_password, stored_hash, stored_salt):
        """Vérifie la correspondance par comparaison sécurisée."""
        new_hash, _ = SecurityManager.hash_password(input_password, salt=stored_salt)
        
        # hmac.compare_digest est plus sûr qu'un simple '==' 
        # car il protège contre les attaques par analyse de temps (timing attacks).
        return hmac.compare_digest(new_hash, stored_hash)