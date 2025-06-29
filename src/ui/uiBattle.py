import arcade
import os
import random
import sys
from pathlib import Path
from ..battle.pokemon import Pokemon, Move, create_pokemon, get_all_pokemon_names
from ..ai.pokeminimax import minimax
from ..battle.damage import get_effectivenessMessage, calculate_damage
from ..battle.battle import BattleState

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))



# Configuración de la ventana
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
SCREEN_TITLE = "Pokeminmax"
# Factores de escala
PLAYER_SCALE   = 1.6
OPPONENT_SCALE = 1.6

# Ruta a assets
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")

def stop_current_music(window):
    """Detiene la música actual si está sonando."""
    if hasattr(window, "music_player") and window.music_player is not None:
        arcade.stop_sound(window.music_player)
        window.music_player = None


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.button_rect = None
        self.button_color = arcade.color.YELLOW
        self.button_hover_color = arcade.color.GOLD
        self.current_button_color = self.button_color
        self.window.music_player = None


    def on_show(self):
        # Cargar fondo
        background_path = os.path.join(ASSETS_PATH, "backgrounds", "fondomenu.jpg")
        if os.path.exists(background_path):
            self.background = arcade.load_texture(background_path)

        # Cargar música
        music_path = os.path.join(ASSETS_PATH, "music", "pokemonmusic.wav")
        if os.path.exists(music_path): 
            self.menu_music = arcade.load_sound(music_path)
            self.window.music_player = self.menu_music.play(loop=True)

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
        self.font_name = None
        self.pokemon_options = []


    def on_show(self):
        # Cargar fondo
        background_path = os.path.join(ASSETS_PATH, "backgrounds", "fondo2.jpg")
        if os.path.exists(background_path):
            self.background = arcade.load_texture(background_path)
        self.font_name = "Pokemon Solid"
        font_path = os.path.join(ASSETS_PATH, "fonts", "Pokemon_Solid.ttf")
        arcade.load_font(font_path)

        # Obtener nombres de Pokémon dinámicamente
        all_names = get_all_pokemon_names()

        # Crear botones en cuadrícula
        self.pokemon_options.clear()
        cols = 3
        spacing_x = 180
        spacing_y = 120
        start_x = 250
        start_y = SCREEN_HEIGHT // 2 + 50

        for i, name in enumerate(all_names):
            col = i % cols
            row = i // cols
            x = start_x + col * spacing_x
            y = start_y - row * spacing_y
            self.pokemon_options.append((name, (x, y), (200, 100)))  # (nombre, posición, tamaño)

    def on_draw(self):
        self.clear()

        # Dibujar fondo
        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        else:
            arcade.set_background_color(arcade.color.LIGHT_BLUE)


        # Título
        arcade.draw_text("ELIGE TU POKEMON", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 250,
                         arcade.color.VIOLET, 40, font_name=self.font_name, anchor_x="center")


        # Dibujar opciones
        for name, (x, y), (w, h) in self.pokemon_options:
            arcade.draw_rectangle_filled(x, y, w, h, arcade.color.VIOLET)
            arcade.draw_text(name, x, y, arcade.color.WHITE, 20,
                             anchor_x="center", anchor_y="center", font_name=self.font_name)

    def on_mouse_press(self, x, y, button, modifiers):
        for name, (bx, by), (bw, bh) in self.pokemon_options:
            if bx - bw / 2 < x < bx + bw / 2 and by - bh / 2 < y < by + bh / 2:
                selected_pokemon = create_pokemon(name)
                battle_view = PokemonBattleUI(selected_pokemon)
                self.window.show_view(battle_view)
                break


