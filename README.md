# 💰 Lancement
python main.py

Compte Test : 
email : un.deux@test.com
mot de passe : Azertyuiop@.1

## 🚀 Récapitulatif des Fonctionnalités : Budget Buddy Pro

### 1. 🔐 Sécurité et Gestion des Comptes
* **Système d'Authentification :** Connexion sécurisée liée à l'e-mail de l'utilisateur.
* **Sessions Personnalisées :** L'application identifie l'utilisateur connecté et charge uniquement ses données propres (via `user_email`).
* **Déconnexion Sécurisée :** Bouton de déconnexion rapide avec retour à l'écran d'accueil.

### 2. 💰 Gestion des Opérations Financières
* **Saisie Intuitive :** Formulaire complet permettant d'enregistrer :
    * La **Description** de l'achat.
    * Le **Montant** (avec gestion des nombres décimaux).
    * Le **Type d'opération** (Retrait, Dépôt, Transfert).
    * La **Catégorie** (Loisir, Repas, Facture, Salaire, Autre).
* **Identifiants Uniques :** Génération automatique d'un code de référence unique (`UUID`) pour chaque transaction afin d'éviter les doublons.

### 3. 📊 Visualisation et Analyse (Data Viz)
* **Tableau de Bord Dynamique :** Affichage en temps réel du solde total du compte.
* **Graphique Circulaire (Matplotlib) :** Génération automatique d'un graphique montrant la répartition des dépenses par catégorie pour aider l'utilisateur à comprendre où va son argent.
* **Historique des Transactions :** Tableau (`Treeview`) listant les 15 dernières opérations avec un code couleur intelligent :
    * **Vert** pour les revenus (dépôts).
    * **Rouge** pour les dépenses (retraits).
    * **Bleu** pour les transferts.

### 4. 📥 Exportation et Portabilité
* **Export CSV Professionnel :** Bouton dédié permettant de générer un relevé bancaire complet au format `.csv`.
* **Compatibilité Excel :** Encodage spécifique (`utf-8-sig`) pour garantir que les symboles (€) et les accents s'affichent parfaitement dans Excel.

### 5. 🔔 Système de Notifications et Alertes
* **Alerte Découvert :** Notification automatique si le solde devient négatif.
* **Confirmations :** Messages de succès lors de l'exportation des données.
* **Gestion des Erreurs :** Alertes en cas de saisie de données invalides ou de champs vides.

### 6. 🎨 Expérience Utilisateur (UX/UI)
* **Design Moderne :** Interface épurée inspirée des tableaux de bord actuels (couleurs bleu nuit, turquoise et blanc cassé).
* **Interactivité (Hover) :** Effets visuels au survol de la souris sur tous les boutons pour une sensation de fluidité.
* **Fermeture Propre :** Code optimisé pour éviter les messages d'erreur dans le terminal lors de la fermeture de l'application.
