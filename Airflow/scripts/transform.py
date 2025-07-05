import os
import pandas as pd

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# === Étape 1 : Charger les données ===

def load_all_data():
    dataframes = []

    # Historique
    hist_dir = os.path.join(base_dir, "data", "historical", "cleaned")
    for root, dirs, files in os.walk(hist_dir):
        for file in files:
            if file.endswith(".csv"):
                path = os.path.join(root, file)
                df = pd.read_csv(path, parse_dates=["Date"])
                dataframes.append(df)

    # Récente
    recent_dir = os.path.join(base_dir, "data", "recent")
    for root, dirs, files in os.walk(recent_dir):
        for file in files:
            if file.endswith(".csv"):
                path = os.path.join(root, file)
                df = pd.read_csv(path, parse_dates=["Date"])
                dataframes.append(df)

    # Fusionner
    if dataframes:
        full_df = pd.concat(dataframes, ignore_index=True)
        return full_df
    else:
        raise Exception("❌ Aucune donnée trouvée dans les dossiers historical/cleaned et recent/")

# === Étape 2 : Transformer les données ===

def transformer(df: pd.DataFrame):
    df["Année"] = df["Date"].dt.year
    df["Mois"] = df["Date"].dt.month

    # Score météo (sur 100)
    def compute_score(row):
        score = 100
        if row["Température (°C)"] < 22 or row["Température (°C)"] > 28:
            score -= 20
        if row["Humidité (%)"] > 80:
            score -= 15
        if row["Vent (m/s)"] > 5:
            score -= 10
        if "rain" in row["Description"].lower() or "pluie" in row["Description"].lower():
            score -= 20
        return max(score, 0)

    df["Score Météo"] = df.apply(compute_score, axis=1)

    # Moyennes mensuelles par ville
    grouped = df.groupby(["Pays", "Ville", "Année", "Mois"]).agg({
        "Température (°C)": "mean",
        "Humidité (%)": "mean",
        "Vent (m/s)": "mean",
        "Pression (hPa)": "mean",
        "Score Météo": "mean"
    }).reset_index()

    return grouped

# === Étape 3 : Sauvegarder les résultats ===

def save_processed(df: pd.DataFrame):
    for (pays, ville), group in df.groupby(["Pays", "Ville"]):
        path = os.path.join(base_dir, "data", "processed", pays)
        os.makedirs(path, exist_ok=True)
        filename = os.path.join(path, f"{ville}.csv")
        group.to_csv(filename, index=False, encoding='utf-8-sig')

    print(f"\n✅ Données transformées sauvegardées dans : {os.path.join(base_dir, 'data', 'processed')}")
    print(f"📦 Total de fichiers : {df[['Pays','Ville']].drop_duplicates().shape[0]}")

# === MAIN ===

if __name__ == "__main__":
    print("🔄 Chargement des données...")
    df_all = load_all_data()

    print("🧠 Transformation des données...")
    df_transformed = transformer(df_all)

    print("💾 Sauvegarde...")
    save_processed(df_transformed)
