## 🖥️ Utilisation

Pour tester la logique du projet, lancez simplement le script principal :
python action.py
---

## 🚀 Fonctionnalités principales

* **Système de Sécurité Avancé** :
* Validation par expressions régulières (Regex) de la complexité des mots de passe (min. 10 caractères, majuscule, chiffre, caractère spécial).
* Hachage cryptographique **SHA-256** pour garantir qu'aucun mot de passe n'est traité en clair.


* **Modélisation Objet (POO)** :
* Séparation claire entre les entités `UserAccount` (Gestion du compte) et `Transaction` (Modèle de données).


* **Logique Financière** :
* Gestion des flux (Dépôts, Retraits, Transferts entre comptes).
* Calcul dynamique du solde et système d'alertes automatiques en cas de découvert.


* **Moteur de Recherche Multicritère** :
* Filtrage dynamique par dates, catégories, types de transactions et tri par montants.



## 🛠️ Architecture des Modules

Le code est organisé de manière modulaire pour favoriser la maintenabilité :

* **`user_account.py`** : Cœur de l'application. Gère l'authentification, la sécurité et la logique de calcul globale.
* **`transaction.py`** : Définit la structure de données d'une transaction financière.
* **`action.py`** : Script d'exécution simulant un flux complet (Inscription -> Sécurisation -> Opérations bancaires).

## 🔐 Concepts Clés implémentés

### 1. Sécurité "by Design"

L'inscription impose une vérification de la force du mot de passe avant toute instanciation. Le hachage est appliqué immédiatement pour protéger l'utilisateur.

### 2. Logique de Transfert

La méthode de transfert a été conçue pour être atomique : elle retire le montant d'un compte et l'ajoute instantanément au compte destinataire, garantissant l'intégrité des soldes.

### 3. Vue Globale & Statistiques

Une méthode dédiée permet d'extraire une synthèse des dépenses par mois et par catégorie, prête à être consommée par une interface graphique ou un moteur de reporting.


