import logging
import os
import pycountry
import requests
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "/home/wesley/Documents/code/python/when-to-travel-Jo/"))
DATA_DIR = os.path.join(BASE_DIR, "data", "recent")

# Dictionnaire pour traduire certains noms de pays
english_to_french = {
    "France": "France",
    "Madagascar": "Madagascar",
    "Japan": "Japon",
    "Germany": "Allemagne",
    "United States": "États-Unis",
    "United Kingdom": "Royaume-Uni",
    "China": "Chine",
    "Italy": "Italie",
    "Spain": "Espagne"
}
# Ici c'est une fonction qui va Transformer les pays en format iso code en leur nom complete
def get_country_name(iso_code):
    try:
        country = pycountry.countries.get(alpha_2=iso_code)
        english_name = country.name if country else iso_code
        return english_to_french[english_name]
    except:
        return iso_code

# ici je vais prendre les info sur la ville plus précisemment sur son pays
def get_city_country_info(city: str, api_key: str) -> dict:
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(url, timeout=20)
    data = response.json()

    if not data:
        raise ValueError(f"Ville inconnue : {city}")

    info = {
        "city": data[0]["name"],
        "lat": data[0]["lat"],
        "lon": data[0]["lon"],
        "country": data[0]["country"]  # ex: "MG"
    }
    return info

# Prévisions météo sur les 5 jours
def extract_5day_forecast(city: str, api_key: str) -> bool:
    """
    Extraire les prévisions météo sur 5 jours via OpenWeather API.

    Args:
        city (str): Nom de la ville
        api_key (str): Clé API

    Returns:
        bool: True si l'extraction réussi, False sinon
    """
    try:
        info = get_city_country_info(city, api_key)
        country_code = info["country"]
        country_name = get_country_name(country_code)
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': city,
            'units': 'metric',
            'appid': api_key,
            'lang': 'fr'
        }
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()  # Exception si code HTTP ≠ 200

        data = response.json()
        weather_data = []

        for item in data["list"]:
            weather_data.append({
                "Pays": country_name,
                "Ville": city,
                "Date": datetime.fromtimestamp(item["dt"]),
                "Température (°C)": item["main"]["temp"],
                "Humidité (%)": item["main"]["humidity"],
                "Pression (hPa)": item["main"]["pressure"],
                "Vent (m/s)": item["wind"]["speed"],
                "Description": item["weather"][0]["description"],
                "Probabilité de pluie": item.get("pop", 0)  # parfois absent
            })

        # Création du dossier de destination
        country_path = os.path.join(DATA_DIR, country_name)
        os.makedirs(country_path, exist_ok=True)

        filename = f"{city}_{datetime.now().date()}.csv"
        file_path = os.path.join(country_path, filename)
        df = pd.DataFrame(weather_data)
        df.to_csv(file_path, index=False)
        return True

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erreur réseau/API pour {city} : {str(e)}")
    except KeyError as e:
        logging.error(f"Ville inconnue : {city} : {str(e)}")

    return False



