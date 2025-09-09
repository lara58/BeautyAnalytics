import os
import pandas as pd
from datetime import datetime

RAW_DIR = "data/raw"
META_DIR = "data/metadata"

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

file_reviews = "sephora_reviews.csv"
file_products = "sephora_products.csv"

print("Chargement des données...")
df_reviews = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", file_reviews))
df_products = pd.read_csv(os.path.join(os.path.dirname(__file__), "..", "data", file_products))
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

import json
with open(os.path.join(META_DIR, "metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)

print("Ingestion terminée!")
