from typing import Optional, Tuple
from ..battle.battle import BattleState
from ..battle.pokemon import Move
from ..battle.damage import calculate_damage

def evaluate_state(state: BattleState) -> float:
    """
    Heurística compuesta por:
      1) Diferencia de HP normalizados.
      2) Potencial de daño (mejor ataque / HP oponente).
      3) Pokémon restantes (propios - oponente).
    """
    # 1) HP
    p_ratio = state.player_pokemon.current_hp / state.player_pokemon.max_hp
    o_ratio = state.opponent_pokemon.current_hp / state.opponent_pokemon.max_hp
    hp_score = p_ratio - o_ratio

    # 2) Mejor daño posible
    best = max(
        calculate_damage(m, state.player_pokemon, state.opponent_pokemon)
        for m in state.player_pokemon.moves
    )
    type_score = best / state.opponent_pokemon.max_hp

    # 3) Pokémon restantes
    alive_player   = sum(not p.is_fainted for p in state.player_team)
    alive_opponent = sum(not p.is_fainted for p in state.opponent_team)
    remaining_score = alive_player - alive_opponent

    return hp_score * 0.6 + type_score * 0.3 + remaining_score * 0.1


def minimax(
    state: BattleState,
    depth: int,
    alpha: float = float("-inf"),
    beta:  float = float("inf"),
    maximizing: bool = True
) -> Tuple[float, Optional[Move]]:
    """
    Minimax con poda alfa-beta.
    Retorna (mejor_evaluacion, mejor_movimiento).
    """
    # Caso base
    if depth == 0 or state.is_terminal():
        return evaluate_state(state), None

    moves = state.get_legal_actions()
    if not moves:
        return evaluate_state(state), None

    best_move: Optional[Move] = None

    if maximizing:
        value = float("-inf")
        for move in moves:
            score, _ = minimax(state.apply_action(move), depth - 1, alpha, beta, False)
            if score > value:
                value, best_move = score, move
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # poda β
        return value, best_move

    else:
        value = float("inf")
        for move in moves:
            score, _ = minimax(state.apply_action(move), depth - 1, alpha, beta, True)
            if score < value:
                value, best_move = score, move
            beta = min(beta, value)
            if beta <= alpha:
                break  # poda α
        return value, best_move
