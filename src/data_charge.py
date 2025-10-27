import logging
import pandas as pd
import json
import re
from pathlib import Path
from typing import Optional


class DataCharger:

    
    def __init__(self, file_path: str):
     
        self.file_path = Path(file_path)
        self.logger = logging.getLogger(__name__)
    
    def load_data(self) -> pd.DataFrame:
    
        if not self.file_path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {self.file_path}")
        
        if self.file_path.suffix == '.js':
            df = self._load_js()
        
        self.logger.info(f"Fichier chargé: {self.file_path}")
        
        # Validation des données
        self._validate_data(df)
         
        return df
    
    def load_js(self) -> pd.DataFrame:
        """Charge un fichier JavaScript contenant reviews = [...]"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'reviews\s*=\s*(\[[\s\S]*\])', content)
        if not match:
            raise ValueError("Tableau 'reviews' introuvable dans le fichier JS")
        
        data = json.loads(match.group(1))
        df = pd.DataFrame(data)
        
        self.logger.info(f"Fichier JS parsé avec succès: {len(data)} avis trouvés")
        
        return df
    
    def validate_data(self, df: pd.DataFrame) -> None:
    
        if df.empty:
            raise ValueError("Le DataFrame est vide")
        
        self.logger.info(f"Données validées: {len(df)} lignes, {len(df.columns)} colonnes")
