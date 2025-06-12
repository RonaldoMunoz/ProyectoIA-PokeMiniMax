import arcade
import os
import random
import sys
from pathlib import Path
from battle.pokemon import Pokemon, Move
from ai.pokeminimax import minimax
from battle.damage import get_effectivenessMessage
from battle.battle import BattleState

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))
# Configuración de la ventana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pokeminmax"
# Factores de escala
PLAYER_SCALE   = 1.6
OPPONENT_SCALE = 1.6

# Ruta a assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

POKEMON_DATA = {
    "Charizard": {
        "types": ["Fuego", "Volador"],
        "hp": 1000,
        "attacks": [
            {"name": "Lanzallamas", "type": "Fuego", "power": 90},
            {"name": "Garra Dragón", "type": "Dragón", "power": 80},
            {"name": "Giro Fuego", "type": "Fuego", "power": 60},
            {"name": "Tajo Aéreo", "type": "Volador", "power": 75}
        ]
    },
    "Blastoise": {
        "types": ["Agua"],
        "hp": 1000,
        "attacks": [
            {"name": "Hidrobomba", "type": "Agua", "power": 110},
            {"name": "Rayo Hielo", "type": "Hielo", "power": 90},
            {"name": "Cabezazo", "type": "Normal", "power": 70},
            {"name": "Pistola Agua", "type": "Agua", "power": 40}
        ]
    }
}


def create_pokemon(name: str) -> Pokemon:
    """Crea una instancia de Pokémon con sus movimientos"""
    data = POKEMON_DATA[name]
    moves = [Move(move["name"], move["type"], move["power"]) for move in data["attacks"]]
    return Pokemon(name, data["types"], data["hp"], moves)

