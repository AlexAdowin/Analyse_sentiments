import pytest
from src.sentiments_analyse import SentimentAnalyzer

class TestSentimentAnalyse:
    """Classe de tests unitaires pour le SentimentAnalyzer."""

    def setup_method(self):
        """Créé un nouvel objet SentimentAnalyzer avant chaque test pour éviter les interférences."""
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

    def test_neutre_text(self):
        """Test d'un texte neutre."""
        text = "Le produit est fourni dans les temps"
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Neutre"
        assert -0.1 < polarity < 0.1

    def test_empty_text(self):
        """Test d'un texte vide."""
        text = ""
        sentiment, polarity = self.analyser.analyse_text(text)

        assert sentiment == "Neutre"
        assert polarity == 0.0

    def test_text_with_url(self):
        """Test d'un texte contenant une URL."""
        text = "Je n'ai pas reçu ma commande. Détails ici : http://site.com/track"
        sentiment, polarity = self.analyser.analyse_text(text)  # CORRECTION : analyse_text au lieu de preprocess_text

        # Devrait détecter négatif malgré la présence de l'URL
        assert sentiment == "Negatif"
        assert polarity < -0.1

    def test_text_with_uppercase_and_punctuation(self):
        """Test d'un texte avec majuscules et ponctuation."""
        text = "EXCELLENT PRODUIT!!! Très satisfait."
        sentiment, polarity = self.analyser.analyse_text(text)

        # Devrait détecter positif malgré la ponctuation et majuscules
        assert sentiment == "Positif"
        assert polarity > 0.1

    def test_text_with_special_symbols_and_emoji(self):
        """Test d'un texte avec symboles spéciaux et emoji."""
        text = "Produit ⭐⭐⭐⭐⭐, je l'adore! 😍"
        sentiment, polarity = self.analyser.analyse_text(text)

        # Devrait détecter positif malgré les symboles et emoji
        assert sentiment == "Positif"
        assert polarity > 0.1