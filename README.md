# BeautyAnalytics - Analyse des tendances Pinterest

Ce projet permet d'importer et d'analyser les données de tendances beauté issues de Pinterest dans une base de données PostgreSQL.

## Structure du projet

### Organisation des dossiers
- `data/` : Données brutes et métadonnées
  - `data_pinterest/` : Fichiers CSV des tendances Pinterest
- `ingestion/` : Scripts d'importation des données
- `scripts/` : Scripts SQL et utilitaires

### Scripts d'ingestion
- `ingestion/ingestion_dataset.py` : Script principal d'importation des données
- `ingestion/import_season_data_simple.py` : Script pour importer les données saisonnières dans PostgreSQL
- `ingestion/import_season_data.py` : Version alternative du script d'importation
- `ingestion/clean_pinterest_csv.py` : Script pour nettoyer les données CSV avant importation

### Scripts SQL
- `scripts/create_tables.sql` : Script SQL de création des tables de base
- `scripts/setup_tables_complete.sql` : Script complet de création et configuration des tables
- `scripts/view_trends_season.sql` : Requêtes pour consulter les données de tendances saisonnières

### Fichiers de configuration
- `config.py` : Configuration de connexion à la base de données PostgreSQL

### Données
- `data/data_pinterest/` : Dossier contenant les fichiers CSV de données Pinterest
  - `final_season_clean.csv` : Données saisonnières nettoyées
  - `final_season.csv` : Données saisonnières brutes
  - `final_year.csv` : Données annuelles
- `data/Top10_Pinterest_Annuel.csv` : Top 10 des tendances annuelles
- `data/Top10_Pinterest_Comparatif.csv` : Comparaison des tendances
- `data/Top10_Pinterest_Saisonnier.csv` : Top 10 des tendances saisonnières

### Documentation
- `POSTGRES_SETUP_GUIDE.md` : Guide d'installation et configuration de PostgreSQL
- `beauty project.pdf` : Documentation du projet
- `JupyterCommandes.ipynb` : Notebook Jupyter avec des exemples de commandes

## Comment utiliser

### Configuration de la base de données
1. Suivez les instructions dans `POSTGRES_SETUP_GUIDE.md` pour installer PostgreSQL
2. Modifiez `config.py` avec vos informations de connexion

### Importation des données
1. Exécutez le script d'ingestion principal :
   ```
   python -m ingestion.ingestion_dataset
   ```
   
2. Pour importer les données saisonnières dans PostgreSQL :
   ```
   python -m ingestion.import_season_data_simple
   ```

### Consultation des données
1. Utilisez pgAdmin 4 pour exécuter les requêtes dans `scripts/view_trends_season.sql`
2. Ou créez vos propres requêtes pour analyser les tendances

## Notes importantes
- Les fichiers CSV français utilisent l'encodage Windows-1252 pour les caractères accentués
- La table `trends_season` contient plus de 50 colonnes (une pour chaque semaine)
