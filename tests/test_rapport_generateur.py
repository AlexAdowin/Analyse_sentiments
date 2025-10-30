"""
Tests unitaires pour le module de génération de rapports.
"""

import pytest
import pandas as pd
import json
from pathlib import Path
from src.rapport_generateur import Generateur_rapport


class TestGenerateur_rapport:
    """Tests pour la classe Generateur_rapport."""
    
    def setup_method(self):
        """Initialisation avant chaque test."""
        self.generator = Generateur_rapport(
            output_csv="output/test_results.csv",
            output_summary="output/test_summary.json"
        )
    
    def test_calculate_statistics(self):
        """Test du calcul des statistiques."""
        # Créer un DataFrame de test
        df = pd.DataFrame({
            "review_text": ["Great!", "Bad!", "Okay"],
            
            "sentiment_final": ["Positif", "Négatif", "Neutre"],
            
            "polarity_score": [0.8, -0.7, 0.0]
        })
        
        stats = self.generator.calculer_statistiques(df)
        
        assert stats["total_avis_analyses"] == 3
        assert stats["statistiques"]["Positif"]["nombre"] == 1
        assert stats["statistiques"]["Négatif"]["nombre"] == 1
        assert stats["statistiques"]["Neutre"]["nombre"] == 1
        assert stats["statistiques"]["Positif"]["pourcentage"] == 33.33
