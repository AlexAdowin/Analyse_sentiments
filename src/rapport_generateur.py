import json
import logging
import pandas as pd 
from pathlib import Path # gere les chemins de fichiers
from typing import Dict, Any # precise le type de donner retourner 


class Generateur_rapport :
     
    def __init__(self , output_csv : str = "output/resultats.csv" , output_summary : str = "output/summary.json") :
         
        self.output_csv = Path(output_csv)
        
        self.output_summary = Path (output_summary)
        
        self.logger = logging.getLogger(__name__) # prepare le logger pour afficher des infos

       #  gerer les dossiers de sorties 

        self.output_csv.parent.mkdir(parents = True , exist_ok = True) #crée le dossier output/ s’il n’existe pas déjà, pour éviter les erreurs d’écriture.
        
    def generer_rapports(self ,df : pd.DataFrame) -> None :
        
      self.save_details_results(df)
      
      self.save_summary(df)
      
    def save_details_results(self , df : pd,DataFrame) -> None :
        
        try:
            df.to_csv(self.output_csv, index=False)
            
            self.logger.info(f"Résultats détaillés sauvegardés: {self.output_csv}")
            
        except Exception as e:
            
            self.logger.error(f"Erreur lors de la sauvegarde du CSV: {e}")
            
            raise
    
    def save_summary(self , df : pd.DataFrame) -> None : #genere les sauvegardes dee rapport
        
        summary = self.calculer_statistiques(df)
        
        try : 
            
             with open(self.output_summary, 'w', encoding='utf-8') as f:
                 
                 json.dump(summary ,f , indent = 2 , ensure_ascii = False)
                 
             self.logger.info(f"Rapport de synthèse sauvegardé: {self.output_summary}")
            
            
        except Exception as e:
            
            self.logger.error(f"Erreur lors de la sauvegarde du rapport: {e}")
            
            raise
            
                 
    def calculer_statistiques(self, df: pd.DataFrame) -> Dict[str, Any]:
        
        total = len(df)
        
        counts = df["sentiment_final"].value_counts().to_dict()
        
        summary = {
            
            "total_avis_analyses": total,
            
            "statistiques": {
                
                sentiment: {
                    
                    "nombre": counts.get(sentiment, 0),
                    
                    "pourcentage": round((counts.get(sentiment, 0) / total) * 100, 2)
                    
                }
                
                for sentiment in ["Positif", "Négatif", "Neutre"]
            },
            
            "score_moyen_polarite": round(df["polarity_score"].mean(), 4) if "polarity_score" in df.columns else None
        }
        
        return summary
            
            
#j'avoue pour ceci j'ai utiliser IA