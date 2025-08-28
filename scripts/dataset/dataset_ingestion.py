import os
import pandas as pd
from datetime import datetime

# --- Configuration ---
RAW_DIR = "data/raw"
META_DIR = "data/metadata"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# --- Fichiers sources ---
file_reviews = "sephora_reviews.csv"
file_products = "sephora_products.csv"

# --- 1. Chargement des datasets ---
print("Chargement des données...")
try :
    df_reviews = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "dataset", file_reviews))
    df_products = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "dataset", file_products))
except Exception as e:
    print(f"Erreur lors du chargement des données : {e}")
    exit(1)

# --- 3. Séparation métadonnées ---
metadata = {
    "reviews": {
        "source": "Gigasheet",
        "filename": file_reviews,
        "nb_rows": len(df_reviews),
        "ingestion_date": datetime.now().isoformat()
    },
    "products": {
        "source": "Kaggle",
        "filename": file_products,
        "nb_rows": len(df_products),
        "ingestion_date": datetime.now().isoformat()
    }
}

# --- 4. Sauvegarde Raw Zone ---
df_reviews.to_csv(os.path.join(RAW_DIR, "reviews_raw.csv"), index=False)
df_products.to_csv(os.path.join(RAW_DIR, "products_raw.csv"), index=False)

# Sauvegarde des métadonnées
pd.DataFrame(metadata).to_json(os.path.join(META_DIR, "ingestion_metadata.json"), indent=4)

print("Ingestion terminée")
