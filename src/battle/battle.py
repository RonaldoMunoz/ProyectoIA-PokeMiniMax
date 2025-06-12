    from dataclasses import dataclass
    from typing import List
    from .pokemon import Pokemon, Move
    from .damage import calculate_damage

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
            # Copiar el estado actual para no modificarlo
            new_state = BattleState(
                player_pokemon=self.player_pokemon,
                opponent_pokemon=self.opponent_pokemon,
                player_team=self.player_team.copy(),
                opponent_team=self.opponent_team.copy(),
                current_turn=1 - self.current_turn  # Alternar turno
            )
            
            # Determinar atacante y defensor
            if self.current_turn == 0:  # Turno jugador
                attacker = new_state.player_pokemon
                defender = new_state.opponent_pokemon
            else:  # Turno oponente
                attacker = new_state.opponent_pokemon
                defender = new_state.player_pokemon
            
            # Calcular y aplicar daño
            damage = calculate_damage(move, attacker, defender)
            defender.take_damage(damage)
            
            # Cambiar Pokémon si es necesario (implementar lógica adicional)
            
            return new_state