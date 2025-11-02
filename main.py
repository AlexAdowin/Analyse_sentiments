
import sys
import logging
import json
from pathlib import Path
from src.data_charge import DataCharger
from src.sentiments_analyse import SentimentAnalyzer
from src.rapport_generateur import Generateur_rapport
from src.vue_turtle import TurtleVisualizer
from src.config import Config


def setup_logging(log_level: str = "INFO") -> None:
    """Configure le système de logging pour la traçabilité."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def main() -> None:
    """
    Fonction principale qui exécute le pipeline complet d'analyse de sentiment.
    
    Pipeline:
    1. Chargement de la configuration
    2. Chargement des données
    3. Analyse de sentiment
    4. Génération des rapports
    5. Visualisation avec Turtle (nouveau)
    """
    # Créer le dossier logs s'il n'existe pas
    Path("logs").mkdir(exist_ok=True)
    
    # Configuration du logging
    config = Config()
    setup_logging(config.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("=== Démarrage de l'analyse de sentiment ===")
        
        # Étape 1: Chargement des données
        print("Chargement des données...")
        data_loader = DataCharger(config.input_file)
        reviews_df = data_loader.load_data()
        print(f"{len(reviews_df)} avis chargés")
        
        # Étape 2: Analyse de sentiment
        print("Analyse en cours...")
        analyzer = SentimentAnalyzer(
            positive_seuil=config.positive_seuil,
            negative_seuil=config.negative_seuil
        )
        analyzed_df = analyzer.analyse_dataframe(reviews_df)
        print("Analyse terminée")
        
        # Étape 3: Génération des rapports
        print("Génération des rapports...")
        report_gen = Generateur_rapport(
            output_csv=config.output_csv,
            output_summary=config.output_summary
        )
        report_gen.generer_rapports(analyzed_df)
        print(f"Rapports: {config.output_csv}, {config.output_summary}")
        
        # Étape 4: Visualisation avec Turtle
        print("Visualisation...")
        with open(config.output_summary, 'r', encoding='utf-8') as f:
            summary = json.load(f)
        
        visualizer = TurtleVisualizer()
        visualizer.visualize_results(summary)
        
        print("Terminé!")
        
        logger.info("=== Analyse terminée avec succès ===")
        
    except FileNotFoundError as e:
        logger.error(f"Fichier non trouvé: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Erreur de validation des données: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
