"""
Module de visualisation avec Turtle.
Crée un diagramme en bâton pour représenter les résultats de l'analyse de sentiment.
"""

import turtle


class TurtleVisualizer:
    """Classe pour créer une visualisation par diagramme en bâton avec Turtle."""

    def __init__(self, width: int = 1000, height: int = 700):
        """Initialise le visualiseur Turtle."""
        self.width = width
        self.height = height

        # Configuration de l'écran
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.screen.title("📊 Analyse de Sentiment - Diagramme en Bâton")
        self.screen.bgcolor("#f8f9fa")

        # Tortue principale pour dessiner
        self.drawer = turtle.Turtle()
        self.drawer.speed(0)
        self.drawer.hideturtle()

    def visualize_results(self, summary: dict) -> None:
        """Crée une visualisation du diagramme en bâton des résultats."""

        self.screen.clear()
        self.drawer.clear()

        stats = summary.get("statistiques", {})
        total = summary.get("total_avis_analyses", 0)

        # Dessiner les éléments
        self._draw_background_frame()
        self._draw_title(total)
        self._draw_bar_chart(stats)
        self._draw_legend(stats)

        print("\n✅ Visualisation affichée. La fenêtre reste ouverte jusqu'à fermeture manuelle.")
        turtle.done()

    def _draw_background_frame(self) -> None:
        """Dessine un cadre élégant autour du graphique."""
        self.drawer.penup()
        self.drawer.goto(-450, 300)
        self.drawer.pendown()
        self.drawer.pensize(3)
        self.drawer.pencolor("#333333")
        
        for _ in range(2):
            self.drawer.forward(900)
            self.drawer.right(90)
            self.drawer.forward(600)
            self.drawer.right(90)
        
        self.drawer.pensize(1)

    def _draw_title(self, total: int) -> None:
        """Dessine le titre et les informations principales."""
        self.drawer.penup()
        self.drawer.goto(0, 270)
        self.drawer.color("#1a1a1a")
        self.drawer.write(
            "📊 ANALYSE DE SENTIMENT",
            align="center",
            font=("Arial", 26, "bold")
        )
        
        self.drawer.goto(0, 240)
        self.drawer.color("#666666")
        self.drawer.write(
            f"{total} avis analysés",
            align="center",
            font=("Arial", 14, "normal")
        )

    def _draw_bar_chart(self, stats: dict) -> None:
        """Dessine le diagramme en bâton avec barres 3D."""
        colors = {
            "Positif": "#4CAF50",
            "Negatif": "#F44336",
            "Neutre": "#FFC107"
        }
        
        x_start = -200
        y_base = 0
        bar_width = 100
        spacing = 200
        max_height = 150

        # Axe Y
        self.drawer.penup()
        self.drawer.goto(x_start - 30, y_base - 50)
        self.drawer.pendown()
        self.drawer.pensize(2)
        self.drawer.pencolor("#333333")
        self.drawer.goto(x_start - 30, y_base + max_height + 30)

        # Axe X
        self.drawer.penup()
        self.drawer.goto(x_start - 50, y_base - 50)
        self.drawer.pendown()
        self.drawer.goto(x_start + 450, y_base - 50)
        self.drawer.pensize(1)

        x = x_start
        for sentiment, data in stats.items():
            pct = data.get("pourcentage", 0)
            count = data.get("nombre", 0)
            height = (pct / 100) * max_height
            color = colors.get(sentiment, "#999999")

            # Barre principale
            self.drawer.penup()
            self.drawer.goto(x, y_base)
            self.drawer.fillcolor(color)
            self.drawer.pencolor("#333333")
            self.drawer.pensize(2)
            self.drawer.begin_fill()
            self.drawer.pendown()
            
            self.drawer.goto(x, y_base + height)
            self.drawer.goto(x + bar_width, y_base + height)
            self.drawer.goto(x + bar_width, y_base)
            self.drawer.goto(x, y_base)
            
            self.drawer.end_fill()

            # Ombre 3D
            darker_color = self._darken_color(color)
            self.drawer.penup()
            self.drawer.goto(x + bar_width, y_base + height)
            self.drawer.fillcolor(darker_color)
            self.drawer.begin_fill()
            self.drawer.pendown()
            
            self.drawer.goto(x + bar_width + 8, y_base + height + 8)
            self.drawer.goto(x + bar_width + 8, y_base - 42)
            self.drawer.goto(x + bar_width, y_base - 50)
            self.drawer.goto(x + bar_width, y_base + height)
            
            self.drawer.end_fill()

            # Étiquette de pourcentage
            self.drawer.penup()
            self.drawer.goto(x + bar_width / 2, y_base + height + 20)
            self.drawer.color(color)
            self.drawer.write(f"{pct:.1f}%", align="center", font=("Arial", 12, "bold"))

            # Nombre d'avis sur la barre
            self.drawer.goto(x + bar_width / 2, y_base + height / 2)
            self.drawer.color("white")
            self.drawer.write(f"{count}", align="center", font=("Arial", 11, "bold"))

            # Nom du sentiment sous la barre
            self.drawer.goto(x + bar_width / 2, y_base - 80)
            self.drawer.color("#333333")
            self.drawer.write(sentiment, align="center", font=("Arial", 12, "bold"))

            x += spacing

        self.drawer.pensize(1)

    def _draw_legend(self, stats: dict) -> None:
        """Affiche la légende avec les statistiques détaillées."""
        self.drawer.penup()
        y_position = -160
        
        self.drawer.goto(-400, y_position)
        self.drawer.color("#333333")
        self.drawer.write("Détails:", font=("Arial", 11, "bold"))
        
        y_position -= 25
        total = sum(data.get("nombre", 0) for data in stats.values())
        
        for sentiment, data in stats.items():
            count = data.get("nombre", 0)
            pct = data.get("pourcentage", 0)
            
            self.drawer.goto(-400, y_position)
            self.drawer.color("#333333")
            self.drawer.write(
                f"{sentiment}: {count} avis ({pct:.1f}%)",
                font=("Arial", 10, "normal")
            )
            y_position -= 20
        
        # Instruction de fermeture
        self.drawer.goto(0, -280)
        self.drawer.color("#999999")
        self.drawer.write(
            "💡 Fermez cette fenêtre manuellement pour terminer",
            align="center",
            font=("Arial", 10, "italic")
        )

    def _darken_color(self, hex_color: str) -> str:
        """Assombrit une couleur hexadécimale pour créer un effet 3D."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.7))
        g = max(0, int(g * 0.7))
        b = max(0, int(b * 0.7))
        return f'#{r:02x}{g:02x}{b:02x}'
