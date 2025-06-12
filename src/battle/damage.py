import random
from .pokemon import Pokemon, Move

# Tabla de efectividad completa (1ª gen.)
TYPE_EFFECTIVENESS = {
    "Normal":    {"Roca": 0.5,  "Fantasma": 0.0},
    "Fuego":     {"Fuego": 0.5, "Agua": 0.5, "Planta": 2.0, "Hielo": 2.0,
                  "Bicho": 2.0, "Roca": 0.5, "Dragón": 0.5},
    "Agua":      {"Fuego": 2.0, "Agua": 0.5, "Planta": 0.5,
                  "Tierra": 2.0, "Roca": 2.0, "Dragón": 0.5},
    # …etc para todos los tipos…
    "Dragón":    {"Dragón": 2.0}
}

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

    # 6) Mensajes de efectividad
    if effectiveness == 0:
        print(f"{move.name} no afecta a {defender.name}!")
    elif effectiveness > 1:
        print(f"¡{move.name} es super efectivo contra {defender.name}!")
    elif effectiveness < 1:
        print(f"{move.name} no es muy efectivo contra {defender.name}…")

    return damage
