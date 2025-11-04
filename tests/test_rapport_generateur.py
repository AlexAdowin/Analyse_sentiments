"""
Tests unitaires pour le module de génération de rapports.
"""

import pytest
import pandas as pd
import json
from pathlib import Path
from src.rapport_generateur import Generateur_rapport


class TestGenerateur_rapport:
    """Classe de tests pour la classe Generateur_rapport."""

    def setup_method(self):
        """
        Méthode exécutée avant chaque test.
        Initialise un objet Generateur_rapport avec des fichiers de test.
        """
        self.generator = Generateur_rapport(
            output_csv="output/test_results.csv",
            output_summary="output/test_summary.json"
        )

    def test_calculer_statistiques(self):
        """
        Test du calcul des statistiques à partir d'un DataFrame simulé.
        Vérifie que le total et la répartition des sentiments sont corrects.
        """

        # Créer un DataFrame de test
        df = pd.DataFrame({
            "review_text": ["Great!", "Bad!", "Okay"],  # Textes d'exemple
            "sentiment_final": ["Positif", "Négatif", "Neutre"],  # Sentiments attendus
            "polarity_score": [0.8, -0.7, 0.0]  # Scores de polarité simulés
        })

        # Calculer les statistiques avec la méthode du générateur
        stats = self.generator.calculer_statistiques(df)

        # Vérification du total d'avis analysés
        assert stats["total_avis_analyses"] == 3

        # Vérification du nombre d'avis par sentiment
        assert stats["statistiques"]["Positif"]["nombre"] == 1
        assert stats["statistiques"]["Négatif"]["nombre"] == 1
        assert stats["statistiques"]["Neutre"]["nombre"] == 1

        # Vérification des pourcentages (arrondis à 2 décimales)
        assert stats["statistiques"]["Positif"]["pourcentage"] == 33.33
        assert stats["statistiques"]["Négatif"]["pourcentage"] == 33.33
        assert stats["statistiques"]["Neutre"]["pourcentage"] == 33.33
