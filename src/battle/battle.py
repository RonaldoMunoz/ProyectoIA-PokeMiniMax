from dataclasses import dataclass
from typing import List
from .pokemon import Pokemon, Move
from .damage import calculate_damage
import copy

@dataclass
class BattleState:
    """Representa el estado actual del combate"""
    player_pokemon: Pokemon
    opponent_pokemon: Pokemon
    player_team: List[Pokemon]
    opponent_team: List[Pokemon]
    current_turn: int  # 0: jugador, 1: oponente
    
    def is_terminal(self) -> bool:
        """Determina si el combate ha terminado"""
        return (self.player_pokemon.is_fainted and 
                not any(not p.is_fainted for p in self.player_team)) or \
               (self.opponent_pokemon.is_fainted and 
                not any(not p.is_fainted for p in self.opponent_team))
    
    def get_legal_actions(self) -> List[Move]:
        """Obtiene movimientos legales para el Pokémon activo"""
        current_pokemon = self.player_pokemon if self.current_turn == 0 else self.opponent_pokemon
        return [move for move in current_pokemon.moves if move.power > 0]
    


    def apply_action(self, move: Move) -> 'BattleState':
        """Aplica un movimiento y genera nuevo estado"""
        # Clonamos TODO: estado y Pokémon
        new_player = copy.deepcopy(self.player_pokemon)
        new_opp    = copy.deepcopy(self.opponent_pokemon)
        new_state = BattleState(
            player_pokemon=new_player,
            opponent_pokemon=new_opp,
            player_team=[copy.deepcopy(p) for p in self.player_team],
            opponent_team=[copy.deepcopy(p) for p in self.opponent_team],
            current_turn=1 - self.current_turn
        )

        # Determinar atacante y defensor en el CLON
        if self.current_turn == 0:
            attacker = new_state.player_pokemon
            defender = new_state.opponent_pokemon
        else:
            attacker = new_state.opponent_pokemon
            defender = new_state.player_pokemon

        # Calcular y aplicar daño sobre el CLON
        damage = calculate_damage(move, attacker, defender)
        defender.take_damage(damage)

        return new_state


    #obtener mensaje de efectividad
    def get_effectiveness_message(self, move: Move) -> str:
        """
        Obtiene un mensaje de efectividad del movimiento contra el Pokémon defensor.
        """
        defender = self.opponent_pokemon if self.current_turn == 0 else self.player_pokemon
        return defender.get_effectiveness_message(move)