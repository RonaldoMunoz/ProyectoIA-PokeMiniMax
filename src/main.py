from battle.core import Trainer, BattleState
from battle.damage import load_type_chart
from utils.loader import load_pokemon_data
from ui.cli import start_battle_ui
from ai.minimax import MinimaxAI

def main():
    # Cargar datos del juego
    type_chart = load_type_chart("data/type_chart.json")
    pokemon_data = load_pokemon_data("data/pokemon/")
    
    # Crear entrenadores
    player = Trainer("Ash")
    opponent = Trainer("Gary", is_ai=True)
    
    # Configurar equipos (con opción de selección por UI)
    player.add_pokemon(pokemon_data["charizard"])
    opponent.add_pokemon(pokemon_data["blastoise"])
    
    # Inicializar IA
    ai_engine = MinimaxAI(max_depth=3, type_chart=type_chart)
    
    # Estado inicial del combate
    battle_state = BattleState(player, opponent, current_turn=0)
    
    # Iniciar interfaz de combate
    start_battle_ui(battle_state, ai_engine, type_chart)

if __name__ == "__main__":
    main()