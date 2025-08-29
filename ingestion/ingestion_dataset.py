import os
import pandas as pd
from datetime import datetime

# --- Configuration ---
RAW_DIR = "data/raw"
META_DIR = "data/metadata"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

# --- Fichiers sources ---
file_reviews = "sephora_reviews.csv"  # Exemple basé sur votre capture d'écran
file_products = "sephora_products.csv"  # Exemple basé sur votre capture d'écran

# --- 1. Chargement des datasets ---
print("Chargement des données...")
df_reviews = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", file_reviews))
df_products = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", file_products))

# --- 3. Séparation métadonnées ---
metadata = {
    "reviews": {
        "source": "Pinterest",
        "filename": file_reviews,
        "nb_rows": len(df_reviews),
        "ingestion_date": datetime.now().isoformat()
    },
    "products": {
        "source": "Pinterest",
        "filename": file_products,
        "nb_rows": len(df_products),
        "ingestion_date": datetime.now().isoformat()
    }
}

# --- 4. Sauvegarde des métadonnées ---
import json
with open(os.path.join(META_DIR, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)

print("Ingestion terminée!")
