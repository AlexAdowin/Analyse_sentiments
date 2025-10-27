
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:

    
    # Fichiers d'entrée/sortie
    input_file: str = os.getenv("INPUT_FILE", "data/reviews.js")

    
    


    positive_seuil: float = float(os.getenv("POSITIVE_SEUIL", "0.1"))
    
    negative_seuil: float = float(os.getenv("NEGATIVE_SEUIL", "-0.1"))  
    
    #config donnees

    text_column: str = os.getenv("TEXT_COLUMN", "review_text")
    
    #config logging

    log_level: str = os.getenv("LOG_LEVEL", "INFO")  # Niveau de logging: DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    def __post_init__(self): # sert à valider que les seuils définis dans la configuration ont un sens juste après la création de l’objet.
        
        if self.positive_seuil <= self.negative_seuil:
            raise ValueError(f"Le seuil positif ({self.positive_seuil}) doit être supérieur au seuil négatif ({self.negative_seuil}).")