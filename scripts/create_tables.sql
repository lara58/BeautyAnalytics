-- Création de la table pour les tendances Pinterest
CREATE TABLE IF NOT EXISTS pinterest_trends (
    id SERIAL PRIMARY KEY,
    source_file TEXT,
    rank INTEGER,
    keyword TEXT,
    volume_normalise REAL,
    var_week REAL,
    var_month REAL,
    var_year REAL,
    date TEXT,
    value REAL
);

-- Création de la table pour les top 10
CREATE TABLE IF NOT EXISTS pinterest_top10 (
    id SERIAL PRIMARY KEY,
    keyword TEXT,
    volume_moyen REAL,
    source TEXT
);
