import pytest
import pandas as pd
from pathlib import Path
from src.data_charge import DataCharger


class TestDataCharger:
    """Tests pour la classe DataCharger."""

    def test_load_inexistant_file(self):
        """Test de chargement d'un fichier inexistant."""
        charger = DataCharger("nonexistent_file.csv")

        with pytest.raises(FileNotFoundError):
            charger.load_data()
    
    def test_validate_empty_dataframe(self):
        """Test de validation d'un DataFrame vide."""
        charger = DataCharger("data/reviews.js")
        empty_df = pd.DataFrame()
        
        with pytest.raises(ValueError, match="DataFrame est vide"):
            charger.validate_data(empty_df)
