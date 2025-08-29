import pandas as pd
import psycopg2
import os
from config import DB_CONFIG

csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                        'data', 'pinterest_trends', 'final_season_clean.csv')

print(f"Lecture du fichier: {csv_path}")

df = pd.read_csv(csv_path)

print("Aperçu des données:")
print(df.head())

create_table_sql = """
DROP TABLE IF EXISTS public.trends_season;

CREATE TABLE public.trends_season (
    "Rang" INT NULL,
    "Tendance" TEXT NULL,
    "Variation hebdomadaire" TEXT NULL,
    "Variation mensuelle" TEXT NULL,
    "Variation annuelle" TEXT NULL,
    "2024-08-13" TEXT NULL,
    "2024-08-20" TEXT NULL,
    "2024-08-27" TEXT NULL,
    "2024-09-03" TEXT NULL,
    "2024-09-10" TEXT NULL,
    "2024-09-17" TEXT NULL,
    "2024-09-24" TEXT NULL,
    "2024-10-01" TEXT NULL,
    "2024-10-08" TEXT NULL,
    "2024-10-15" TEXT NULL,
    "2024-10-22" TEXT NULL,
    "2024-10-29" TEXT NULL,
    "2024-11-05" TEXT NULL,
    "2024-11-12" TEXT NULL,
    "2024-11-19" TEXT NULL,
    "2024-11-26" TEXT NULL,
    "2024-12-03" TEXT NULL,
    "2024-12-10" TEXT NULL,
    "2024-12-17" TEXT NULL,
    "2024-12-24" TEXT NULL,
    "2024-12-31" TEXT NULL,
    "2025-01-07" TEXT NULL,
    "2025-01-14" TEXT NULL,
    "2025-01-21" TEXT NULL,
    "2025-01-28" TEXT NULL,
    "2025-02-04" TEXT NULL,
    "2025-02-11" TEXT NULL,
    "2025-02-18" TEXT NULL,
    "2025-02-25" TEXT NULL,
    "2025-03-04" TEXT NULL,
    "2025-03-11" TEXT NULL,
    "2025-03-18" TEXT NULL,
    "2025-03-25" TEXT NULL,
    "2025-04-01" TEXT NULL,
    "2025-04-08" TEXT NULL,
    "2025-04-15" TEXT NULL,
    "2025-04-22" TEXT NULL,
    "2025-04-29" TEXT NULL,
    "2025-05-06" TEXT NULL,
    "2025-05-13" TEXT NULL,
    "2025-05-20" TEXT NULL,
    "2025-05-27" TEXT NULL,
    "2025-06-03" TEXT NULL,
    "2025-06-10" TEXT NULL,
    "2025-06-17" TEXT NULL,
    "2025-06-24" TEXT NULL,
    "2025-07-01" TEXT NULL,
    "2025-07-08" TEXT NULL,
    "2025-07-15" TEXT NULL,
    "2025-07-22" TEXT NULL,
    "2025-07-29" TEXT NULL,
    "2025-08-05" TEXT NULL,
    "2025-08-12" TEXT NULL,
    "2025-08-13" TEXT NULL
);
"""

try:
    print("Connexion à PostgreSQL...")
    conn = psycopg2.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    conn.autocommit = True
    
    print("Création de la table trends_season...")
    with conn.cursor() as cursor:
        cursor.execute(create_table_sql)
        print("Table créée avec succès!")
    
    columns = df.columns.tolist()
    placeholders = ','.join(['%s'] * len(columns))
    
    insert_query = f"""
    INSERT INTO public.trends_season ({','.join([f'"{col}"' for col in columns])}) 
    VALUES ({placeholders})
    """
    
    print("Importation des données...")
    with conn.cursor() as cursor:
        for index, row in df.iterrows():
            values = [None if pd.isna(val) else val for val in row]
            cursor.execute(insert_query, values)
    
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM public.trends_season")
        row_count = cursor.fetchone()[0]
        print(f"Nombre de lignes importées: {row_count}")
    
    print("Importation terminée avec succès!")
    
except Exception as e:
    print(f"Erreur lors de l'importation: {e}")
finally:
    if 'conn' in locals():
        conn.close()
