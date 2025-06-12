import random
from .pokemon import Pokemon, Move

# Tabla de efectividad completa (1ª gen.)
TYPE_EFFECTIVENESS = {
    "Normal": {
        "Rock": 0.5,
        "Ghost": 0.0,
    },
    "Fire": {
        "Fire": 0.5,  "Water": 0.5,  "Grass": 2.0,  "Ice": 2.0,
        "Bug": 2.0,   "Rock": 0.5,   "Dragon": 0.5,
    },
    "Water": {
        "Fire": 2.0,  "Water": 0.5,  "Grass": 0.5,
        "Ground": 2.0, "Rock": 2.0,  "Dragon": 0.5,
    },
    "Electric": {
        "Water": 2.0,   "Electric": 0.5, "Grass": 0.5,
        "Ground": 0.0,  "Flying": 2.0,  "Dragon": 0.5,
    },
    "Grass": {
        "Water": 2.0,  "Fire": 0.5,   "Grass": 0.5,
        "Poison": 0.5, "Ground": 2.0, "Flying": 0.5,
        "Bug": 0.5,    "Rock": 2.0,   "Dragon": 0.5,
    },
    "Ice": {
        "Grass": 2.0,  "Fire": 0.5,  "Water": 0.5,
        "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0,
    },
    "Fighting": {
        "Normal": 2.0, "Ice": 2.0,    "Rock": 2.0,
        "Dark": 2.0,   "Ghost": 0.0,
    },
    "Poison": {
        "Grass": 2.0,  "Poison": 0.5, "Ground": 0.5,
        "Rock": 0.5,   "Ghost": 0.5,
    },
    "Ground": {
        "Fire": 2.0,   "Electric": 2.0, "Grass": 0.5,
        "Poison": 2.0, "Flying": 0.0,   "Bug": 0.5,
        "Rock": 2.0,
    },
    "Flying": {
        "Grass": 2.0,   "Electric": 0.5, "Fighting": 2.0,
        "Bug": 2.0,     "Rock": 0.5,
    },
    "Psychic": {
        "Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5,
    },
    "Bug": {
        "Grass": 2.0,   "Fire": 0.5,    "Fighting": 0.5,
        "Poison": 0.5,  "Flying": 0.5,   "Psychic": 2.0,
        "Ghost": 0.5,
    },
    "Rock": {
        "Fire": 2.0,    "Ice": 2.0,     "Fighting": 0.5,
        "Ground": 0.5,  "Flying": 2.0,  "Bug": 2.0,
    },
    "Ghost": {
        "Normal": 0.0,  "Psychic": 0.0, "Ghost": 2.0,
    },
    "Dragon": {
        "Dragon": 2.0,
    },
    "Dark": {
        "Psychic": 2.0, "Ghost": 0.5,  "Dark": 0.5,
    },
}

#obtener el mensaje de efectividad de un movimiento
def get_effectivenessMessage(move: Move, defender: Pokemon) -> str:
    """
    Obtiene un mensaje de efectividad del movimiento contra el defensor.
    """
    effectiveness = 1.0
    for t in defender.types:
        effectiveness *= TYPE_EFFECTIVENESS.get(move.move_type, {}).get(t, 1.0)

    if effectiveness == 0:
        return f"{move.name} no afecta a {defender.name}!"
    elif effectiveness > 1:
        return f"¡{move.name} es super efectivo contra {defender.name}!"
    elif effectiveness < 1:
        return f"{move.name} no es muy efectivo contra {defender.name}…"
    else:
        return f"{move.name} tiene un efecto normal contra {defender.name}."
    

def calculate_damage(move: Move, attacker: Pokemon, defender: Pokemon) -> int:
    """
    Calcula daño teniendo en cuenta:
      - poder base del movimiento
      - efectividad (incluye inmunidad: 0.0)
      - STAB (1.5 si coincide tipo)
      - variación aleatoria (0.85–1.0)
    """
    # 1) Efectividad contra cada tipo del defensor
    effectiveness = 1.0
    for t in defender.types:
        effectiveness *= TYPE_EFFECTIVENESS.get(move.move_type, {}).get(t, 1.0)

    # 2) STAB
    stab = 1.5 if move.move_type in attacker.types else 1.0

    # 3) Daño base
    base = move.power

    # 4) Variación aleatoria
    variation = random.uniform(0.85, 1.0)

    # 5) Cálculo final
    damage = int(base * effectiveness * stab * variation)
    
    return damage
