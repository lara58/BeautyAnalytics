import pandas as pd
import io

def clean_pinterest_csv(input_path, output_path):
    """Nettoie un fichier CSV Pinterest et génère un nouveau fichier compatible avec pgAdmin"""
    print(f"Nettoyage du fichier: {input_path}")
    
    # Lire tout le contenu brut
    raw = open(input_path, "r", encoding="utf-8-sig", errors="ignore").read()
    lines = raw.splitlines()
    
    # Trouver la ligne d'en-tête
    header_idx = 0
    for i, line in enumerate(lines):
        if "Tendance" in line and "Variation" in line:
            header_idx = i
            break
    
    # Charger à partir de la vraie ligne d'entête
    df = pd.read_csv(io.StringIO("\n".join(lines[header_idx:])), encoding="utf-8-sig")
    
    # Nettoyer les colonnes
    df.rename(columns={
        "Rang": "rank",
        "Tendance": "keyword",
        "Variation annuelle": "var_year",
        "Variation mensuelle": "var_month",
        "Variation hebdomadaire": "var_week"
    }, inplace=True)
    
    # Supprimer les lignes vides
    df = df[df["keyword"].notna()]
    
    # Sauvegarder en CSV propre
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Fichier nettoyé créé: {output_path}")

def main():
    # Chemins des fichiers
    input_files = [
        "data_pinterest/Pinterest Trends report_2025-08-12.csv",
        "data_pinterest/Pinterest Trends report_2025-08-12 (2).csv"
    ]
    output_files = [
        "clean_pinterest_1.csv",
        "clean_pinterest_2.csv"
    ]
    
    for i, (input_file, output_file) in enumerate(zip(input_files, output_files)):
        clean_pinterest_csv(input_file, output_file)
    
    print("\nInstructions pour l'importation:")
    print("1. Dans pgAdmin, faites un clic droit sur votre table")
    print("2. Sélectionnez 'Import/Export'")
    print("3. Sélectionnez le fichier CSV nettoyé")
    print("4. Cochez 'Header' et définissez 'Delimiter' sur ','")
    print("5. Cliquez sur 'OK'")

if __name__ == "__main__":
    main()