class PokemonBattleUI(arcade.View):
    def __init__(self, selected_pokemon: Pokemon):
        super().__init__()
        self.player_pokemon = selected_pokemon
        possible_opponents = [name for name in get_all_pokemon_names() if name != selected_pokemon.name]
        opponent_name = random.choice(possible_opponents)
        self.opponent_pokemon = create_pokemon(opponent_name)
        self.last_attack_info = ""  # <-- aquí almacenaremos el log
        self.effectiveness_message = ""  # Mensaje de efectividad del ataque
        self.battle_state = BattleState(
            player_pokemon=self.player_pokemon,
            opponent_pokemon=self.opponent_pokemon,
            player_team=[self.player_pokemon],
            opponent_team=[self.opponent_pokemon],
            current_turn=0  
        )
        
        self.message = "¡Comienza el combate!"
        self.effectiveness_message = ""
        self.attack_buttons = []
        self.selected_attack = None
        self.font = None
        self.background = None
        self.player_sprite = None
        self.opponent_sprite = None
        self.battle_over = False
        self.result = None  # "win" o "lose"
        self.log_time = 0.0
        self.LOG_DURATION = 5.0 


        # Fuente y fondo
        font_path = os.path.join(ASSETS_PATH, "fonts", "pokemon.ttf")
        if os.path.exists(font_path):
            arcade.load_font(font_path)
            self.font = "pokemon.ttf"

        bg_path = os.path.join(ASSETS_PATH, "backgrounds", "backgroundBattle.png")
        if os.path.exists(bg_path):
            self.background = arcade.load_texture(bg_path)

        self.setup()
    
    def on_update(self, delta_time: float):
        # Reducir el temporizador
        if self.log_time > 0:
            self.log_time -= delta_time
            if self.log_time <= 0:
                # Cuando se acabe, limpiamos los mensajes
                self.last_attack_info = ""
                self.effectiveness_message = ""

    def setup(self):
        player_path = os.path.join(ASSETS_PATH, "pokemon", f"{self.player_pokemon.name}.png")

        if os.path.exists(player_path):
            self.player_sprite = arcade.Sprite(player_path, scale=PLAYER_SCALE)
            self.player_sprite.center_x = 200
            self.player_sprite.center_y = 160
        opp_path = os.path.join(ASSETS_PATH, "pokemon", f"{self.opponent_pokemon.name}.png")
        if os.path.exists(opp_path):
            self.opponent_sprite = arcade.Sprite(opp_path, scale=OPPONENT_SCALE)
            self.opponent_sprite.center_x = 600
            self.opponent_sprite.center_y = 450


        attacks = self.player_pokemon.moves
        positions = [(200, 80), (450, 80), (200, 40), (450, 40)]

        self.attack_buttons = []
        for attack, (x, y) in zip(attacks, positions):
            button = {
                "name": attack.name,
                "move": attack,
                "x": x,
                "y": y
            }
            self.attack_buttons.append(button)

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
            self.battle_state.opponent_pokemon.name,
            is_opponent=True
        )
        
        self.draw_health_bar(
            200, 220,
            self.battle_state.player_pokemon.current_hp,
            self.battle_state.player_pokemon.max_hp,
            self.battle_state.player_pokemon.name,
            is_opponent=False
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
            "Fire": arcade.color.RED,
            "Water": arcade.color.BLUE,
            "Grass": arcade.color.GREEN,
            "Eletric": arcade.color.YELLOW,
            "Flying": arcade.color.LIGHT_BLUE,
            "Dragon": arcade.color.PURPLE,
            "Normal": arcade.color.LIGHT_GRAY
        }
        for btn in self.attack_buttons:
            color = type_colors.get(btn["move"].move_type, arcade.color.LIGHT_GRAY)
            move = btn["move"]
            border = (arcade.color.GOLD if self.selected_attack == move.name else arcade.color.BLACK)
            arcade.draw_rectangle_filled(btn["x"], btn["y"], 200, 30, color)
            arcade.draw_rectangle_outline(btn["x"], btn["y"], 200, 30, border, 2)
            arcade.draw_text(
            move.name,
            btn["x"], btn["y"],
            arcade.color.BLACK, 14,
            anchor_x="center", anchor_y="center",
            font_name=self.font
            )
        # 2) Finalmente, el “log” tipo Game Boy debajo:

        if self.log_time > 0:
            log_width, log_height = 300, 80
            # margen derecho e inferior
            margin = 12
            log_x = SCREEN_WIDTH - log_width/2 - margin
            log_y = log_height/2 + margin

            # Fondo semitransparente
            arcade.draw_rectangle_filled(
                log_x, log_y,
                log_width, log_height,
                (*arcade.color.BLACK[:3], 180)
            )

            padding = 8
            text_x = log_x - log_width/2 + padding
            # alineamos la primera línea arriba dentro del recuadro
            text_y = log_y + log_height/2 - padding - 2

            # Línea 1: daño y tipo
            arcade.draw_text(
                self.last_attack_info,
                text_x, text_y,
                arcade.color.WHITE, 10,
                width=log_width - 2*padding,
                align="left",
                font_name=self.font
            )

            # Línea 2: efectividad
            arcade.draw_text(
                self.effectiveness_message,
                text_x, text_y - 18,
                arcade.color.LIGHT_GRAY, 8,
                width=log_width - 2*padding,
                align="left",
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
        # Si el combate terminó, no hacer nada
        if self.battle_state.is_terminal() or self.battle_state.player_pokemon.is_fainted or self.battle_state.opponent_pokemon.is_fainted:
            return

        # Sólo procesar clics si es turno del jugador
        if button == arcade.MOUSE_BUTTON_LEFT and self.battle_state.current_turn == 0:
            for btn in self.attack_buttons:
                if abs(x - btn["x"]) < 100 and abs(y - btn["y"]) < 15:
                    self.use_attack(btn["move"])
                    break

    def use_attack(self, move: Move):
        """Turno del jugador"""
        self.message = f"¡{self.player_pokemon.name} usó {move.name}!"
        #self.message = f"¡{self.player_pokemon.name} usó {attack['name']}!"
        # Calcular efectividad para mensaje
        damage = calculate_damage(move, self.player_pokemon, self.opponent_pokemon)
        self.last_attack_info = f"{move.name} ({move.move_type}) hizo {damage} pts."
        self.effectiveness_message = get_effectivenessMessage(move, self.opponent_pokemon)
        self.log_time = self.LOG_DURATION

        #base = attack["move"].power
        # Aplicar movimiento
        print("Turno del jugador:")
        print(f"Movimiento seleccionado por el Jugador: {move.name}")
        print(f"Tipo: {move.move_type}, Poder: {move.power}")
        
        self.battle_state = self.battle_state.apply_action(move)
        
        if self.battle_state.current_turn == 1:
            arcade.schedule(self.ai_turn, 2.0)
        
        # Verificar si el combate ha terminado
        if self.battle_state.is_terminal() or self.battle_state.player_pokemon.is_fainted or self.battle_state.opponent_pokemon.is_fainted:
            arcade.unschedule(self.ai_turn)
            self.battle_over = True

            if self.battle_state.opponent_pokemon.is_fainted:
                self.message = f"¡{self.opponent_pokemon.name} fue derrotado!"
                self.result = "Ganaste"
            else:
                self.message = f"¡{self.player_pokemon.name} fue derrotado!"
                self.result = "Perdiste"

            # Esperar 2 segundos antes de mostrar el resultado
            arcade.schedule(self.show_result, 2.0)
            return


    def ai_turn(self, delta_time: float):
        arcade.unschedule(self.ai_turn)
        # Seleccionar mejor movimiento con Minimax
        _, best_move = minimax(self.battle_state, depth=3, maximizing=False)
        
        if best_move:
            damage = calculate_damage(best_move, self.opponent_pokemon, self.player_pokemon)
            self.last_attack_info = f"{best_move.name} ({best_move.move_type}) hizo {damage} pts."
            self.message = f"¡{self.opponent_pokemon.name} usó {best_move.name}!"
            movimiento = Move(best_move.name, best_move.move_type, best_move.power)
            print(f"Movimiento seleccionado por IA: {movimiento.name}")
            print(f"Tipo: {movimiento.move_type}, Poder: {movimiento.power}")
            
            # Calcular efectividad para mensaje
            self.effectiveness_message = get_effectivenessMessage(best_move, self.player_pokemon)
            self.log_time = self.LOG_DURATION

            # Aplicar movimiento
            print("Turno de IA:")
            self.battle_state = self.battle_state.apply_action(best_move)

            
            # Verificar si el combate ha terminado
        if self.battle_state.is_terminal() or self.battle_state.player_pokemon.is_fainted or self.battle_state.opponent_pokemon.is_fainted:
            arcade.unschedule(self.ai_turn)
            self.battle_over = True

            if self.battle_state.player_pokemon.is_fainted:
                self.message = f"¡{self.player_pokemon.name} fue derrotado!"
                self.result = "Perdiste"
            else:
                self.message = f"¡{self.opponent_pokemon.name} fue derrotado!"
                self.result = "Ganaste"

            # Esperar 2 segundos antes de mostrar el resultado
            arcade.schedule(self.show_result, 2.0)
            return


    def show_result(self, delta_time):
        arcade.unschedule(self.show_result)
        result_view = BattleResultView(self.result)
        self.window.show_view(result_view)

class BattleResultView(arcade.View):
    def __init__(self, result: str):
        super().__init__()
        self.result = result
        self.background = None
        self.font = None

        # Cargar fondo
        bg_path = os.path.join(ASSETS_PATH, "backgrounds", "final2.jpg")
        if os.path.exists(bg_path):
            self.background = arcade.load_texture(bg_path)

        # Cargar fuente
        font_path = os.path.join(ASSETS_PATH, "fonts", "Pokemon_Solid.ttf")
        arcade.load_font(font_path)
        self.font = "Pokemon Solid"

        font_path = os.path.join(ASSETS_PATH, "fonts", "Pokemon Hollow.ttf")
        arcade.load_font(font_path)
        self.font2 = "Pokemon Hollow"

    def on_draw(self):
        self.clear()

        if self.background:
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        color = arcade.color.GREEN if "Ganaste" in self.result else arcade.color.RED
        arcade.draw_text(self.result, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100,
                         color, 70, anchor_x="center", font_name=self.font)

        # Botón "Volver a jugar"
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, 250, 50, arcade.color.YELLOW)
        arcade.draw_text("Volver a jugar", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60,
                         arcade.color.BLACK, 20, anchor_x="center", font_name=self.font2)

        # Botón "Salir"
        arcade.draw_rectangle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120, 250, 50, arcade.color.LIGHT_GRAY)
        arcade.draw_text("Salir del juego", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130,
                         arcade.color.BLACK, 20, anchor_x="center", font_name=self.font2)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            # "Volver a jugar"
            if SCREEN_WIDTH // 2 - 125 < x < SCREEN_WIDTH // 2 + 125 and SCREEN_HEIGHT // 2 - 75 < y < SCREEN_HEIGHT // 2 - 25:
                stop_current_music(self.window)
                menu_view = MainMenuView()
                self.window.show_view(menu_view)

            # "Salir"
            elif SCREEN_WIDTH // 2 - 125 < x < SCREEN_WIDTH // 2 + 125 and SCREEN_HEIGHT // 2 - 145 < y < SCREEN_HEIGHT // 2 - 95:
                arcade.close_window()




def main():
    """Función principal"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()