import pandas as pd
from pytrends.request import TrendReq
import os
import time
import random
from datetime import datetime

# Configuration complète des pays et mots-clés (traduits)
COUNTRIES = {
    "FR": {
        "name": "France",
        "keywords": [
            "crème hydratante", "fond de teint", "mascara waterproof",
            "sérum vitamine C", "rouge à lèvres mat", "soin anti-âge",
            "démaquillant", "bb crème", "palette fards à paupières", "vernis à ongles"
        ]
    },
    "US": {
        "name": "United States",
        "keywords": [
            "moisturizing cream", "foundation", "waterproof mascara",
            "vitamin C serum", "matte lipstick", "anti-aging cream",
            "makeup remover", "bb cream", "eyeshadow palette", "nail polish"
        ]
    },
    "DE": {
        "name": "Germany",
        "keywords": [
            "Feuchtigkeitscreme", "Foundation", "wasserfester Mascara",
            "Vitamin C Serum", "matte Lippenstift", "Anti-Aging-Creme",
            "Abschminkmittel", "BB-Creme", "Lidschatten-Palette", "Nagellack"
        ]
    },
    "GB": {
        "name": "United Kingdom",
        "keywords": [
            "moisturizing cream", "foundation", "waterproof mascara",
            "vitamin C serum", "matte lipstick", "anti-aging cream",
            "makeup remover", "bb cream", "eyeshadow palette", "nail polish"
        ]
    },
    "ES": {
        "name": "Spain",
        "keywords": [
            "crema hidratante", "base de maquillaje", "rimel resistente al agua",
            "suero de vitamina C", "pintalabios mate", "crema antiedad",
            "desmaquillante", "bb cream", "paleta de sombras", "esmalte de uñas"
        ]
    }
}

# Période complète (2021-2023)
START_DATE = "2021-01-01"
END_DATE = "2023-12-31"

def init_pytrends(max_retries=3):
    """Initialise PyTrends avec gestion des retries"""
    for attempt in range(max_retries):
        try:
            pytrends = TrendReq(
                hl='en-US',
                tz=360,
                timeout=(30, 60),
                retries=2,
                backoff_factor=1,
                requests_args={'verify': False}
            )
            return pytrends
        except Exception as e:
            print(f"⚠️ Tentative {attempt + 1}/{max_retries} échouée: {str(e)}")
            time.sleep(5)
    return None

def fetch_data(country_code, keyword):
    """Récupère les données pour un mot-clé et un pays"""
    pytrends = init_pytrends()
    if not pytrends:
        return None

    try:
        print(f"  🔍 Récupération des données pour '{keyword}'...")

        # Configuration de la requête
        pytrends.build_payload(
            kw_list=[keyword],
            timeframe=f"{START_DATE} {END_DATE}",
            geo=country_code
        )

        # Récupération des tendances temporelles
        data = pytrends.interest_over_time()
        if data.empty or keyword not in data.columns:
            print(f"  ⚠️ Aucune donnée trouvée pour '{keyword}'")
            return None

        # Récupération des topics associés (optionnel)
        try:
            related = pytrends.related_queries()
            if related and keyword in related:
                data[f"{keyword}_related"] = str(related[keyword])
        except Exception as e:
            print(f"  ⚠️ Impossible de récupérer les requêtes associées: {str(e)}")

        return data[[keyword]]  # Retourne uniquement la colonne du mot-clé

    except Exception as e:
        print(f"  ❌ Erreur pour '{keyword}': {str(e)}")
        return None

def save_data(country_code, keyword, data):
    """Sauvegarde les données dans un fichier CSV"""
    if data is None or data.empty:
        return False

    # Création du dossier si nécessaire
    os.makedirs(f"data/raw/{country_code}", exist_ok=True)

    # Nom de fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_keyword = "".join(c if c.isalnum() else "_" for c in keyword)
    filename = f"data/raw/{country_code}/{timestamp}_{safe_keyword}.csv"

    try:
        data.to_csv(filename, index=True)
        print(f"  ✅ Sauvegardé: {filename}")
        return True
    except Exception as e:
        print(f"  ❌ Échec de sauvegarde: {str(e)}")
        return False

def main():
    print("==================================================")
    print("🚀 Début de la récupération des données Google Trends")
    print(f"📅 Période: {START_DATE} → {END_DATE}")
    print(f"🌍 Pays: {', '.join(COUNTRIES.keys())}")
    print("==================================================\n")

    total_success = 0
    total_attempts = 0

    for country_code, config in COUNTRIES.items():
        print(f"🌍 {config['name']} ({country_code})")
        print(f"   Mots-clés: {len(config['keywords'])}")

        for keyword in config["keywords"]:
            total_attempts += 1
            print(f"\n   📌 '{keyword}'")

            # Récupération des données
            data = fetch_data(country_code, keyword)

            # Sauvegarde si données valides
            if data is not None:
                if save_data(country_code, keyword, data):
                    total_success += 1

            # Pause aléatoire pour éviter les blocages
            time.sleep(random.uniform(2, 8))

        print(f"\n   ➡️ {config['name']} terminé ({total_success}/{total_attempts} succès)\n")

    print("==================================================")
    print(f"🎉 Récupération terminée! {total_success}/{total_attempts} réussis")
    print("📂 Dossier de sortie: data/raw/")
    print("==================================================")

if __name__ == "__main__":
    main()
