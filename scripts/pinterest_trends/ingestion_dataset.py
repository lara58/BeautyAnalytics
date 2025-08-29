import os
import pandas as pd
from datetime import datetime

RAW_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pinterest_trends", "raw")
META_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pinterest_trends", "metadata")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

file_reviews = "final_season_clean.csv"
file_products = "final_year.csv"

print("Chargement des données...")
df_reviews = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pinterest_trends", file_reviews))
df_products = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "pinterest_trends", file_products))

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
