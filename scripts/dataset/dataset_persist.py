import os
import pandas as pd
import unicodedata
import psycopg2
from datetime import datetime

print("Nettoyage des données...")

# === Fonction pour enlever les accents ===
def remplacer_accents_fichier_safe(fichier_path):
    """
    Remplace les caractères accentués par leur équivalent sans accent dans un fichier CSV,
    sans altérer la structure du fichier.
    """
    temp_file = fichier_path + ".tmp"
    
    with open(fichier_path, 'r', encoding='latin-1', errors='ignore') as f_in, \
         open(temp_file, 'w', encoding='utf-8') as f_out:
        for ligne in f_in:
            ligne_sans_accents = unicodedata.normalize('NFKD', ligne)\
                .encode('ASCII', 'ignore').decode('ASCII')
            f_out.write(ligne_sans_accents)
    
    os.replace(temp_file, fichier_path)
    print(f"Remplacement effectué dans {fichier_path}")

# === Fichiers CSV à traiter ===
files = [
    r"D:\IPSSI\Cours\Datalake\TD_Spark\TP_Groupe\BeautyAnalytics\data\dataset\raw\reviews_raw.csv",
    r"D:\IPSSI\Cours\Datalake\TD_Spark\TP_Groupe\BeautyAnalytics\data\dataset\raw\products_raw.csv"
]

# === Suppression des accents ===
for file_path in files:
    remplacer_accents_fichier_safe(file_path)

# === Chargement des datasets ===
try:
    reviews_df = pd.read_csv(files[0], encoding='utf-8')
    products_df = pd.read_csv(files[1], encoding='utf-8')
except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")
    exit(1)

products_df = products_df.rename(columns={
    "brand": "brand_name",
    "category": "category_name",
    "name": "product_name",
    "price": "price",
    "rating": "rating",
    "love": "love"
})


# === Connexion PostgreSQL avec psycopg2 ===
conn = psycopg2.connect(
    dbname="beautyanalytics",
    user="postgres",
    password="postgres",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

print("Insertion des données...")

# === Insérer les brands uniques ===
brands = products_df["brand_name"].dropna().unique().tolist()
insert_brands_query = "INSERT INTO brands (brand_name) VALUES (%s) ON CONFLICT DO NOTHING;"

try:
    cursor.executemany(insert_brands_query, [(b,) for b in brands])
    conn.commit()
    print("Insertion des marques terminée.")
except Exception as e:
    conn.rollback()
    print(f"Erreur lors de l'insertion des marques : {e}")

# === Insérer les categories uniques ===
categories = products_df["category_name"].dropna().unique().tolist()
insert_categories_query = "INSERT INTO category (category_name) VALUES (%s) ON CONFLICT DO NOTHING;"

try:
    cursor.executemany(insert_categories_query, [(c,) for c in categories])
    conn.commit()
    print("Insertion des catégories terminée.")
except Exception as e:
    conn.rollback()
    print(f"Erreur lors de l'insertion des catégories : {e}")


# === Récupérer brands et categories avec leurs IDs ===

brands_db = pd.read_sql("SELECT * FROM brands", conn)
categories_db = pd.read_sql("SELECT * FROM category", conn)

# --- Joindre products avec brands et categories pour avoir leurs IDs ---
brands_db_unique = brands_db.drop_duplicates(subset=["brand_name"])
categories_db_unique = categories_db.drop_duplicates(subset=["category_name"])

products_df = products_df.merge(brands_db_unique, on="brand_name", how="left")
products_df = products_df.merge(categories_db_unique, on="category_name", how="left")

products_df_final = products_df[["product_name", "brand_id", "category_id", "price", "rating", "love"]]

# --- Insertion dans la table products ---
insert_products_query = """
    INSERT INTO products (product_name, brand_id, category_id, price, rating, love)
    VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
"""
try:
    cursor.executemany(
        insert_products_query,
        [tuple(x) for x in products_df_final.to_numpy()]
    )
    conn.commit()
    print("Insertion des produits terminée.")
except Exception as e:
    conn.rollback()
    print(f"Erreur lors de l'insertion des produits : {e}")

# === Récupérer products avec leurs IDs pour les reviews ===
products_db = pd.read_sql("SELECT * FROM products", conn)

# --- Joindre reviews avec products et brands pour avoir les IDs ---

# Nettoyage des valeurs brand_name pour garantir la jointure
reviews_df["brand_name"] = reviews_df["brand_name"].astype(str).str.strip().str.lower()
brands_db_unique["brand_name"] = brands_db_unique["brand_name"].astype(str).str.strip().str.lower()

reviews_df = reviews_df.merge(products_db, on="product_name", how="left")
reviews_df = reviews_df.merge(brands_db_unique, on="brand_name", how="left")

# Correction : choisir la bonne colonne brand_id
if "brand_id_x" in reviews_df.columns:
    reviews_df["brand_id"] = reviews_df["brand_id_x"]
elif "brand_id_y" in reviews_df.columns:
    reviews_df["brand_id"] = reviews_df["brand_id_y"]

# Vérification et sélection des colonnes pour reviews_df_final
expected_cols = ["product_id", "brand_id", "submission_time",
    "total_neg_feedback_count", "total_pos_feedback_count",
    "price_usd", "is_recommended"]
missing_cols = [col for col in expected_cols if col not in reviews_df.columns]
if missing_cols:
    print(f"Colonnes manquantes dans reviews_df : {missing_cols}")
    # Optionnel : raise ou exit
reviews_df_final = reviews_df[[col for col in expected_cols if col in reviews_df.columns]]

# --- Insertion dans la table reviews ---
insert_reviews_query = """
    INSERT INTO reviews (
        product_id, brand_id, review_date,
        total_neg_feedback_count, total_pos_feedback_count,
        price_usd, is_recommended
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
"""
try:
    cursor.executemany(
        insert_reviews_query,
        [tuple(x) for x in reviews_df_final.to_numpy()]
    )
    conn.commit()
    print("Insertion des reviews terminée.")
except Exception as e:
    conn.rollback()
    print(f"Erreur lors de l'insertion des reviews : {e}")

# === Insertion des métadonnées ===
metadata = pd.DataFrame([
    {
        "dataset_name": "Sephora Products",
        "filename": "sephora_products.csv",
        "source": "Kaggle",
        "nb_rows": len(products_df),
        "ingestion_date": datetime.now()
    },
    {
        "dataset_name": "Sephora Reviews",
        "filename": "sephora_reviews.csv",
        "source": "Gigasheet",
        "nb_rows": len(reviews_df),
        "ingestion_date": datetime.now()
    }
])

insert_metadata_query = """
    INSERT INTO metadata (dataset_name, filename, source, nb_rows, ingestion_date)
    VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
"""
try:
    cursor.executemany(
        insert_metadata_query,
        [tuple(x) for x in metadata.to_numpy()]
    )
    conn.commit()
    print("Insertion des métadonnées terminée.")
except Exception as e:
    conn.rollback()
    print(f"Erreur lors de l'insertion des métadonnées : {e}")

# === Fermeture de la connexion ===
cursor.close()
conn.close()

print("Données insérées avec succès !")