import pytest 
from src.sentiments_analyse import SentimentAnalyzer


class TestSentimentAnalyse : #ceci s'execute a chaque test et cree un new object SentimenAnalyzer pour eviter que les test se pertubent entre eux
    
    def setup_method(self) :
        
        self.analyser = SentimentAnalyzer(positive_seuil = 0.1 , negative_seuil = -0.1)
        
    def test_positive_text(self) : 
        
        text = "Excellent produit, je le recommande vivement à tout le monde !"
        
        sentiment , polarity = self.analyser.analyse_text(text) #recuperation des valeurs retourner par analyse_text
        
        #assert sert averifier qu'une condition est vrai ou non
        
        assert sentiment =="Positif"
        assert polarity > 0.1 
        
    def test_negatif_text(self) : 
        
        text = "Le service client était absolument horrible. J'attends toujours une réponse."
        
        sentiment , polarity = self.analyser.analyse_text(text)
        
        assert sentiment == "Negatif"
        assert polarity < -0.1 
        
    def test_neutre_text(self) : 
        
        text = "Le produit est fournie dans les temps"
        
        sentiment , polarity = self.analyser.analyse_text(text)
        
        assert sentiment == "Neutre"
        assert polarity == 0.0
        
    def test_vide_text(self) : 
        
        text = ""
        
        sentiment , polarity = self.analyser.analyse_text(text)
        
        assert sentiment == "Neutre"
        assert polarity == 0.0
        
