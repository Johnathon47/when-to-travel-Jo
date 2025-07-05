# 🌟 Star Schema - When To Travel

Ce projet suit une architecture en étoile adaptée à l’analyse multidimensionnelle des données météo.

---

## 🧮 Table de faits : `fact_weather_score`

Contient les mesures météo quotidiennes par ville, enrichies d’un score météo synthétique.

| Champ       | Type     | Description                                                    |
|-------------|----------|----------------------------------------------------------------|
| id          | `int`    | Identifiant unique de la ligne                                 |
| id_city     | `string` | Clé étrangère vers `dim_city`                                  |
| id_date     | `int`    | Clé étrangère vers `dim_date`                                  |
| temperature | `float`  | Température moyenne du jour (°C)                               |
| description | `string` | Description météo du jour (ex : cloudy, sunny...)              |
| humidity    | `float`  | Taux d'humidité (%)                                             |
| wind        | `float`  | Vitesse du vent (km/h)                                          |
| pressure    | `float`  | Pression atmosphérique (hPa)                                    |
| score_meteo | `float`  | Score météo calculé (qualité globale du climat pour voyager)   |

---

## 🌍 Dimension : `dim_city`

| Champ   | Type     | Description                                   |
|---------|----------|-----------------------------------------------|
| id      | `string` | Identifiant unique de la ville                |
| name    | `string` | Nom de la ville                               |
| country | `string` | Nom du pays auquel appartient la ville        |

---

## 📅 Dimension : `dim_date`

| Champ    | Type     | Description                                     |
|----------|----------|-------------------------------------------------|
| id       | `int`    | Identifiant unique de la date (clé surrogate)   |
| fulldate | `date`   | Date complète (ex : 2023-07-05)                 |
| day      | `int`    | Jour du mois (1 à 31)                           |
| month    | `int`    | Mois (1 à 12)                                   |
| year     | `int`    | Année (ex : 2023)                               |
| season   | `string` | Saison climatique (ex : Winter, Summer, etc.)   |

---

> Ce modèle permet de faire des analyses temporelles (par mois, saison...), géographiques (par ville ou pays), ou encore d’agréger des scores météo pour identifier les **meilleures périodes pour voyager** dans une ville donnée.
