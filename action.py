from user_account import UserAccount
from datetime import datetime
import uuid

print("--- 🧪 Test du Système Budget Buddy Pro ---")

# 1. Configuration des données de test
nom, prenom, email, pwd = "Dupont", "Jean", "jean.test@email.com", "Securise2026!"

# 2. Validation et Inscription
print(f"Vérification du mot de passe pour {prenom}...")
if UserAccount.validate_password_strength(pwd):
    new_user = UserAccount(nom, prenom, email, pwd)
    if new_user.register():
        print(f"[OK] Compte créé avec succès.")
    else:
        print("[INFO] Compte déjà existant ou erreur MySQL (on continue le test).")
else:
    print("[REFUS] Le mot de passe ne respecte pas les critères (10 car. + Maj + Chiffre + Spécial).")

print("-" * 40)

# 3. Test de Connexion
print(f"Tentative de connexion : {email}")
if UserAccount.login(email, pwd):
    print("[SUCCÈS] Authentification réussie.")
    
    # Initialisation de l'objet utilisateur pour les opérations
    user = UserAccount(email=email)
    date_today = datetime.now().strftime("%Y-%m-%d")

    # 4. Test des 3 types d'opérations
    tests = [
        ("REF-DEP", "Dépôt Salaire", 2500.0, "dépôts", "Salaire"),
        ("REF-RET", "Achat Courses", 75.50, "retrait", "Repas"),
        ("REF-TRA", "Virement Épargne", 200.0, "transfert", "Autre")
    ]

    print("\nEnregistrement des transactions de test...")
    for ref, desc, montant, t_type, cat in tests:
        if user.process_transaction(ref, desc, montant, date_today, t_type, cat):
            print(f"  [OK] {t_type.capitalize()} de {montant}€ enregistré.")
        else:
            print(f"  [ERREUR] Échec pour le {t_type}.")

    # 5. Vérification finale du solde
    # Calcul attendu : 2500 (dépôt) - 75.50 (retrait) - 200 (transfert) = 2224.50
    solde_final = user.get_balance()
    print(f"\n--- RÉSULTAT FINAL ---")
    print(f"Solde calculé en base : {solde_final:.2f} €")
    
    if solde_final == 2224.50:
        print("✅ TEST RÉUSSI : Le transfert est bien déduit du solde !")
    else:
        print("⚠️ ATTENTION : Le calcul du solde semble incorrect.")

else:
    print("[ÉCHEC] Connexion impossible. Vérifiez MySQL.")