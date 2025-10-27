from src.data_charge import DataCharger


# Indiquer le vrai chemin de ton fichier reviews.js
chemin = "../data/reviews.js"  # ou chemin absolu comme "C:/Users/Latitude 7320/Desktop/python/data/reviews.js"

# Créer le chargeur
charger = DataCharger(chemin)

# Charger les données dans un DataFrame
df = charger.load_data()

# Afficher les premières lignes
print(df.head())
