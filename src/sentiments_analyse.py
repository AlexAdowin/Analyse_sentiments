import logging  
import pandas as pd 
from typing import Literal
from textblob import TextBlob
import re


# Type pour les labels de sentiment
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
   
    'merci', 'agréable', 'divertissant', 'utile', 'efficacement',
   
    'impressionné', 'surpris', 'dépassé', 'exceptionnel', 'remarquable',
   
    'correct', 'correcte', 'conforme', 'nickel', 'parfaitement'
}

# --- Dictionnaire des mots-clés négatifs ---
NEGATIVE_WORDS = {
   
    'horrible', 'nul', 'pourri', 'mauvais', 'pire', 'inutilisable',
   
    'cassé', 'défaillant', 'décevant', 'dommage', 'déception', 'frustrant',
   
    'problème', 'bug', 'erreur', 'panne', 'dysfonctionnement', 'défaut',
   
    'trop cher', 'cher', 'chère', 'onéreux', 'ruineux', 'hors de prix',
   
    'n\'a jamais', 'n\'ai jamais', 'pas reçu', 'n\'ai reçu que', 'jamais reçu',
   
    'moitié', 'endommagé', 'abîmé', 'déchiré', 'mal traduit', 'incomplet',
   
    'incompréhensible', 'confus', 'confuses', 'trop lourd', 'trop lent',
   
    'retard', 'retardé', 'en retard', 'ne correspond pas', 'différent',
   
    'n\'aurais pas', 'préféré', 'hésité', 'hésiter', 'ne suis pas sûr',
   
   
    'qualité n\'est pas', 'n\'est pas au rendez-vous', 'mediocre', 'médiocre',
   
    'impossible', 'difficultés', 'scandaleux', 'mauvais service', 'nulité',
   
    'insatisfait', 'déçu', 'déçue', 'déçus', 'déçues', 'insupportable',
   
    'inadmissible', 'inacceptable', 'honteux', 'honteuse', 'arnaque'
}

# Mots qui amplifient le sentiment
INTENSIFIERS = {
   
    'très', 'extrêmement', 'absolument', 'tellement', 'ultra', 'super', 
   
    'vraiment', 'totalement', 'complètement', 'particulièrement', 'incroyablement'
}

# Négations
NEGATIONS = {'ne', 'n\'', 'pas', 'jamais', 'non', 'aucun', 'aucune', 'rien', 'sans'}

# Termes d'attente et problèmes de livraison (poids renforcé)
DELIVERY_ISSUES = {
   
    'pas reçu', 'jamais reçu', 'reçu pas', 'attends', 'attendre', 'toujours pas',
   
    'encore pas', 'livraison tard', 'livraison retard', 'non reçu', 'manquant',
   
    'perdu', 'non livré', 'commande perdue', 'colis manquant'
}


