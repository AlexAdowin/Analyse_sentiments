import pytest
import pandas as pd
from src.sentiments_analyse import SentimentAnalyzer


class TestSentimentAnalyse:
    """Classe de tests unitaires pour le SentimentAnalyzer amélioré."""

    def setup_method(self):
        """Crée un nouvel objet SentimentAnalyzer avant chaque test."""
        self.analyser = SentimentAnalyzer(positive_seuil=0.1, negative_seuil=-0.1)

    def test_positive_text(self):
        """Test d'un texte clairement positif."""
        text = "Excellent produit, je le recommande vivement à tout le monde !"
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Positif"
        assert polarity > 0.1

    def test_negative_text(self):
        """Test d'un texte clairement négatif."""
        text = "Le service client était absolument horrible. J'attends toujours une réponse."
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Negatif"
        assert polarity < -0.1

    def test_negative_text_with_delivery_issue(self):
        """Test d'un texte avec problème de livraison."""
        text = "Je n'ai pas reçu ma commande. Service client inexistant."
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Negatif"
        assert polarity < -0.1

    def test_neutre_text(self):
        """Test d'un texte neutre."""
        text = "Le produit est fourni dans les temps"
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Neutre"
        assert -0.1 <= polarity <= 0.1

    def test_empty_text(self):
        """Test d'un texte vide."""
        text = ""
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Neutre"
        assert polarity == 0.0

    def test_text_with_url(self):
        """Test d'un texte contenant une URL."""
        text = "Je n'ai pas reçu ma commande. Détails ici : http://site.com/track"
        sentiment, polarity = self.analyser.analyse_text(text)  # CORRECTION ICI

        # Devrait détecter négatif grâce à la gestion améliorée des problèmes de livraison
        assert sentiment == "Negatif"
        assert polarity < -0.1

    def test_text_with_uppercase_and_punctuation(self):
        """Test d'un texte avec majuscules et ponctuation."""
        text = "EXCELLENT PRODUIT!!! Très satisfait."
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Positif"
        assert polarity > 0.1

    def test_text_with_special_symbols_and_emoji(self):
        """Test d'un texte avec symboles spéciaux et emoji."""
        text = "Produit ⭐⭐⭐⭐⭐, je l'adore! 😍"
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Positif"
        assert polarity > 0.1

    def test_dataframe_analysis(self):
        """Test de l'analyse sur un DataFrame."""
        df = pd.DataFrame({
            'review_text': [
                "Excellent produit !",
                "Service horrible, je déconseille",
                "Produit correct pour le prix",
                ""
            ]
        })
        
        result_df = self.analyser.analyse_dataframe(df, 'review_text')
        
        assert 'sentiment_final' in result_df.columns
        assert 'polarite' in result_df.columns
        assert len(result_df) == 4

    def test_sentiment_stats(self):
        """Test des statistiques de sentiment."""
        df = pd.DataFrame({
            'sentiment_final': ["Positif", "Negatif", "Neutre"],
            'polarite': [0.8, -0.7, 0.0]
        })
        
        stats = self.analyser.get_sentiment_stats(df)
        
        assert stats["total"] == 3
        assert stats["positifs"] == 1
        assert stats["negatifs"] == 1
        assert stats["neutres"] == 1