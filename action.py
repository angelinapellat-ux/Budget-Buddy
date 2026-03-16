from user_account import UserAccount
from transaction import TransactionManager

# 1. Inscription (Remplit utilisateur + membres)
new_user = UserAccount("Dupont", "Jean", "jean@email.com", "Securise2026!")
new_user.register()

# 2. Test de connexion
if UserAccount.login("jean@email.com", "Securise2026!"):
    print("Accès autorisé.")
    
    # 3. Ajout d'une transaction
    tm = TransactionManager()
    tm.add_transaction("TXN001", "Achat Supermarché", 45, "2026-03-16", "retrait")
else:
    print("Accès refusé.")