# 4. Vistas de la interfaz gráfica

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.button_rect = None
        self.button_color = arcade.color.YELLOW
        self.button_hover_color = arcade.color.GOLD
        self.current_button_color = self.button_color

    def on_show(self):
        # Cargar fondo
        background_path = os.path.join(ASSETS_PATH, "backgrounds", "fondomenu.jpg")
        if os.path.exists(background_path):
            self.background = arcade.load_texture(background_path)

        # Registrar fuente personalizada
        self.font_name = "Pokemon Hollow"
        font_path = os.path.join(ASSETS_PATH, "fonts", "Pokemon Hollow.ttf")
        arcade.load_font(font_path)

        # Definir botón
        self.button_rect = arcade.get_rectangle_points(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 300, 60, 20)

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        else:
            arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Dibujar título
        arcade.draw_text("POKEMINMAX", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, arcade.color.YELLOW, 60, font_name=self.font_name, anchor_x="center")

        # Dibujar botón
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 300, 60, self.current_button_color, tilt_angle=0)
        arcade.draw_text("Iniciar Batalla", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 10, arcade.color.BLACK, 20, font_name=self.font_name, anchor_x="center")

    def on_mouse_motion(self, x, y, dx, dy):
        if (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150) and (SCREEN_HEIGHT // 2 - 30 < y < SCREEN_HEIGHT // 2 + 30):
            self.current_button_color = self.button_hover_color
        else:
            self.current_button_color = self.button_color

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (SCREEN_WIDTH // 2 - 150 < x < SCREEN_WIDTH // 2 + 150) and (SCREEN_HEIGHT // 2 - 30 < y < SCREEN_HEIGHT // 2 + 30):
                selection_view = PokemonSelectionView()
                self.window.show_view(selection_view)

class PokemonSelectionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selection = None
        self.background = None
        self.font_name = "Pokemon Solid"

    def on_show(self):
        # Cargar fondo
        background_path = os.path.join(ASSETS_PATH, "backgrounds", "fondo2.jpg")
        if os.path.exists(background_path):
            self.background = arcade.load_texture(background_path)

        # Registrar fuente
        font_path = os.path.join(ASSETS_PATH, "fonts", "Pokemon_Solid.ttf")
        arcade.load_font(font_path)

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        else:
            arcade.set_background_color(arcade.color.LIGHT_BLUE)

        arcade.draw_text("ELIGE TU POKEMON", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, arcade.color.VIOLET, 40, font_name=self.font_name, anchor_x="center")
        
        # Opciones de Pokémon
        arcade.draw_rectangle_filled(250, 300, 200, 100, arcade.color.VIOLET)
        arcade.draw_text("Charizard", 250, 300, arcade.color.WHITE, 20, anchor_x="center", anchor_y="center", font_name=self.font_name)

        arcade.draw_rectangle_filled(550, 300, 200, 100, arcade.color.VIOLET)
        arcade.draw_text("Blastoise", 550, 300, arcade.color.WHITE, 20, anchor_x="center", anchor_y="center", font_name=self.font_name)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if 150 < x < 350 and 250 < y < 350:
                selected_pokemon = "Charizard"
            elif 450 < x < 650 and 250 < y < 350:
                selected_pokemon = "Blastoise"
            else:
                return

            # Crear instancias de Pokémon
            player_pokemon = create_pokemon(selected_pokemon)
            opponent_pokemon = create_pokemon("Blastoise" if selected_pokemon == "Charizard" else "Charizard")
            
            battle_view = PokemonBattleUI(player_pokemon, opponent_pokemon)
            self.window.show_view(battle_view)

class PokemonBattleUI(arcade.View):
    def __init__(self, player_pokemon: Pokemon, opponent_pokemon: Pokemon):
        super().__init__()
        self.player_pokemon = player_pokemon
        self.opponent_pokemon = opponent_pokemon
        self.battle_state = BattleState(player_pokemon, opponent_pokemon, [player_pokemon], [opponent_pokemon], current_turn=0)
        self.message = "¡Comienza el combate!"
        self.effectiveness_message = ""
        self.attack_buttons = []
        self.selected_attack = None
        self.font = None
        self.background = None
        self.player_sprite = None
        self.opponent_sprite = None

        # Precargar fuente
        font_path = os.path.join(ASSETS_PATH, "fonts", "pokemon.ttf")
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.font = "pokemon.ttf"

        # Precargar fondo
        bg_path = os.path.join(ASSETS_PATH, "backgrounds", "backgroundBattle.png")
        if os.path.exists(bg_path):
            self.background = arcade.load_texture(bg_path)

        # Setup inicial
        self.setup()

    def setup(self):
        """Configurar sprites y botones según los Pokémon"""
        # Cargar sprites
        player_path = os.path.join(ASSETS_PATH, "pokemon", f"{self.player_pokemon.name}.png")
        opp_path = os.path.join(ASSETS_PATH, "pokemon", f"{self.opponent_pokemon.name}.png")
        
        if os.path.exists(player_path):
            self.player_sprite = arcade.Sprite(player_path, scale=PLAYER_SCALE)
            self.player_sprite.center_x = 200
            self.player_sprite.center_y = 160
        
        if os.path.exists(opp_path):
            self.opponent_sprite = arcade.Sprite(opp_path, scale=OPPONENT_SCALE)
            self.opponent_sprite.center_x = 600
            self.opponent_sprite.center_y = 450

        # Crear botones de ataque
        positions = [(200, 80), (450, 80), (200, 40), (450, 40)]
        for i, move in enumerate(self.player_pokemon.moves):
            if i < len(positions):
                self.attack_buttons.append({
                    "name": move.name,
                    "type": move.move_type,
                    "power": move.power,
                    "move": move,  # Guardar objeto Move
                    "x": positions[i][0],
                    "y": positions[i][1]
                })

    def on_draw(self):
        """Renderizar todos los elementos"""
        self.clear()

        # Fondo
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Indicador de turno
        turn_text = "Tu turno" if self.battle_state.current_turn == 0 else "Turno del oponente"
        turn_color = arcade.color.BLUE if self.battle_state.current_turn == 0 else arcade.color.RED
        arcade.draw_text(turn_text, SCREEN_WIDTH//2, SCREEN_HEIGHT - 60, turn_color, 20, anchor_x="center", font_name=self.font)

        # Mensajes de acción/efectividad
        arcade.draw_text(self.message, SCREEN_WIDTH//2, 95, arcade.color.BLACK, 16, anchor_x="center", font_name=self.font)
        
        if self.effectiveness_message:
            arcade.draw_text(self.effectiveness_message, SCREEN_WIDTH//2, 75, arcade.color.RED, 16, anchor_x="center", font_name=self.font)

        # Sprites
        if self.opponent_sprite:
            self.opponent_sprite.draw()
        if self.player_sprite:
            self.player_sprite.draw()

        # Barras de vida
        self.draw_health_bar(
            600, 520,
            self.battle_state.opponent_pokemon.current_hp,
            self.battle_state.opponent_pokemon.max_hp,
            self.opponent_pokemon.name, 
            is_opponent=True
        )
        
        self.draw_health_bar(
            200, 220,
            self.battle_state.player_pokemon.current_hp,
            self.battle_state.player_pokemon.max_hp,
            self.player_pokemon.name, 
            is_opponent=False
        )

        # Panel de ataques
        arcade.draw_rectangle_filled(SCREEN_WIDTH//2, 60, SCREEN_WIDTH-40, 120, arcade.color.WHITE)
        arcade.draw_rectangle_outline(SCREEN_WIDTH//2, 60, SCREEN_WIDTH-40, 120, arcade.color.BLACK, 2)

        # Botones de ataque (solo en turno del jugador)
        if self.battle_state.current_turn == 0:
            type_colors = {
                "Fuego": arcade.color.RED,
                "Agua": arcade.color.BLUE,
                "Planta": arcade.color.GREEN,
                "Eléctrico": arcade.color.YELLOW,
                "Volador": arcade.color.LIGHT_BLUE,
                "Dragón": arcade.color.PURPLE,
                "Normal": arcade.color.LIGHT_GRAY,
                "Hielo": arcade.color.CYAN,
                "Lucha": arcade.color.ORANGE,
                "Veneno": arcade.color.PURPLE,
                "Tierra": arcade.color.BROWN,
                "Psíquico": arcade.color.PINK,
                "Bicho": arcade.color.LIME,
                "Roca": arcade.color.TAN,
                "Fantasma": arcade.color.PURPLE
            }
            
            for btn in self.attack_buttons:
                color = type_colors.get(btn["type"], arcade.color.LIGHT_GRAY)
                border = arcade.color.GOLD if self.selected_attack == btn["name"] else arcade.color.BLACK
                
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
        """Barra de vida estilo Pokémon con texto"""
        # Fondo y borde
        arcade.draw_rectangle_filled(x, y, 200, 20, (40, 40, 40))
        arcade.draw_rectangle_outline(x, y, 200, 20, arcade.color.BLACK, 2)

        # Relleno
        ratio = max(0, min(1, current/maximum)) if maximum > 0 else 0
        fill_w = 196 * ratio
        fill_color = (
            arcade.color.GREEN if ratio > 0.6
            else arcade.color.YELLOW if ratio > 0.3
            else arcade.color.RED
        )
        arcade.draw_rectangle_filled(x - 98 + fill_w/2, y, fill_w, 16, fill_color)

        # Texto de PS
        hp_text = f"{current}/{maximum}"
        arcade.draw_text(
            hp_text, x, y + 14,
            arcade.color.BLACK, 12,
            anchor_x="center", anchor_y="bottom",
            font_name=self.font
        )

        # Nombre
        name_x = x + 110 if is_opponent else x - 110
        anchor = "left" if is_opponent else "right"
        
        arcade.draw_text(
            name, name_x, y + 12,
            arcade.color.BLACK, 14,
            anchor_x=anchor, anchor_y="bottom",
            font_name=self.font
        )

    def on_mouse_press(self, x, y, button, modifiers):
        """Clic en ataques en turno del jugador"""
        if button == arcade.MOUSE_BUTTON_LEFT and self.battle_state.current_turn == 0:
            for btn in self.attack_buttons:
                if abs(x - btn["x"]) < 100 and abs(y - btn["y"]) < 15:
                    self.use_attack(btn["move"])
                    break

    def use_attack(self, move: Move):
        """Turno del jugador"""
        self.message = f"¡{self.player_pokemon.name} usó {move.name}!"
        
        # Calcular efectividad para mensaje
        #self.effectiveness_message = self.battle_state.get_effectiveness_message(move, self.opponent_pokemon)
        self.effectiveness_message = get_effectivenessMessage(move, self.player_pokemon)

        # Aplicar movimiento
        print("Turno del jugador:")
        print(f"Movimiento seleccionado por el Jugador: {move.name}")
        print(f"Tipo: {move.move_type}, Poder: {move.power}")


        self.battle_state = self.battle_state.apply_action(move)
        if self.battle_state.current_turn == 1:
            arcade.schedule(self.ai_turn, 1.0)
        
        # Verificar si el combate ha terminado
        if self.battle_state.is_terminal():
            if self.battle_state.opponent_pokemon.is_fainted:
                self.message = f"¡{self.opponent_pokemon.name} fue derrotado! ¡Ganaste!"
            else:
                self.message = f"¡{self.player_pokemon.name} fue derrotado! ¡Perdiste!"
            return
        
        

    def ai_turn(self, delta_time: float):
        arcade.unschedule(self.ai_turn)
        # Seleccionar mejor movimiento con Minimax
        _, best_move = minimax(self.battle_state, depth=3)
        
        if best_move:
            self.message = f"¡{self.opponent_pokemon.name} usó {best_move.name}!"
            movimiento = Move(best_move.name, best_move.move_type, best_move.power)
            print(f"Movimiento seleccionado por IA: {movimiento.name}")
            print(f"Tipo: {movimiento.move_type}, Poder: {movimiento.power}")
            
            # Calcular efectividad para mensaje
            self.effectiveness_message = self.battle_state.get_effectiveness_message
            (movimiento, self.player_pokemon)
            
            # Aplicar movimiento
            print("Turno de IA:")
            self.battle_state = self.battle_state.apply_action(best_move)

        if self.battle_state.current_turn == 1:
            arcade.schedule(self.ai_turn, 1.0)
            
            # Verificar si el combate ha terminado
            if self.battle_state.is_terminal():
                if self.battle_state.player_pokemon.is_fainted:
                    self.message = f"¡{self.player_pokemon.name} fue derrotado! ¡Perdiste!"
                else:
                    self.message = f"¡{self.opponent_pokemon.name} fue derrotado! ¡Ganaste!"


def main():
    """Función principal"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()