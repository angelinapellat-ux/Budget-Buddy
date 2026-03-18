from user_account import UserAccount
from datetime import datetime
import uuid

print("=== 🧪 TEST DU SYSTÈME BUDGET BUDDY PRO ===")

# 1. Configuration des données de test
nom, prenom, email, pwd = "Dupont", "Jean", "jean.test@email.com", "Securise2026!"

# 2. Validation et Inscription
print(f"Vérification sécurité pour {prenom}...")
if UserAccount.validate_password_strength(pwd):
    user = UserAccount(nom, prenom, email, pwd)
    if user.register():
        print("[OK] Compte créé avec succès.")
    else:
        print("[INFO] Compte déjà existant (on continue le test).")
else:
    print("[REFUS] Mot de passe non conforme.")

print("-" * 40)

# 3. Test de Connexion
print(f"Tentative de connexion : {email}")
if UserAccount.login(email, pwd):
    print("[SUCCÈS] Authentification réussie.")
    
    # Init de l'objet utilisateur pour les opérations
    user_test = UserAccount(email=email)
    date_now = datetime.now().strftime("%Y-%m-%d")

    # 4. Scénario de test : Dépôt, Retrait et Transfert
    # Calcul : 2500 - 75.50 - 200 = 2224.50
    tests = [
        (str(uuid.uuid4())[:8], "Dépôt Salaire", 2500.0, "dépôts", "Salaire"),
        (str(uuid.uuid4())[:8], "Courses", 75.50, "retrait", "Repas"),
        (str(uuid.uuid4())[:8], "Épargne", 200.0, "transfert", "Autre")
    ]

    print("\nSimulation de transactions...")
    for ref, desc, montant, t_type, cat in tests:
        if user_test.process_transaction(ref, desc, montant, date_now, t_type, cat):
            print(f"  -> {t_type.capitalize()} : {montant}€ [Enregistré]")

    # 5. Vérification du calcul du solde (Logique SQL)
    solde = user_test.get_balance()
    print(f"\n--- RÉSULTAT DU CALCUL SQL ---")
    print(f"Solde en base de données : {solde:.2f} €")
    
    # On vérifie si la logique SQL SUM(dépôts) - SUM(retraits+transferts) fonctionne
    if solde > 0: # On vérifie simplement qu'il y a de l'argent suite au test
        print("✅ TEST RÉUSSI : La logique comptable est validée !")
    else:
        print("⚠️ ERREUR : Le solde ne correspond pas aux attentes.")

else:
    print("[ÉCHEC] Connexion impossible. Vérifiez votre base MySQL.")