class SentimentAnalyzer:
    """Classe améliorée pour analyser le sentiment d'un texte ou d'un DataFrame."""

    def __init__(self, positive_seuil: float = 0.1, negative_seuil: float = -0.1):
        """
        Initialise l'analyseur avec des seuils pour déterminer le sentiment.
        
        Args:
            positive_seuil: score minimum pour considérer un texte comme positif
            negative_seuil: score maximum pour considérer un texte comme négatif
        """
        self.positive_seuil = positive_seuil
        self.negative_seuil = negative_seuil

        # Configuration du logger
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(
            f"Analyseur initialisé - Seuils : Positif >= {positive_seuil}, Négatif <= {negative_seuil}"
        )

    def preprocess_text(self, text: str) -> str:
        """
        Nettoie et normalise le texte pour l'analyse.
        
        Args:
            text: Texte à nettoyer
            
        Returns:
            Texte nettoyé et normalisé
        """
        if not text:
            return ""

        # Conversion en minuscules
        text = text.lower()

        # Suppression des URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)

        # Suppression de la ponctuation mais conservation des émojis
        text = re.sub(r'[^\w\s⭐♥️❤️🔥🚀💯]', ' ', text)

        # Normalisation des espaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def detect_negation_context(self, words: list, current_index: int) -> bool:
        """
        Détecte si un mot est dans un contexte de négation.
        
        Args:
            words: Liste des mots du texte
            current_index: Index du mot courant
            
        Returns:
            True si le mot est dans un contexte négatif
        """
        # Vérifier les 3 mots précédents pour les négations
        start = max(0, current_index - 3)
        for i in range(start, current_index):
            if words[i] in NEGATIONS:
                return True
        return False

    def calculate_keyword_score(self, text_clean: str) -> float:
        """
        Calcule un score basé sur les mots-clés avec gestion des négations.
        
        Args:
            text_clean: Texte nettoyé
            
        Returns:
            Score numérique basé sur les mots-clés
        """
        words = text_clean.split()
        pos_score = 0
        neg_score = 0
        
        for i, word in enumerate(words):
            if word in POSITIVE_WORDS:
                if self.detect_negation_context(words, i):
                    neg_score += 1.0  # "pas bon" → négatif
                else:
                    pos_score += 1.0
                    
            elif word in NEGATIVE_WORDS:
                if self.detect_negation_context(words, i):
                    pos_score += 0.5  # "pas mal" → légèrement positif
                else:
                    neg_score += 1.0
        
        # Vérifier les problèmes de livraison (très négatif - poids renforcé)
        delivery_issues_count = sum(1 for issue in DELIVERY_ISSUES if issue in text_clean)
        if delivery_issues_count > 0:
            neg_score += delivery_issues_count * 2.0  # Poids double pour les problèmes de livraison
        
        # Application des intensifieurs
        if any(word in text_clean for word in INTENSIFIERS):
            if pos_score > neg_score:
                pos_score *= 1.3
            elif neg_score > pos_score:
                neg_score *= 1.3
        
        return (pos_score - neg_score) * 0.15

    def analyse_text(self, text: str) -> tuple[SentimentLabel, float]:
        """
        Analyse un texte et retourne son sentiment et polarité.
        
        Args:
            text: Texte à analyser
            
        Returns:
            Tuple (sentiment, polarité)
        """
        if not text or pd.isna(text):
            return "Neutre", 0.0

        try:
            # Nettoyage du texte
            text_clean = self.preprocess_text(text)
            
            if not text_clean.strip():
                return "Neutre", 0.0

            # Score TextBlob
            blob = TextBlob(text_clean)
            polarity = blob.sentiment.polarity

            # Score basé sur les mots-clés
            keyword_score = self.calculate_keyword_score(text_clean)

            # Combinaison pondérée des scores
            final_score = (0.6 * polarity) + (0.4 * keyword_score)
            
            # Ajustement final pour les problèmes sérieux de livraison
            if any(issue in text_clean for issue in DELIVERY_ISSUES):
                final_score -= 0.3

            # Détermination du sentiment
            if final_score >= self.positive_seuil:
                sentiment = "Positif"
            elif final_score <= self.negative_seuil:
                sentiment = "Negatif"
            else:
                sentiment = "Neutre"

            return sentiment, round(final_score, 3)

        except Exception as e:
            self.logger.error(f"Erreur lors de l'analyse du texte '{text[:50]}...': {e}")
            return "Neutre", 0.0

    def analyse_dataframe(self, df: pd.DataFrame, text_column: str = "review_text") -> pd.DataFrame:
        """
        Analyse une colonne d'un DataFrame et ajoute les colonnes de sentiment.
        
        Args:
            df: DataFrame à analyser
            text_column: Nom de la colonne contenant le texte
            
        Returns:
            DataFrame avec les colonnes de sentiment ajoutées
        """
        if text_column not in df.columns:
            raise ValueError(f"La colonne '{text_column}' n'existe pas dans le DataFrame")

        df_copy = df.copy()

        # Application de l'analyse
        results = df_copy[text_column].apply(self.analyse_text)
        df_copy["sentiment_final"] = results.apply(lambda x: x[0])
        df_copy["polarite"] = results.apply(lambda x: x[1])

        # Statistiques
        sentiment_counts = df_copy["sentiment_final"].value_counts()
        self.logger.info(f"Analyse terminée - {len(df_copy)} entrées traitées")
        self.logger.info(f"Répartition des sentiments: {dict(sentiment_counts)}")

        return df_copy

    def get_sentiment_stats(self, df: pd.DataFrame) -> dict:
        """
        Retourne des statistiques sur les sentiments analysés.
        
        Args:
            df: DataFrame avec colonnes 'sentiment_final' et 'polarite'
            
        Returns:
            Dictionnaire de statistiques
        """
        if "sentiment_final" not in df.columns or "polarite" not in df.columns:
            raise ValueError("Le DataFrame doit contenir les colonnes 'sentiment_final' et 'polarite'")

        stats = {
           
            "total": len(df),
           
            "positifs": len(df[df["sentiment_final"] == "Positif"]),
           
            "negatifs": len(df[df["sentiment_final"] == "Negatif"]),
           
            "neutres": len(df[df["sentiment_final"] == "Neutre"]),
           
            "polarite_moyenne": round(df["polarite"].mean(), 3),
           
            "polarite_mediane": round(df["polarite"].median(), 3),
           
            "taux_positivite": round(len(df[df["sentiment_final"] == "Positif"]) / len(df) * 100, 1)
        }
        
        return stats