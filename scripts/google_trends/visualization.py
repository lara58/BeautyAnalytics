# visualization.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from glob import glob
import os
from datetime import datetime

# ======================
# 1. CHARGEMENT DES DONNÉES
# ======================
def load_all_data():
    """Charge tous les fichiers CSV dans un seul DataFrame"""
    all_files = glob("data/raw/*/*.csv")
    if not all_files:
        raise FileNotFoundError("Aucun fichier CSV trouvé dans data/raw/")

    dfs = []
    for file in all_files:
        try:
            # Extraction des métadonnées depuis le chemin
            parts = file.split('/')
            country = parts[2]
            filename = parts[3]
            keyword = '_'.join(filename.split('_')[1:]).split('.')[0].replace('_', ' ')

            # Chargement du fichier
            df = pd.read_csv(file, parse_dates=['date'])
            df['country'] = country
            df['keyword'] = keyword
            df['value'] = df.iloc[:, 1]  # La 2ème colonne contient les valeurs

            # Sélection des colonnes utiles
            dfs.append(df[['date', 'value', 'country', 'keyword']])

        except Exception as e:
            print(f"⚠️ Erreur avec {file}: {str(e)}")

    if not dfs:
        raise ValueError("Aucune donnée valide trouvée")

    return pd.concat(dfs, ignore_index=True)

# ======================
# 2. NETTOYAGE DES DONNÉES
# ======================
def clean_data(df):
    """Nettoie et prépare les données pour la visualisation"""
    # Renommage des pays
    country_map = {
        'FR': 'France 🇫🇷',
        'US': 'USA 🇺🇸',
        'DE': 'Allemagne 🇩🇪',
        'GB': 'Royaume-Uni 🇬🇧',
        'ES': 'Espagne 🇪🇸'
    }
    df['country'] = df['country'].map(country_map)

    # Conversion des dates en mois/année pour les tendances
    df['month'] = df['date'].dt.to_period('M').astype(str)
    df['year'] = df['date'].dt.year

    # Suppression des valeurs nulles
    return df.dropna()

# ======================
# 3. VISUALISATIONS
# ======================
def plot_trend_over_time(df, country=None, keyword=None):
    """Graphique des tendances dans le temps"""
    title = "Tendances Google Trends (2021-2023)"

    if country:
        df = df[df['country'] == country]
        title += f" - {country}"
    if keyword:
        df = df[df['keyword'] == keyword]
        title += f" - '{keyword}'"

    fig = px.line(
        df,
        x='date',
        y='value',
        color='keyword' if not keyword else 'country',
        title=title,
        labels={'value': 'Popularité (0-100)', 'date': 'Date'},
        line_shape='spline',
        render_mode='svg'
    )

    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Score de popularité",
        legend_title="Légende",
        height=600
    )
    return fig

def plot_country_comparison(df, keyword):
    """Comparaison entre pays pour un mot-clé"""
    df_keyword = df[df['keyword'] == keyword]

    fig = px.line(
        df_keyword,
        x='date',
        y='value',
        color='country',
        title=f"Comparaison par pays: '{keyword}'",
        labels={'value': 'Popularité', 'date': 'Date'},
        line_shape='spline'
    )

    fig.update_layout(
        hovermode="x unified",
        height=600
    )
    return fig

def plot_top_keywords(df, country, top_n=5):
    """Top mots-clés pour un pays"""
    # Agrégation par mot-clé (moyenne sur la période)
    df_agg = df[df['country'] == country].groupby('keyword')['value'].mean().reset_index()
    df_agg = df_agg.sort_values('value', ascending=False).head(top_n)

    fig = px.bar(
        df_agg,
        x='keyword',
        y='value',
        title=f"Top {top_n} mots-clés en {country}",
        labels={'value': 'Popularité moyenne', 'keyword': 'Produit'},
        color='value',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        xaxis_title="Produit",
        yaxis_title="Score moyen (0-100)",
        height=500
    )
    return fig

def plot_seasonality(df, keyword):
    """Analyse de la saisonnalité (par mois)"""
    df['month_num'] = df['date'].dt.month
    df_monthly = df[df['keyword'] == keyword].groupby(['month_num', 'country'])['value'].mean().reset_index()

    fig = px.line(
        df_monthly,
        x='month_num',
        y='value',
        color='country',
        title=f"Saisonnalité pour '{keyword}' (moyenne par mois)",
        labels={'month_num': 'Mois', 'value': 'Popularité'},
        markers=True
    )

    fig.update_xaxes(
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin',
                 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc']
    )

    return fig

# ======================
# 4. INTERFACE UTILISATEUR
# ======================
def main():
    print("🔍 Chargement des données...")
    try:
        df = load_all_data()
        df = clean_data(df)
        print(f"✅ {len(df)} lignes chargées ({df['country'].nunique()} pays, {df['keyword'].nunique()} mots-clés)")

        # Exemple 1: Tendances globales
        fig1 = plot_trend_over_time(df)
        fig1.show()

        # Exemple 2: Comparaison par pays pour "crème hydratante"
        fig2 = plot_country_comparison(df, "creme hydratante")
        fig2.show()

        # Exemple 3: Top 5 produits en France
        fig3 = plot_top_keywords(df, "France 🇫🇷")
        fig3.show()

        # Exemple 4: Saisonnalité du "mascara waterproof"
        fig4 = plot_seasonality(df, "mascara waterproof")
        fig4.show()

    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    main()
