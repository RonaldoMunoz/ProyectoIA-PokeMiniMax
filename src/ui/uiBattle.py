import arcade
import os
import random

# Configuración de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pokeminmax"
# Factores de escala
PLAYER_SCALE   = 1.6
OPPONENT_SCALE = 1.6

# Ruta a assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

class PokemonBattleUI(arcade.View):
    def __init__(self):
        super().__init__()

        # Sprites de Pokémon
        self.player_sprite = None
        self.opponent_sprite = None

        # Fuente personalizada
        self.font = None

        # Fondo
        self.background = None

        # Estado del combate
        self.player_hp = 150
        self.player_max_hp = 150
        self.opponent_hp = 140
        self.opponent_max_hp = 140
        self.player_pokemon = "Charizard"
        self.opponent_pokemon = "Blastoise"
        self.message = "¡Comienza el combate!"
        self.attack_buttons = []
        self.selected_attack = None
        self.turn_phase = "player"
        self.effectiveness_message = ""

        # Color de fondo
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Precargar fuente Pokémon
        font_path = os.path.join(ASSETS_PATH, "fonts", "pokemon.ttf")
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.font = "pokemon.ttf"

        # Precargar textura de fondo
        bg_path = os.path.join(ASSETS_PATH, "backgrounds", "backgroundBattle.png")
        if os.path.exists(bg_path):
            self.background = arcade.load_texture(bg_path)

        # Setup inicial
        self.setup()

    def setup(self):
        """Configurar sprites y botones."""
        # Charizard
        player_path = os.path.join(ASSETS_PATH, "pokemon", "Charizard.png")
        if os.path.exists(player_path):
            self.player_sprite = arcade.Sprite(player_path, scale=PLAYER_SCALE)
            self.player_sprite.center_x = 200
            self.player_sprite.center_y = 160

        # Blastoise
        opp_path = os.path.join(ASSETS_PATH, "pokemon", "Blastoise.png")
        if os.path.exists(opp_path):
            self.opponent_sprite = arcade.Sprite(opp_path, scale=OPPONENT_SCALE)
            self.opponent_sprite.center_x = 600
            self.opponent_sprite.center_y = 450
        # Botones de ataque
        self.attack_buttons = [
            {"name": "Lanzallamas", "type": "Fuego",   "power": 90,  "x": 200, "y": 80},
            {"name": "Garra Dragón","type": "Dragón",  "power": 80,  "x": 450, "y": 80},
            {"name": "Giro Fuego",  "type": "Fuego",   "power": 60,  "x": 200, "y": 40},
            {"name": "Tajo Aéreo",  "type": "Volador", "power": 75,  "x": 450, "y": 40},
        ]

        # Turno IA cada 3s
        arcade.schedule(self.ai_turn, 3.0)

    def on_draw(self):
        """Renderizar todos los elementos."""
        self.clear()

        # Fondo
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0,
                SCREEN_WIDTH, SCREEN_HEIGHT,
                self.background
            )

        # Título y turno
        arcade.draw_text(
            "POKEMINMAX BATTLE",
            SCREEN_WIDTH//2, SCREEN_HEIGHT - 30,
            arcade.color.RED, 24,
            anchor_x="center", font_name=self.font, bold=True
        )
        turn_text = "Tu turno" if self.turn_phase=="player" else "Turno del oponente"
        turn_color = (arcade.color.BLUE if self.turn_phase=="player" else arcade.color.RED)
        arcade.draw_text(
            turn_text,
            SCREEN_WIDTH//2, SCREEN_HEIGHT - 60,
            turn_color, 20,
            anchor_x="center", font_name=self.font
        )

        # Mensajes de acción/efectividad
        arcade.draw_text(
            self.message,
            SCREEN_WIDTH//2, 95,
            arcade.color.BLACK, 16,
            anchor_x="center", font_name=self.font
        )
        if self.effectiveness_message:
            arcade.draw_text(
                self.effectiveness_message,
                SCREEN_WIDTH//2, 75,
                arcade.color.RED, 16,
                anchor_x="center", font_name=self.font
            )

        # Sprites
        if self.opponent_sprite:
            self.opponent_sprite.draw()
        if self.player_sprite:
            self.player_sprite.draw()

        # Barras de vida
        self.draw_health_bar(
            600, 520,
            self.opponent_hp, self.opponent_max_hp,
            self.opponent_pokemon, is_opponent=True
        )
        self.draw_health_bar(
            200, 220,
            self.player_hp, self.player_max_hp,
            self.player_pokemon, is_opponent=False
        )

        # Panel de ataques
        arcade.draw_rectangle_filled(
            SCREEN_WIDTH//2, 60,
            SCREEN_WIDTH-40, 120,
            arcade.color.WHITE
        )
        arcade.draw_rectangle_outline(
            SCREEN_WIDTH//2, 60,
            SCREEN_WIDTH-40, 120,
            arcade.color.BLACK, 2
        )

        # Botones
        type_colors = {
            "Fuego": arcade.color.RED,
            "Agua": arcade.color.BLUE,
            "Planta": arcade.color.GREEN,
            "Eléctrico": arcade.color.YELLOW,
            "Volador": arcade.color.LIGHT_BLUE,
            "Dragón": arcade.color.PURPLE,
            "Normal": arcade.color.LIGHT_GRAY
        }
        for btn in self.attack_buttons:
            color = type_colors.get(btn["type"], arcade.color.LIGHT_GRAY)
            border = (arcade.color.GOLD if self.selected_attack==btn["name"]
                      else arcade.color.BLACK)
            arcade.draw_rectangle_filled(btn["x"], btn["y"], 200, 30, color)
            arcade.draw_rectangle_outline(btn["x"], btn["y"], 200, 30, border, 2)
            arcade.draw_text(
                btn["name"],
                btn["x"], btn["y"],
                arcade.color.BLACK, 14,
                anchor_x="center", anchor_y="center",
                font_name=self.font
            )

    def draw_health_bar(self, x, y, current, maximum, name, is_opponent):
        """Barra de vida estilo Pokémon con texto centrado y nombre."""
        # Fondo y borde
        arcade.draw_rectangle_filled(x, y, 200, 20, (40,40,40))
        arcade.draw_rectangle_outline(x, y, 200, 20, arcade.color.BLACK, 2)

        # Relleno
        ratio = max(0, min(1, current/maximum)) if maximum>0 else 0
        fill_w = 196 * ratio
        fill_color = (arcade.color.GREEN if ratio>0.6
                      else arcade.color.YELLOW if ratio>0.3
                      else arcade.color.RED)
        arcade.draw_rectangle_filled(
            x - 98 + fill_w/2, y,
            fill_w, 16,
            fill_color
        )

        # Texto de PS (centrado sobre la barra)
        hp_text = f"{current}/{maximum}"
        arcade.draw_text(
            hp_text,
            x, y + 14,
            arcade.color.BLACK, 12,
            anchor_x="center", anchor_y="bottom",
            font_name=self.font
        )

        # Nombre (alineado al extremo)
        if is_opponent:
            name_x, anchor = x + 110, "left"
        else:
            name_x, anchor = x - 110, "right"

        arcade.draw_text(
            name,
            name_x, y + 12,
            arcade.color.BLACK, 14,
            anchor_x=anchor, anchor_y="bottom",
            font_name=self.font
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Clic en ataques en tu turno."""
        if button==arcade.MOUSE_BUTTON_LEFT and self.turn_phase=="player":
            for btn in self.attack_buttons:
                if abs(x-btn["x"])<100 and abs(y-btn["y"])<15:
                    self.selected_attack = btn["name"]
                    self.use_attack(btn)
                    break

    def use_attack(self, attack):
        """Turno jugador."""
        self.message = f"¡{self.player_pokemon} usó {attack['name']}!"
        self.effectiveness_message = ""
        eff = random.choice(["normal","super","not_very"])
        base = attack["power"]
        if eff=="super":
            dmg = int(base*1.5*random.uniform(0.9,1.1))
            self.effectiveness_message = "¡Es super efectivo!"
        elif eff=="not_very":
            dmg = int(base*0.7*random.uniform(0.9,1.1))
            self.effectiveness_message = "No es muy efectivo..."
        else:
            dmg = int(base*random.uniform(0.85,1.0))

        self.opponent_hp = max(0, self.opponent_hp - dmg)
        self.turn_phase = "opponent"
        self.selected_attack = None

        if self.opponent_hp<=0:
            self.message = f"¡{self.opponent_pokemon} fue derrotado! ¡Ganaste!"
            arcade.unschedule(self.ai_turn)

    def ai_turn(self, dt):
        """Turno IA."""
        if self.turn_phase!="opponent":
            return
        moves = [
            {"name":"Hidrobomba","type":"Agua","power":110},
            {"name":"Rayo Hielo","type":"Hielo","power":90},
            {"name":"Cabezazo","type":"Normal","power":70},
            {"name":"Pistola Agua","type":"Agua","power":40},
        ]
        atk = random.choice(moves)
        self.message = f"¡{self.opponent_pokemon} usó {atk['name']}!"
        self.effectiveness_message = ""
        eff = random.choice(["normal","super","not_very"])
        base = atk["power"]
        if eff=="super":
            dmg = int(base*1.5*random.uniform(0.9,1.1))
            self.effectiveness_message = "¡Es super efectivo!"
        elif eff=="not_very":
            dmg = int(base*0.7*random.uniform(0.9,1.1))
            self.effectiveness_message = "No es muy efectivo..."
        else:
            dmg = int(base*random.uniform(0.85,1.0))

        self.player_hp = max(0, self.player_hp - dmg)
        self.turn_phase = "player"

        if self.player_hp<=0:
            self.message = f"¡{self.player_pokemon} fue derrotado! ¡Perdiste!"
            arcade.unschedule(self.ai_turn)


def main():
    """Función principal."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    battle = PokemonBattleUI()
    window.show_view(battle)
    arcade.run()

if __name__ == "__main__":
    main()
