import sqlite3
import pandas as pd
from glob import glob
import os

# 1. Connexion à la base
DB_FILE = "trends.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# 2. Création des tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    keyword TEXT NOT NULL,
    ingestion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source TEXT,
    UNIQUE(country, keyword) ON CONFLICT IGNORE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS trends_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    value INTEGER NOT NULL,
    metadata_id INTEGER NOT NULL,
    FOREIGN KEY (metadata_id) REFERENCES metadata(id)
)
""")

# 3. Index
cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON trends_data(date)")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_metadata ON trends_data(metadata_id)")
conn.commit()

# 4. Fonction pour extraire le nom du produit depuis le chemin
def extract_keyword(file_path):
    parts = file_path.split('/')
    filename = parts[-1].replace('.csv', '')
    keyword = '_'.join(filename.split('_')[1:]).replace('_', ' ')
    return parts[-2], keyword  # (country, keyword)

# 5. Fonction pour charger un CSV
def load_csv_to_db(file_path):
    try:
        country, keyword = extract_keyword(file_path)

        # Vérifier les métadonnées
        cursor.execute(
            "SELECT id FROM metadata WHERE country = ? AND keyword = ?",
            (country, keyword)
        )
        metadata_id = cursor.fetchone()

        if not metadata_id:
            cursor.execute(
                "INSERT INTO metadata (country, keyword, source) VALUES (?, ?, ?)",
                (country, keyword, "Google Trends")
            )
            metadata_id = cursor.lastrowid
            conn.commit()
        else:
            metadata_id = metadata_id[0]

        # Charger le CSV
        df = pd.read_csv(file_path)

        # Trouver automatiquement la colonne de valeur (ex: "crème hydratante")
        value_column = [col for col in df.columns if col not in ['date', 'isPartial']][0]

        # Nettoyer les données
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['value'] = pd.to_numeric(df[value_column], errors='coerce').fillna(0).astype(int)

        # Insérer les données
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO trends_data (date, value, metadata_id) VALUES (?, ?, ?)",
                (row['date'], row['value'], metadata_id)
            )
        conn.commit()
        print(f"✅ {file_path} chargé ({df.shape[0]} lignes)")

    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {str(e)}")
        conn.rollback()

# 6. Charger tous les fichiers
csv_files = glob("data/raw/*/*.csv")
if not csv_files:
    print("⚠️ Aucun CSV trouvé dans data/raw/")
else:
    print(f"📂 {len(csv_files)} fichiers CSV trouvés. Chargement en cours...")
    for file in csv_files:
        load_csv_to_db(file)

# 7. Fermer la connexion
conn.close()
print("🎉 ETL terminé avec succès !")
