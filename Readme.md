# Beauty Trends & Insights – SEO & Data pour une Marque de Cosmétiques


*Vendez le bon produit au bon moment.*

---

## Sommaire

* [Description du projet](#description-du-projet)
* [Objectifs](#objectifs)
* [Problématiques clés](#problématiques-clés)
* [Stratégie proposée](#stratégie-proposée)
* [Données exploitées](#données-exploitées)
* [Sources de données](#sources-de-données)
* [Résultats attendus](#résultats-attendus)
* [Architecture du projet](#architecture-du-projet)
* [Analyses prévues](#analyses-prévues)
* [Technologies utilisées](#technologies-utilisées)
* [Auteurs](#auteurs)

---

## Description du projet

Ce projet a pour objectif d'améliorer le **référencement naturel (SEO)** et la **visibilité digitale** d'une marque de cosmétiques grâce à l'analyse de données et l'étude des tendances émergentes.
Il vise à optimiser les ventes en ligne en exploitant les comportements des consommateurs, les pics de recherche et la veille concurrentielle.

---

## Objectifs

* Améliorer la visibilité SEO des produits cosmétiques
* Anticiper les pics de saisonnalité et les tendances émergentes
* Identifier les produits à promouvoir selon les périodes clés et les zones géographiques
* Proposer des recommandations marketing et un reporting visuel via un **dashboard Power BI**

---

## Problématiques clés

* Comment maximiser la visibilité des produits cosmétiques sur internet ?
* Quels segments de marché cibler selon la saisonnalité et les tendances ?
* Quels produits mettre en avant selon les cycles de consommation ?
* Comment se différencier des concurrents (Amazon, Sephora, AromaZone) ?

---

## Stratégie proposée

* Publier du **contenu tendance** basé sur Google Trends
* Optimiser le contenu existant avec des **mots-clés SEO** pertinents
* Planifier un **calendrier éditorial saisonnier** (ex. : solaires en été, hydratants en hiver)
* Adapter le contenu selon la zone géographique (France, Europe, Monde)
* Promouvoir le **bon produit au bon moment** (ex. : parfums pour la fête des mères)
* Analyser le marché concurrentiel (Amazon, Sephora, AromaZone)
* Optimiser la présence sur **YouTube** pour accroître la visibilité

---

## Données exploitées

* **Google Trends** : popularité des mots-clés cosmétiques
* **Pinterest Trends** : détection des tendances beauté émergentes
* **Kaggle** : datasets cosmétiques (produits les plus vendus : Amazon, Sephora)

---

## Sources de données

| Source                                                                                            | Description                          | Format     |
| ------------------------------------------------------------------------------------------------- | ------------------------------------ | ---------- |
| [Google Trends API](https://trends.google.com/)                                                   | Popularité des mots-clés cosmétiques | CSV / JSON |
| [Pinterest Trends API](https://trends.pinterest.com/)                                             | Tendances beauté émergentes          | CSV        |
| [Kaggle Cosmetics Dataset](https://www.kaggle.com/datasets/devi5723/e-commerce-cosmetics-dataset) | Produits Amazon & Sephora            | CSV        |
| [Gigasheet Reviews Dataset](https://www.gigasheet.com/sample-data/sephora-cosmetic-reviews)       | Avis consommateurs Sephora           | CSV        |


---

## Résultats attendus

* **Augmentation du trafic organique** grâce à un meilleur positionnement SEO
* **Amélioration des ventes** par la mise en avant de produits tendance
* **Réduction du time-to-market** pour les campagnes marketing
* **Vision concurrentielle claire** pour ajuster prix et stratégies

---

## Architecture du projet

### 1. Couche d’ingestion

* **Objectif** : collecter les données brutes
* **Outils** :  API Google Trends & Pinterest, datasets Kaggle

### 2. Couche de persistance (Data Lake)

* **Objectif** : stocker et structurer les données
* **Structure** :

  * **Raw Zone** : données brutes (CSV, JSON)
  * **Processed Zone** : données nettoyées et enrichies
  * **Curated Zone** : datasets optimisés pour l’analyse SEO
* **Technologies** :  Data Lake

### 3. Couche Insight / Analyse

* **Objectif** : transformer les données en insights exploitables
* **Analyses** : tendances saisonnières, produits phares, analyse concurrentielle, recommandations SEO
* **Outils** : Spark / PySpark, Power BI, Jupyter Notebook

---

## Analyses prévues

* **Top 10 des tendances cosmétiques** (2025 & 2026)
* **Tendances émergentes à surveiller** en 2025
* Analyse des attentes et enjeux des **consommateurs beauté**

---

## Technologies utilisées
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![Power BI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=Power%20BI&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![pgAdmin](https://img.shields.io/badge/pgAdmin-336791?style=for-the-badge&logo=postgresql&logoColor=white)

* **Python** : pandas, numpy, pytrends, matplotlib
* **Big Data** : DataLake
* **SEO & Tendances** : Google Trends API, Pinterest Trends
* **Dashboarding** : Power BI
* **Exploration** : Jupyter Notebooks

---

## Auteurs

* **Mouna KHOLASSI**
* **Narimane TAHIR**
* **Lidia KHELIFI**

---

© 2025 Beauty Analytics Team – Tous droits réservés

---
