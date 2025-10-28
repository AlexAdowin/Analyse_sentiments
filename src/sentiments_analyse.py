import logging
import pandas as pd
from typing import Literal # pour typer precisement les labels de sentiments
from textblob import TextBlob # pour calculer la polarite d'un texte



SentimentLabel = Literal["Positive", "Negative", "Neutral"]

class SentimentAnalyzer: 
    
    def __init__(self , positive_seuil : float = 0.1 , negative_seuil : float = -0.1): # initialise l'analyseur avec des seuils
        
        self.positive_seuil = positive_seuil
        self.negative_seuil = negative_seuil
        self.logger = logging.getLogger(__name__) # prépare le logger pour afficher des infos
        
        self.logger.info(f"Analyseur initialisé - Seuils : Positif >= {positive_seuil}," f"Négative <= {negative_seuil}") #affiche un message utile pour savoir que l’objet est bien initialisé avec les bons seuils

    def analyse_text(self , text : str ) -> tuple [str , float]: # Prend un texte en entrée et Retourne un tuple (label, polarité)
        
        if not text :
            
            return "Neutre" , 0.0
        
        try : 
            
            # calcule de la polarite avec TextBlob
            polarity = TextBlob(text).sentiment.polarity
            
            
            #classification selon le seuils
            
            if polarity >= self.positive_seuil :
                
                sentiment = "Positif"
                
            elif polarity <= self.negative_seuil :
                
                sentiment = "Negatif"
                
            else :
                
                sentiment = "Neutre"
                
            return sentiment , polarity # retourne le label et la polarité du texte
        
        except Exception as e :
            
            self.logger.error(f"Erreur lors de l'analyse du texte : {e}")
            return "Neutre" , 0.0 # en cas d'erreur, retourne neutre avec polarité 0.0
        
    def analyse_dataframe (self , df : pd.DataFrame , text_column : str = "review_text" ) -> pd.DataFrame :
         # -> pd.DataFrame: annotation de type de retour pour indiquer que la fonction retourne un DataFrame
  
        if text_column not in df.columns:
            raise ValueError(f"La colonne '{text_column}' n'existe pas dans le DataFrame")

        df_copy = df.copy()  # évite de modifier le DataFrame original
        
        results = df_copy[text_column].apply(self.analyse_text)  # applique l'analyse à chaque texte

        # lambda récupère les éléments du tuple
        
        
        df_copy["sentiment_final"] = results.apply(lambda x: x[0])  # extrait le label
        df_copy["polarite"] = results.apply(lambda x: x[1])   # extrait la polarite 
        
        self.logger.info(f"Analyse de sentiment terminée pour {len(df_copy)} entrées.") 
        
        return df_copy  # retourne le DataFrame annoté