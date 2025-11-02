"""Générateur de rapports pour l'analyse de sentiment."""
import json
import pandas as pd
from pathlib import Path


class Generateur_rapport:
    """Génère les rapports CSV et JSON."""
    
    def __init__(self, output_csv: str, output_summary: str):
        self.output_csv = Path(output_csv)
        self.output_summary = Path(output_summary)
        self.output_csv.parent.mkdir(parents=True, exist_ok=True)
    
    def generer_rapports(self, df: pd.DataFrame):
        """Génère tous les rapports."""
        self.save_details_results(df)
        self.save_summary(df)
        print(f"Rapports générés: {self.output_csv} et {self.output_summary}")
    
    def save_details_results(self, df: pd.DataFrame):
        """Sauvegarde le CSV détaillé."""
        df.to_csv(self.output_csv, index=False, encoding='utf-8')
    
    def save_summary(self, df: pd.DataFrame):
        """Sauvegarde le résumé JSON."""
        stats = df['sentiment_final'].value_counts().to_dict()
        total = len(df)
        
        summary = {
            "total_avis": total,
            "statistiques": {
                sentiment: {
                    "nombre": count,
                    "pourcentage": round(count / total * 100, 2)
                }
                for sentiment, count in stats.items()
            },
            "score_moyen_polarite": round(df['polarite'].mean(), 3)
        }
        
        with open(self.output_summary, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
