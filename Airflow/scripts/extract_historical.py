import os

import pandas as pd

# Charder un aperçu du fichier CSV uploadé
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "/home/wesley/Documents/code/python/when-to-travel-Jo/"))
file_path = os.path.join(base_dir, "data", "historical","raw", "Global_weather_repository.csv")
df = pd.read_csv(file_path)

# Sélectionner uniquement les colonnes importantes
df = df[[
    "country",
    "location_name",
    "last_updated",
    "temperature_celsius",
    "humidity",
    "wind_kph",
    "pressure_mb",
    "condition_text"
]]

# Renommer les colonnes pour plus de clarté
df.columns = [
    "Pays",
    "Ville",
    "Date",
    "Température (°C)",
    "Humidité (%)",
    "Vent (km/h)",
    "Pression (hPa)",
    "Description"
]

# Convertir la date en datetime
df["Date"] = pd.to_datetime(df["Date"])

# Convertir le vent en m/s (1 km/h ≈ 0.27778 m/s)
df["Vent (m/s)"] = df["Vent (km/h)"] * 0.27778

# Supprimer l'ancienne colonne km/h
df.drop(columns="Vent (km/h)", inplace=True)

# Vérifie les doublons exacts sur toutes les colonnes
duplicates = df[df.duplicated()]
print("Doublons exacts : ", len(duplicates))

# Enlever les doublons exacts (ligne identique)
df_cleaned = df.drop_duplicates()

# Réinitialiser l'index
df_cleaned = df_cleaned.reset_index(drop=True)

for _, row in df_cleaned.iterrows():
    pays = row["Pays"]
    ville = row["Ville"]
    date = row["Date"]
    annee = date.year
    mois = date.month

    # Chemin du dossier
    dossier = f"../../data/historical/cleaned/{pays}/{annee}/"
    os.makedirs(dossier, exist_ok=True)

    # Chemin du fichier
    fichier = f"{dossier}{mois:02d}.csv"

    # Enregistrement ligne par ligne
    row_df = row.to_frame().T # Convertir la ligne Series en DataFrame
    if not os.path.exists(fichier):
        row_df.to_csv(fichier, index=False, mode='w', encoding='utf-8-sig')
    else:
        row_df.to_csv(fichier, index=False, mode='a', header=False, encoding='utf-8-sig')


# 🔚 ✅ À mettre juste ici, en dehors de la boucle
print(f"\n✅ Données nettoyées et sauvegardées avec succès dans :")
print(f"→ {os.path.join(base_dir, 'data', 'historical', 'cleaned')}")
print(f"📊 Total de lignes finales : {len(df_cleaned)}")