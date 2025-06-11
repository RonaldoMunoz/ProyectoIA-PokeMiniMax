import arcade
import os
import random

# Configuración de la ventana
SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Pokeminmax Battle"

# Ruta a assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


class PokemonBattleUI(arcade.View):
    def __init__(self):
        super().__init__()

        # Fondo como SpriteList
        self.background_list = arcade.SpriteList()

        # Fuente (usaremos la por defecto si no existe el archivo)
        self.font = None

        # Botones y paneles
        self.action_buttons = []
        self.attack_buttons = []
        self.info_panels = []

        # Estado de combate
        self.player_hp = 150
        self.player_max_hp = 150
        self.opponent_hp = 140
        self.opponent_max_hp = 140
        self.player_pokemon = "Charizard"
        self.opponent_pokemon = "Blastoise"
        self.player_team = ["Charizard", "Pikachu", "Venusaur"]
        self.opponent_team = ["Blastoise", "Gyarados", "Alakazam"]
        self.message = "¡Comienza el combate!"
        self.selected_action = None
        self.turn_phase = "player"

        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        self.setup()

    def setup(self):
        # Intentar cargar fondo (opcional)
        try:
            bg_path = os.path.join(ASSETS_PATH, "backgrounds", "battle_bg.png")
            if os.path.exists(bg_path):
                bg = arcade.Sprite(bg_path, scale=1.0)
                bg.center_x = SCREEN_WIDTH // 2
                bg.center_y = SCREEN_HEIGHT // 2
                self.background_list.append(bg)
        except:
            # Si no existe el fondo, continuamos sin él
            pass

        # Intentar cargar fuente personalizada
        try:
            font_path = os.path.join(ASSETS_PATH, "fonts", "Pokemon Solid.ttf")
            if os.path.exists(font_path):
                self.font = font_path
                print(f"Fuente cargada: {self.font}")
        except:
            # Usar fuente por defecto
            pass

        # Crear UI
        self.create_action_buttons()
        self.create_attack_buttons()
        self.create_info_panels()

        # Programar IA
        arcade.schedule(self.ai_turn, 3.0)

    def create_action_buttons(self):
        self.action_buttons = [
            {"name": "Luchar",   "x": 150, "y":  80, "w": 200, "h": 50},
            {"name": "Pokémon",  "x": 400, "y":  80, "w": 200, "h": 50},
            {"name": "Mochila",  "x": 650, "y":  80, "w": 200, "h": 50},
            {"name": "Huir",     "x": 900, "y":  80, "w": 200, "h": 50},
        ]

    def create_attack_buttons(self):
        self.attack_buttons = [
            {"name": "Lanzallamas",  "type": "Fuego",   "power": 90, "x": 150, "y": 200},
            {"name": "Garra Dragón", "type": "Dragón",  "power": 80, "x": 400, "y": 200},
            {"name": "Giro Fuego",   "type": "Fuego",   "power": 60, "x": 650, "y": 200},
            {"name": "Tajo Aéreo",   "type": "Volador", "power": 75, "x": 900, "y": 200},
        ]

    def create_info_panels(self):
        self.info_panels = [
            {"title": "Tú",       "x": 150, "y": 600, "w": 300, "h": 120},
            {"title": "Oponente", "x": 750, "y": 600, "w": 300, "h": 120},
            {"title": "Mensajes", "x": 150, "y": 300, "w": 800, "h": 150},
        ]

    def draw_rectangle_outline(self, center_x, center_y, width, height, color, border_width=2):
        """Dibuja el contorno de un rectángulo usando líneas"""
        half_width = width / 2
        half_height = height / 2
        
        # Líneas del rectángulo
        points = [
            (center_x - half_width, center_y - half_height),
            (center_x + half_width, center_y - half_height),
            (center_x + half_width, center_y + half_height),
            (center_x - half_width, center_y + half_height),
            (center_x - half_width, center_y - half_height)  # Cerrar el rectángulo
        ]
        
        arcade.draw_line_strip(points, color, border_width)

    def on_draw(self):
        self.clear()
        
        # 1) Fondo
        if len(self.background_list) > 0:
            self.background_list.draw()

        # 2) Paneles de información
        for p in self.info_panels:
            # Dibujar fondo semi-transparente
            arcade.draw_lrbt_rectangle_filled(
                p["x"] - p["w"]/2,  # left
                p["x"] + p["w"]/2,  # right
                p["y"] - p["h"]/2,  # bottom
                p["y"] + p["h"]/2,  # top
                (0, 0, 0, 180)
            )
            
            # Dibujar contorno
            self.draw_rectangle_outline(
                p["x"], p["y"], p["w"], p["h"],
                arcade.color.YELLOW, 3
            )
            
            # Título
            arcade.draw_text(
                p["title"],
                p["x"], p["y"] + p["h"]/2 - 15,
                arcade.color.WHITE, 20,
                anchor_x="center", font_name=self.font
            )

            # Contenido según panel
            if p["title"] == "Tú":
                arcade.draw_text(
                    self.player_pokemon,
                    p["x"] - 100, p["y"] - 10,
                    arcade.color.WHITE, 24,
                    anchor_x="center", font_name=self.font
                )
                self.draw_health_bar(
                    p["x"], p["y"] - 40,
                    self.player_hp, self.player_max_hp
                )
            elif p["title"] == "Oponente":
                arcade.draw_text(
                    self.opponent_pokemon,
                    p["x"] + 100, p["y"] - 10,
                    arcade.color.WHITE, 24,
                    anchor_x="center", font_name=self.font
                )
                self.draw_health_bar(
                    p["x"], p["y"] - 40,
                    self.opponent_hp, self.opponent_max_hp
                )
            else:  # Mensajes
                arcade.draw_text(
                    self.message,
                    p["x"], p["y"] - 30,
                    arcade.color.WHITE, 18,
                    width=p["w"] - 20,
                    align="center",
                    anchor_x="center", anchor_y="center",
                    font_name=self.font
                )

        # 3) Botones de acción
        for b in self.action_buttons:
            # Fondo del botón
            arcade.draw_lrbt_rectangle_filled(
                b["x"] - b["w"]/2,  # left
                b["x"] + b["w"]/2,  # right
                b["y"] - b["h"]/2,  # bottom
                b["y"] + b["h"]/2,  # top
                arcade.color.RED if self.selected_action == b["name"]
                else arcade.color.LIGHT_GRAY
            )
            
            # Contorno del botón
            self.draw_rectangle_outline(
                b["x"], b["y"], b["w"], b["h"],
                arcade.color.BLACK, 2
            )
            
            # Texto del botón
            arcade.draw_text(
                b["name"],
                b["x"], b["y"],
                arcade.color.BLACK, 18,
                anchor_x="center", anchor_y="center",
                font_name=self.font
            )

        # 4) Botones de ataque (modo Luchar)
        if self.selected_action == "Luchar":
            type_colors = {
                "Fuego":    arcade.color.RED,
                "Agua":     arcade.color.BLUE,
                "Planta":   arcade.color.GREEN,
                "Eléctrico":arcade.color.YELLOW,
                "Volador":  arcade.color.LIGHT_BLUE,
                "Dragón":   arcade.color.PURPLE
            }
            for a in self.attack_buttons:
                # Fondo del botón de ataque
                arcade.draw_lrbt_rectangle_filled(
                    a["x"] - 100,  # left
                    a["x"] + 100,  # right
                    a["y"] - 25,   # bottom
                    a["y"] + 25,   # top
                    type_colors.get(a["type"], arcade.color.LIGHT_GRAY)
                )
                
                # Contorno del botón de ataque
                self.draw_rectangle_outline(
                    a["x"], a["y"], 200, 50,
                    arcade.color.BLACK, 2
                )
                
                # Texto del ataque
                arcade.draw_text(
                    a["name"],
                    a["x"], a["y"] + 10,
                    arcade.color.BLACK, 16,
                    anchor_x="center", font_name=self.font
                )
                arcade.draw_text(
                    f"{a['type']} - Poder: {a['power']}",
                    a["x"], a["y"] - 10,
                    arcade.color.BLACK, 14,
                    anchor_x="center", font_name=self.font
                )

        # 5) Equipo (modo Pokémon)
        if self.selected_action == "Pokémon":
            for i, pkm in enumerate(self.player_team):
                x = 150 + (i % 3) * 250
                y = 300 + (i // 3) * 100
                
                # Fondo del botón de Pokémon
                arcade.draw_lrbt_rectangle_filled(
                    x - 100, x + 100,  # left, right
                    y - 40, y + 40,    # bottom, top
                    arcade.color.GREEN if pkm == self.player_pokemon
                    else arcade.color.LIGHT_GRAY
                )
                
                # Contorno del botón de Pokémon
                self.draw_rectangle_outline(
                    x, y, 200, 80,
                    arcade.color.BLACK, 2
                )
                
                # Texto del Pokémon
                arcade.draw_text(
                    pkm, x, y,
                    arcade.color.BLACK, 18,
                    anchor_x="center", anchor_y="center",
                    font_name=self.font
                )

        # 6) Título y turno
        arcade.draw_text(
            "POKEMINMAX BATTLE - DEMO UI",
            SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40,
            arcade.color.RED, 28,
            anchor_x="center", font_name=self.font, bold=True
        )
        turno = "Tu turno" if self.turn_phase == "player" else "Turno del oponente"
        turno_color = arcade.color.BLUE if self.turn_phase == "player" else arcade.color.RED
        arcade.draw_text(
            turno,
            SCREEN_WIDTH // 2, 40,
            turno_color, 24,
            anchor_x="center", font_name=self.font
        )

    def draw_health_bar(self, x, y, current, maximum):
        # Fondo de barra
        arcade.draw_lrbt_rectangle_filled(
            x - 125, x + 125,  # left, right
            y - 10, y + 10,    # bottom, top
            (50, 50, 50)
        )
        
        # Porción de vida
        if maximum > 0:  # Evitar división por cero
            ratio = current / maximum
            bar_color = (0, 200, 0) if ratio > 0.6 else (255, 200, 0) if ratio > 0.3 else (255, 50, 50)
            arcade.draw_lrbt_rectangle_filled(
                x - 123, x - 123 + (246 * ratio),  # left, right
                y - 8, y + 8,                       # bottom, top
                bar_color
            )
        
        # Texto de PS
        arcade.draw_text(
            f"PS: {current}/{maximum}",
            x, y - 30,
            arcade.color.WHITE, 16,
            anchor_x="center", font_name=self.font
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT or self.turn_phase != "player":
            return

        # Botones de acción
        for b in self.action_buttons:
            if abs(x - b["x"]) < b["w"]/2 and abs(y - b["y"]) < b["h"]/2:
                self.selected_action = b["name"]
                self.message = f"Seleccionaste: {b['name']}"
                return

        # Ataques
        if self.selected_action == "Luchar":
            for a in self.attack_buttons:
                if abs(x - a["x"]) < 100 and abs(y - a["y"]) < 25:
                    self.use_attack(a)
                    return

        # Cambio de Pokémon
        if self.selected_action == "Pokémon":
            for i, pkm in enumerate(self.player_team):
                bx = 150 + (i % 3) * 250
                by = 300 + (i // 3) * 100
                if abs(x - bx) < 100 and abs(y - by) < 40:
                    self.switch_pokemon(pkm)
                    return

    def use_attack(self, attack):
        self.message = f"¡{self.player_pokemon} usó {attack['name']}!"
        eff = random.choice(["", "¡Es super efectivo! ", "¡No es muy efectivo... "])
        dmg = int(attack["power"] * random.uniform(0.8, 1.2) *
                  (1.5 if "super" in eff else 0.7 if "no es muy" in eff else 1))
        self.opponent_hp = max(0, self.opponent_hp - dmg)
        self.message += f" {eff}Hizo {dmg} de daño."
        self.selected_action = None
        self.turn_phase = "opponent"

    def switch_pokemon(self, pokemon):
        if pokemon != self.player_pokemon:  # Solo cambiar si es diferente
            self.player_pokemon = pokemon
            self.player_hp = random.randint(100, 200)
            self.player_max_hp = self.player_hp
            self.message = f"¡Has cambiado a {pokemon}!"
            self.selected_action = None
            self.turn_phase = "opponent"

    def ai_turn(self, delta_time: float):
        if self.turn_phase != "opponent":
            return
            
        # Verificar si el juego ha terminado
        if self.player_hp <= 0 or self.opponent_hp <= 0:
            return
            
        moves = ["Hidrobomba", "Rayo Hielo", "Cabezazo", "Pistola Agua"]
        mv = random.choice(moves)
        dmg = random.randint(15, 35)
        eff = random.choice(["", "¡Es super efectivo! ", "¡No es muy efectivo... "])
        if eff:
            dmg = int(dmg * (1.5 if "super" in eff else 0.7))
        self.player_hp = max(0, self.player_hp - dmg)
        self.message = f"¡{self.opponent_pokemon} usó {mv}! {eff}Hizo {dmg} de daño."
        self.turn_phase = "player"
        
        # Verificar condiciones de fin de juego
        if self.player_hp <= 0:
            self.message = "¡Todos tus Pokémon se han debilitado!\n¡Has perdido!"
            arcade.unschedule(self.ai_turn)
        elif self.opponent_hp <= 0:
            self.message = "¡Todos los Pokémon rivales se han debilitado!\n¡Has ganado!"
            arcade.unschedule(self.ai_turn)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    view = PokemonBattleUI()
    window.show_view(view)
    arcade.run()


if __name__ == "__main__":
    main()