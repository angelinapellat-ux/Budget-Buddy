# 💰 Lancement
python main.py

Compte Test : 
email : un.deux@test.com
mot de passe : Azertyuiop@.1

# 💰 Budget Buddy Pro
**L'assistant intelligent pour la gestion de vos finances personnelles.**

Budget Buddy est une application de bureau développée en **Python** avec **Tkinter**, permettant de suivre ses revenus, ses dépenses et ses transferts bancaires en temps réel avec une interface moderne et intuitive (Design Argon/Material).
---
## ✨ Fonctionnalités Clés

* **🔒 Sécurité Renforcée** : 
    * Validation stricte des mots de passe (10 car. min, Maj, Min, Chiffre, Symbole).
    * Hachage des données sensibles en **SHA-256**.
* **📈 Dashboard Interactif** : 
    * Vue d'ensemble du solde en temps réel (Vert si positif, Rouge si négatif).
    * Graphique de répartition des dépenses par catégorie (Matplotlib).
    * Historique filtrable des 15 dernières transactions.
* **💸 Gestion Complète des Opérations** :
    * Support des **Dépôts**, **Retraits** et **Transferts**.
    * Système de catégories (Loisir, Repas, Factures, Salaire...).
* **💾 Persistance des Données** :
    * Base de données **MySQL** pour les utilisateurs et transactions.
    * Option "Se souvenir de moi" via stockage JSON local sécurisé.
      

## 🛠️ Stack Technique

* **Langage** : Python 3.x
* **Interface Graphique** : Tkinter (Customized UI)
* **Base de Données** : MySQL
* **Visualisation** : Matplotlib
* **Sécurité** : Hashlib, Re (Regex)

## 🚀 Installation & Configuration

### 1. Prérequis
Assurez-vous d'avoir installé :
* Python 3.10+
* Un serveur MySQL (XAMPP, WAMP ou MySQL Server)

### 2. Dépendances
Installez les bibliothèques nécessaires via pip :
pip install mysql-connector-python matplotlib
Installez les bibliothèques nécessaires via pip :
```bash
pip install mysql-connector-python matplotlib
