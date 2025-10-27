
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:

    
    # Fichiers d'entrée/sortie
    input_file: str = os.getenv("INPUT_FILE", "data/reviews.js")
   