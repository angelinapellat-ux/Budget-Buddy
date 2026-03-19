# Important 
Changer les identifiants de la base de donnée pour que le code fonctionne :
* ligne 12 et 51 pour user_account.py,
* ligne 6 pour seed_data.py,
* N'oublié pas d'installer les dépendances !
* Supprimer l'adresse enregistré dans le fichier json car elle n'existe pas dans votre base de donnée.
* Créer un compte et la connexion se fera sans soucis.

# 💰 Budget Buddy Pro - Assistant de Gestion Financière

**Budget Buddy Pro** est une application Desktop développée en Python (Tkinter) permettant de suivre ses finances personnelles de manière sécurisée et intuitive. L'application communique avec une base de données **MySQL** et offre des outils d'analyse visuelle.

## 🚀 Fonctionnalités Clés

### 1. Gestion des Utilisateurs & Sécurité
* **Authentification Sécurisée** : Système de Login/Inscription avec gestion des sessions.
* **Protection des Données** : Implémentation d'un hachage **SHA-256** combiné à un **Sel (Salt)** unique par utilisateur et un **Poivre (Pepper)** global.
* **Validation de Force** : Contrôle strict des mots de passe (10 caractères, Majuscules, Chiffres, Caractères spéciaux).
* **Session Persistante** : Option "Se souvenir de moi" (stockage sécurisé de l'identifiant uniquement).

### 2. Tableau de Bord (Dashboard)
* **Vue d'ensemble** : Affichage dynamique du solde en temps réel (calculé via SQL).
* **Gestion des Opérations** : Formulaire complet pour ajouter des **Dépôts**, **Retraits** ou **Transferts**.
* **Historique Intelligent** : Liste détaillée des transactions avec code couleur par type (Vert pour les gains, Rouge pour les dépenses).

### 3. Analyse & Data Visualization
* **Graphique Circulaire (Pie Chart)** : Visualisation de la répartition des dépenses par catégorie (Loisir, Repas, Factures, etc.) via **Matplotlib**.
* **Système de Filtres Avancé** : 
    * Filtrage par type de transaction.
    * Filtrage par catégorie.
    * Recherche par plage de dates.
    * Tri par montant (croissant/décroissant) ou par date.

### 4. Portabilité des Données
* **Export CSV** : Possibilité d'exporter l'historique filtré au format Excel/CSV pour un traitement externe.

---

## 🛠️ Architecture Technique

L'application repose sur une architecture **modulaire** pour séparer les responsabilités :

| Fichier | Rôle |
| :--- | :--- |
| `main.py` | Point d'entrée, gestion du Login et du routage. |
| `dashboard.py` | Interface principale et logique des filtres. |
| `user_account.py` | Moteur SQL (Requêtes CRUD, calculs de solde). |
| `security.py` | Gestionnaire de hachage et vérification cryptographique. |
| `budget_chart.py` | Module de rendu graphique Matplotlib. |
| `action.py` | Script de tests unitaires automatisés. |
| `seed_data.py` | Script de générations de contenu pour la table transaction. |



---

## 📦 Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/ton-pseudo/budget-buddy.git
   ```
2. **Installer les dépendances** :
   ```bash
   pip install mysql-connector-python matplotlib
   ```
3. **Configurer la base de données** :
   * Importer le fichier `database.sql` dans votre serveur MySQL (WAMP/XAMPP).
   * Vérifier les identifiants dans `user_account.py`.

4. **Lancer l'application** :
   ```bash
   python main.py
   ```

---

## 🧪 Tests
Pour vérifier l'intégrité du système (Calculs, Sécurité, SQL), lancez le script de test :
```bash
python action.py
```

---
