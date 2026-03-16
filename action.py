from user_account import UserAccount
from transaction import TransactionManager

print("--- Test du système Budget Buddy ---")

# 1. Tentative d'Inscription
# Note : Le mot de passe doit faire 10 car. + Maj + Chiffre + Spécial pour passer la validation
nom, prenom, email, pwd = "Dupont", "Jean", "jean@email.com", "Securise2026!"

if UserAccount.validate_password_strength(pwd):
    new_user = UserAccount(nom, prenom, email, pwd)
    if new_user.register():
        print(f"[OK] Compte créé pour {prenom} dans les tables 'utilisateur' et 'membres'.")
    else:
        print("[ERREUR] L'inscription a échoué (Email déjà présent ou serveur MySQL éteint).")
else:
    print("[REFUS] Le mot de passe ne respecte pas les critères de sécurité.")

print("-" * 30)

# 2. Test de connexion
print(f"Tentative de connexion pour : {email}")
if UserAccount.login(email, pwd):
    print("[SUCCÈS] Accès autorisé. Connexion à la table 'membres' réussie.")
    
    # 3. Ajout d'une transaction
    print("Enregistrement d'une transaction de test...")
    tm = TransactionManager()
    # On utilise la date du jour
    if tm.add_transaction("TXN-TEST-001", "Achat test console", 45, "2026-03-16", "retrait"):
        print("[OK] Transaction enregistrée dans la table 'transaction'.")
    else:
        print("[ERREUR] Échec de l'enregistrement de la transaction.")
else:
    print("[ÉCHEC] Accès refusé. Vérifiez vos identifiants dans MySQL.")