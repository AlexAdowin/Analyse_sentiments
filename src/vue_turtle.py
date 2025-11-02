"""
Module de visualisation avec Turtle.
Crée des animations graphiques pour représenter les résultats de l'analyse de sentiment.
"""

import turtle
import math
from typing import Dict, Any


class TurtleVisualizer:
    """Classe pour créer des visualisations animées avec Turtle."""
    
    def __init__(self, width: int = 1000, height: int = 700):
        """Initialise le visualiseur Turtle."""
        self.width = width
        self.height = height
        
        # Configuration de l'écran
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.title("📊 Analyse de Sentiment - Visualisation Interactive")
        self.screen.bgcolor("#f5f5f5")
        
        # Tortue principale
        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        self.drawer.hideturtle()
    
    def visualize_results(self, summary: Dict[str, Any]) -> None:
        """Crée une visualisation complète et améliorée des résultats."""
        self.screen.clear()
        self.drawer.clear()
        
        stats = summary.get("statistiques", {})
        total = summary.get("total_avis_analyses", 0)
        score_moyen = summary.get("score_moyen_polarite", 0)
        
        self._draw_header(total)
        self._draw_improved_pie(stats)
        self._draw_improved_bars(stats)
        self._draw_improved_score(score_moyen)
        self._draw_detailed_stats(stats, total)
        self._draw_footer()
        
        print("\n✅ Visualisation affichée. Fenêtre maintenue ouverte en continu.")
        
        # --- 🔁 Boucle infinie pour garder la fenêtre ouverte ---
        try:
            while True:
                self.screen.update()
        except turtle.Terminator:
            print("🟡 Fenêtre fermée manuellement.")
    
    def _draw_header(self, total: int) -> None:
        """Dessine un en-tête stylisé."""
        self.drawer.penup()
        self.drawer.goto(-450, 320)
        self.drawer.fillcolor("#2196F3")
        self.drawer.begin_fill()
        for _ in range(2):
            self.drawer.forward(900)
            self.drawer.right(90)
            self.drawer.forward(80)
            self.drawer.right(90)
        self.drawer.end_fill()
        
        self.drawer.goto(0, 270)
        self.drawer.color("white")
        self.drawer.write(
            "📊 ANALYSE DE SENTIMENT",
            align="center",
            font=("Arial", 24, "bold")
        )
        self.drawer.goto(0, 245)
        self.drawer.write(
            f"{total} avis analysés",
            align="center",
            font=("Arial", 14, "normal")
        )
    
    def _draw_improved_pie(self, stats: Dict[str, Any]) -> None:
        """Dessine un camembert amélioré avec ombres et légende."""
        colors = {"Positif": "#4CAF50", "Négatif": "#F44336", "Neutre": "#FFC107"}
        center_x, center_y, radius = -250, 50, 120
        
        # Ombre
        self.drawer.penup()
        self.drawer.goto(center_x + 5, center_y - 5)
        self.drawer.fillcolor("#cccccc")
        self.drawer.begin_fill()
        self.drawer.circle(radius)
        self.drawer.end_fill()
        
        angle = 0
        legend_y = 150
        
        for sentiment, data in stats.items():
            count = data.get("nombre", 0)
            pct = data.get("pourcentage", 0)
            arc = (pct / 100) * 360
            color = colors.get(sentiment, "gray")
            
            self.drawer.penup()
            self.drawer.goto(center_x, center_y)
            self.drawer.setheading(angle)
            self.drawer.fillcolor(color)
            self.drawer.pencolor("#ffffff")
            self.drawer.pensize(2)
            self.drawer.begin_fill()
            self.drawer.pendown()
            self.drawer.circle(radius, arc)
            self.drawer.goto(center_x, center_y)
            self.drawer.end_fill()
            
            if pct > 5:
                label_angle = angle + arc / 2
                label_x = center_x + (radius * 0.65) * math.cos(math.radians(label_angle))
                label_y = center_y + (radius * 0.65) * math.sin(math.radians(label_angle))
                self.drawer.penup()
                self.drawer.goto(label_x, label_y)
                self.drawer.color("white")
                self.drawer.write(f"{pct:.1f}%", align="center", font=("Arial", 14, "bold"))
            
            self.drawer.penup()
            self.drawer.goto(center_x - 50, legend_y)
            self.drawer.fillcolor(color)
            self.drawer.begin_fill()
            for _ in range(4):
                self.drawer.forward(20)
                self.drawer.right(90)
            self.drawer.end_fill()
            self.drawer.goto(center_x - 20, legend_y)
            self.drawer.color("#333333")
            self.drawer.write(f"{sentiment}: {count} ({pct:.1f}%)", font=("Arial", 12, "normal"))
            legend_y -= 30
            angle += arc
        
        self.drawer.pensize(1)
    
    def _draw_improved_bars(self, stats: Dict[str, Any]) -> None:
        """Dessine des barres 3D améliorées."""
        colors = {"Positif": "#4CAF50", "Négatif": "#F44336", "Neutre": "#FFC107"}
        x_start, y_base, bar_width, spacing = 100, -100, 80, 120
        
        self.drawer.penup()
        self.drawer.goto(x_start + 180, y_base + 200)
        self.drawer.color("#333333")
        self.drawer.write("Distribution des sentiments", align="center", font=("Arial", 14, "bold"))
        
        x = x_start
        max_height = 150
        
        for sentiment, data in stats.items():
            pct = data.get("pourcentage", 0)
            count = data.get("nombre", 0)
            height = (pct / 100) * max_height
            color = colors.get(sentiment, "gray")
            
            self.drawer.penup()
            self.drawer.goto(x, y_base)
            self.drawer.fillcolor(color)
            self.drawer.pencolor("#333333")
            self.drawer.pensize(2)
            self.drawer.begin_fill()
            self.drawer.pendown()
            for dx, dy in [(0, height), (bar_width, 0), (0, -height), (-bar_width, 0)]:
                self.drawer.goto(self.drawer.xcor() + dx, self.drawer.ycor() + dy)
            self.drawer.end_fill()
            
            darker_color = self._darken_color(color)
            self.drawer.penup()
            self.drawer.goto(x, y_base + height)
            self.drawer.fillcolor(darker_color)
            self.drawer.begin_fill()
            self.drawer.pendown()
            for dx, dy in [(10, 10), (bar_width, 0), (-10, -10), (-bar_width, 0)]:
                self.drawer.goto(self.drawer.xcor() + dx, self.drawer.ycor() + dy)
            self.drawer.end_fill()
            
            self.drawer.penup()
            self.drawer.goto(x + bar_width/2, y_base + height + 20)
            self.drawer.color(color)
            self.drawer.write(f"{pct:.1f}%", align="center", font=("Arial", 14, "bold"))
            self.drawer.goto(x + bar_width/2, y_base + height/2)
            self.drawer.color("white")
            self.drawer.write(f"{count}", align="center", font=("Arial", 12, "bold"))
            self.drawer.goto(x + bar_width/2, y_base - 25)
            self.drawer.color("#333333")
            self.drawer.write(sentiment, align="center", font=("Arial", 11, "bold"))
            x += spacing
        
        self.drawer.pensize(1)
    
    def _draw_improved_score(self, score: float) -> None:
        """Dessine un indicateur de score amélioré avec jauge."""
        self.drawer.penup()
        self.drawer.goto(-350, -200)
        self.drawer.color("#333333")
        self.drawer.write("Score moyen de polarité", font=("Arial", 14, "bold"))
        
        center_x, center_y, radius = -250, -270, 50
        self.drawer.penup()
        self.drawer.goto(center_x, center_y - radius)
        self.drawer.pendown()
        self.drawer.pensize(15)
        self.drawer.color("#e0e0e0")
        self.drawer.circle(radius, 180)
        
        if score > 0.1:
            color, label = "#4CAF50", "Positif"
        elif score < -0.1:
            color, label = "#F44336", "Négatif"
        else:
            color, label = "#FFC107", "Neutre"
        
        angle = ((score + 1) / 2) * 180
        self.drawer.penup()
        self.drawer.goto(center_x, center_y - radius)
        self.drawer.pendown()
        self.drawer.color(color)
        self.drawer.circle(radius, angle)
        
        self.drawer.penup()
        self.drawer.goto(center_x, center_y - 20)
        self.drawer.color(color)
        self.drawer.write(f"{score:.3f}", align="center", font=("Arial", 18, "bold"))
        self.drawer.goto(center_x, center_y - 40)
        self.drawer.write(label, align="center", font=("Arial", 12, "normal"))
        self.drawer.pensize(1)
    
    def _draw_detailed_stats(self, stats: Dict[str, Any], total: int) -> None:
        """Affiche des statistiques détaillées."""
        self.drawer.penup()
        self.drawer.goto(-100, -230)
        self.drawer.color("#333333")
        self.drawer.goto(-120, -210)
        self.drawer.pencolor("#2196F3")
        self.drawer.pensize(2)
        self.drawer.pendown()
        for _ in range(2):
            self.drawer.forward(240)
            self.drawer.right(90)
            self.drawer.forward(80)
            self.drawer.right(90)
        
        self.drawer.penup()
        self.drawer.goto(0, -230)
        self.drawer.color("#333333")
        self.drawer.write(f"Total analysé: {total} avis", align="center", font=("Arial", 12, "bold"))
        y = -255
        for sentiment, data in stats.items():
            count = data.get("nombre", 0)
            self.drawer.goto(0, y)
            self.drawer.write(f"{sentiment}: {count} avis", align="center", font=("Arial", 10, "normal"))
            y -= 20
        self.drawer.pensize(1)
    
    def _draw_footer(self) -> None:
        """Dessine le pied de page avec instructions."""
        self.drawer.penup()
        self.drawer.goto(0, -320)
        self.drawer.color("#666666")
        self.drawer.write("💡 Fermez cette fenêtre manuellement pour terminer", align="center", font=("Arial", 11, "italic"))
    
    def _darken_color(self, hex_color: str) -> str:
        """Assombrit une couleur hexadécimale pour l'effet 3D."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.7))
        g = max(0, int(g * 0.7))
        b = max(0, int(b * 0.7))
        return f'#{r:02x}{g:02x}{b:02x}'
