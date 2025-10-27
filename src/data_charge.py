import logging      # pour enregistrer des messages (infos, erreurs, etc.)
import pandas as pd  # pour manipuler les tableaux de données
import json          # pour lire/écrire des données JSON
import re            # pour chercher des motifs dans du texte
from pathlib import Path   # pour gérer les chemins de fichiers
from typing import Optional  # pour indiquer qu'un argument peut être optionnel


class DataCharger:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)          # transforme le chemin en objet Path
        self.logger = logging.getLogger(__name__) # prépare le logger pour afficher des infos

    def load_data(self) -> pd.DataFrame:
        # Vérifie que le fichier existe
        if not self.file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {self.file_path}")
        
        # Si le fichier est un JS, on charge les données avec load_js
        if self.file_path.suffix == '.js':
            df = self.load_js()
        
        self.logger.info(f"Fichier chargé: {self.file_path}")  # log info
        self.validate_data(df)                                 # valide les données
        return df                                              # retourne le DataFrame

    def load_js(self) -> pd.DataFrame:
        """Charge un fichier JavaScript contenant reviews = [...]"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()  # lit tout le contenu du fichier
        
        # Cherche le tableau reviews dans le texte
        match = re.search(r'reviews\s*=\s*(\[[\s\S]*\])', content)
        if not match:
            raise ValueError("Tableau 'reviews' introuvable dans le fichier JS")
        
        # Transforme le texte JSON en liste Python puis en DataFrame
        data = json.loads(match.group(1))
        df = pd.DataFrame(data)
        
        self.logger.info(f"Fichier JS parsé avec succès: {len(data)} avis trouvés")  # log info
        return df  # retourne le DataFrame

    def validate_data(self, df: pd.DataFrame) -> None:
        # Vérifie que le DataFrame n'est pas vide
        if df.empty:
            raise ValueError("Le DataFrame est vide")
        
        # Log le nombre de lignes et colonnes
        self.logger.info(f"Données validées: {len(df)} lignes, {len(df.columns)} colonnes")
