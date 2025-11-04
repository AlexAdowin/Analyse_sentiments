import logging  
import pandas as pd 
from typing import Literal  # pour typer précisément les labels de sentiment
from textblob import TextBlob  # pour calculer la polarité du texte
import re  # pour gérer les expressions régulières et nettoyer le texte


# Permet de préciser que le label retourné sera soit "Positif", "Negatif" ou "Neutre"
SentimentLabel = Literal["Positif", "Negatif", "Neutre"]

# --- Dictionnaire des mots-clés positifs ---
POSITIVE_WORDS = {
    
  
    'excellent', 'génial', 'merveilleux', 'fantastique', 'incroyable',
  
    'adore', 'aime', 'superbe', 'parfait', 'magnifique', 'ravissant',
  
    'très bien', 'très bon', 'très facile', 'très rapide', 'très satisfait',
  
    'satisfait', 'content', 'heureux', 'ravi', 'comblé', 'enchanté',
  
    'recommande', 'meilleur', 'top', 'idéal', 'simple', 'efficace',
  
    'bonne affaire', 'bon prix', 'qualité', 'belle', 'élégant', 'moderne',
  
    'facile', 'rapide', 'fiable', 'solide', 'durable', 'pratique',
  
    'cinq étoiles', '⭐', 'reviendrais', 'reachèterais', 'réserver',
  
    'fonction parfaitement', 'fonctionne bien', 'fonctionne comme prévu', 'convient parfaitement',
  
    'merci', 'agréable', 'plaisir', 'divertissant', 'utile', 'efficacement'
}


# --- Dictionnaire des mots-clés négatifs ---
NEGATIVE_WORDS = {

    'horrible', 'nul', 'pourri', 'mauvais', 'pire', 'inutilisable',

    'cassé', 'défaillant', 'décevant', 'dommage', 'décep', 'frustrant',

    'problème', 'bug', 'erreur', 'panne', 'dysfonction', 'défaut',

    'trop cher', 'cher', 'chère', 'onéreux', 'ruineux',

    'n\'a jamais', 'n\'ai jamais', 'pas reçu', 'n\'ai reçu que',

    'moitié', 'endommagé', 'abîmé', 'déchiré', 'mal traduit',

    'incompréhensible', 'confus', 'confuses', 'trop lourd',

    'retard', 'retardé', 'en retard', 'ne correspond pas',

    'n\'aurais pas', 'préféré', 'hésité', 'hésiter', 'ne suis pas sûr',

    'qualité n\'est pas', 'n\'est pas au rendez-vous', 'mediocre',

    'impossible', 'difficultés', 'scandaleux', 'mauvais service' , 'plaisir' ,
    
    'meilleur'
}

# Permet de détecter si le texte contient des mots qui amplifient le sentiment

INTENSIFIERS = {'très', 'extrêmement', 'absolument', 'tellement', 'ultra', 'super', 'vraiment'}

NEGATIONS = {'n\'', 'pas', 'jamais', 'non', 'aucun', 'aucune'}

class SentimentAnalyzer:
    """Classe pour analyser le sentiment d'un texte ou d'un DataFrame."""

    def __init__(self, positive_seuil: float = 0.1, negative_seuil: float = -0.1):
        """
        Initialise l'analyseur avec des seuils pour déterminer le sentiment.
        positive_seuil : score minimum pour considérer un texte comme positif
        negative_seuil : score maximum pour considérer un texte comme négatif
        """
        self.positive_seuil = positive_seuil
        self.negative_seuil = negative_seuil

        # Création du logger pour enregistrer les messages
        self.logger = logging.getLogger(__name__)
        
        # Message d'information indiquant que l'analyseur est initialisé
        self.logger.info(
            f"Analyseur initialisé - Seuils : Positif >= {positive_seuil}, Négatif <= {negative_seuil}"
        )

    def preprocess_text(self, text: str) -> str:
       
        if not text:
            return ""

        # Mettre en minuscule
        text = text.lower()

        # Supprimer les URL
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)

        # Supprimer ponctuation et symboles spéciaux (sauf emojis)
        text = re.sub(r'[^\w\s⭐]', '', text)

        # Supprimer espaces multiples
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def analyse_text(self, text: str) -> tuple[SentimentLabel, float]:
        """
        Analyse un texte et retourne :
        - le sentiment : Positif, Negatif, Neutre
        - la polarité : score numérique entre -1 et 1
        """
        if not text or pd.isna(text):
            return "Neutre", 0.0

        try:
            # Nettoyage et normalisation du texte
            text_clean = self.preprocess_text(text)

            # Compter les mots-clés positifs et négatifs
            pos_count = sum(word in text_clean for word in POSITIVE_WORDS)
            neg_count = sum(word in text_clean for word in NEGATIVE_WORDS)

            # Détecter présence d'intensifieurs
            has_intensifier = any(word in text_clean for word in INTENSIFIERS)

            # Score de polarité de base avec TextBlob
            polarity = TextBlob(text_clean).sentiment.polarity

            # Ajuster score si intensifieur détecté
            if has_intensifier:
                if pos_count > 0:
                    polarity += 0.2  # intensifie le positif
                elif neg_count > 0:
                    polarity -= 0.2  # intensifie le négatif

            # Score mots-clés normalisé
            keyword_score = (pos_count - neg_count) * 0.15

            # Combinaison finale : TextBlob + mots-clés
            final_score = 0.5 * polarity + 0.5 * keyword_score

            # Déterminer le sentiment selon seuils
            if final_score >= self.positive_seuil:
                sentiment = "Positif"
            elif final_score <= self.negative_seuil:
                sentiment = "Negatif"
            else:
                sentiment = "Neutre"

            return sentiment, round(final_score, 2)

        except Exception as e:
            # En cas d'erreur, retourner neutre et log l'erreur
            self.logger.error(f"Erreur lors de l'analyse du texte : {e}")
            return "Neutre", 0.0

    def analyse_dataframe(self, df: pd.DataFrame, text_column: str = "review_text") -> pd.DataFrame:
        """
        Analyse une colonne d'un DataFrame et ajoute :
        - sentiment_final : le label du sentiment
        - polarite : la polarité numérique
        """
        if text_column not in df.columns:
            raise ValueError(f"La colonne '{text_column}' n'existe pas dans le DataFrame")

        # Crée une copie pour ne pas modifier le DataFrame original
        df_copy = df.copy()

        # Appliquer l'analyse à chaque texte de la colonne
        results = df_copy[text_column].apply(self.analyse_text)

        # Extraire les résultats dans de nouvelles colonnes
        df_copy["sentiment_final"] = results.apply(lambda x: x[0])
        df_copy["polarite"] = results.apply(lambda x: x[1])

        # Logger le nombre d'entrées analysées
        self.logger.info(f"Analyse de sentiment terminée pour {len(df_copy)} entrées.")

        return df_copy
