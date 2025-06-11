from typing import List, Tuple
from battle.battle import BattleState
from battle.pokemon import Move
from battle.damage import calculate_damage

def evaluate_state(state: BattleState) -> float:
    """Función heurística para evaluar un estado del combate"""
    # 1. Diferencia de PS normalizados
    player_hp_ratio = state.player_pokemon.current_hp / state.player_pokemon.max_hp
    opponent_hp_ratio = state.opponent_pokemon.current_hp / state.opponent_pokemon.max_hp
    hp_score = player_hp_ratio - opponent_hp_ratio
    
    # 2. Ventaja de tipos (mejor movimiento posible)
    best_damage = 0
    for move in state.player_pokemon.moves:
        damage = calculate_damage(move, state.player_pokemon, state.opponent_pokemon)
        best_damage = max(best_damage, damage)
    type_score = best_damage / state.opponent_pokemon.max_hp
    
    # 3. Pokémon restantes
    player_remaining = sum(1 for p in state.player_team if not p.is_fainted)
    opponent_remaining = sum(1 for p in state.opponent_team if not p.is_fainted)
    remaining_score = player_remaining - opponent_remaining
    
    # Ponderación de factores
    return (hp_score * 0.6) + (type_score * 0.3) + (remaining_score * 0.1)

def minimax(
    state: BattleState, 
    depth: int, 
    alpha: float = -float('inf'), 
    beta: float = float('inf'),
    maximizing_player: bool = True
) -> Tuple[float, Move]:
    """Algoritmo Minimax con poda alfa-beta"""
    if depth == 0 or state.is_terminal():
        return evaluate_state(state), None
    
    legal_moves = state.get_legal_actions()
    if not legal_moves:
        return evaluate_state(state), None
    
    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in legal_moves:
            new_state = state.apply_action(move)
            evaluation, _ = minimax(new_state, depth-1, alpha, beta, False)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in legal_moves:
            new_state = state.apply_action(move)
            evaluation, _ = minimax(new_state, depth-1, alpha, beta, True)
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval, best_move