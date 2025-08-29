# Guide d'installation et configuration de PostgreSQL pour le projet BeautyAnalytics

## 1. Installation de PostgreSQL

1. Téléchargez PostgreSQL depuis le site officiel : https://www.postgresql.org/download/windows/
   - Choisissez la version la plus récente pour Windows

2. Exécutez l'installeur et suivez ces étapes :
   - Sélectionnez tous les composants (PostgreSQL Server, pgAdmin, Command Line tools)
   - Choisissez un répertoire d'installation (par défaut : `C:\Program Files\PostgreSQL\15`)
   - Définissez un mot de passe pour l'utilisateur `postgres` (par défaut dans notre script : `postgres`)
   - Conservez le port par défaut (5432)
   - Utilisez la locale par défaut

3. Terminez l'installation et décochez l'option de lancement de Stack Builder

## 2. Vérification de l'installation

1. Ouvrez pgAdmin depuis le menu Démarrer
   - Connectez-vous avec le mot de passe défini lors de l'installation
   - Vous devriez voir un serveur PostgreSQL dans le panneau de gauche

2. Vérifiez l'accès en ligne de commande :
   - Ouvrez une invite de commande ou PowerShell
   - Exécutez : `psql -U postgres -h localhost`
   - Entrez le mot de passe défini lors de l'installation
   - Vous devriez obtenir une invite `postgres=#`
   - Tapez `\q` pour quitter

## 3. Configuration du script Python

Si votre installation utilise des paramètres différents des valeurs par défaut, modifiez ces lignes dans le script `create_database.py` :

```python
# Configuration de la base de données PostgreSQL
DB_NAME = "beauty_analytics"  # Nom de la base de données à créer
DB_USER = "postgres"          # Nom d'utilisateur (par défaut: postgres)
DB_PASSWORD = "postgres"      # Mot de passe (à remplacer par celui défini lors de l'installation)
DB_HOST = "localhost"         # Adresse du serveur (localhost si installé sur la même machine)
DB_PORT = "5432"              # Port PostgreSQL (par défaut: 5432)
```

## 4. Exécution du script

Une fois PostgreSQL configuré, exécutez le script Python :

```
python create_database.py
```

Cela créera la base de données `beauty_analytics` et importera les données du dossier `data_pinterest`.

## 5. Connexion à la base de données

Pour visualiser ou manipuler les données après l'importation :

1. Ouvrez pgAdmin
2. Dans l'arborescence à gauche, développez : Servers > PostgreSQL > Databases
3. Cliquez sur la base de données `beauty_analytics`
4. Dans le menu contextuel, choisissez "Query Tool"
5. Exécutez des requêtes SQL, par exemple :
   ```sql
   -- Voir toutes les tendances par popularité
   SELECT keyword, AVG(value) as popularité
   FROM pinterest_trends
   GROUP BY keyword
   ORDER BY popularité DESC
   LIMIT 10;
   
   -- Voir les données du top 10
   SELECT * FROM pinterest_top10;
   ```
