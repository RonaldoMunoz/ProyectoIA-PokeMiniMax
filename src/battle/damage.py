from random import random
from .pokemon import Pokemon, Move
# Tabla de efectividad completa para primera generación (simplificada)
TYPE_EFFECTIVENESS = {
    "Normal": {"Roca": 0.5, "Fantasma": 0.0},
    "Fuego": {"Fuego": 0.5, "Agua": 0.5, "Planta": 2.0, "Hielo": 2.0, "Bicho": 2.0, "Roca": 0.5, "Dragón": 0.5},
    "Agua": {"Fuego": 2.0, "Agua": 0.5, "Planta": 0.5, "Tierra": 2.0, "Roca": 2.0, "Dragón": 0.5},
    "Planta": {"Fuego": 0.5, "Agua": 2.0, "Planta": 0.5, "Tierra": 2.0, "Volador": 0.5, "Bicho": 0.5, "Veneno": 0.5, "Roca": 2.0, "Dragón": 0.5},
    "Eléctrico": {"Agua": 2.0, "Planta": 0.5, "Eléctrico": 0.5, "Tierra": 0.0, "Volador": 2.0, "Dragón": 0.5},
    "Hielo": {"Agua": 0.5, "Planta": 2.0, "Hielo": 0.5, "Tierra": 2.0, "Volador": 2.0, "Dragón": 2.0},
    "Lucha": {"Normal": 2.0, "Hielo": 2.0, "Veneno": 0.5, "Volador": 0.5, "Psíquico": 0.5, "Bicho": 0.5, "Roca": 2.0, "Fantasma": 0.0},
    "Veneno": {"Planta": 2.0, "Veneno": 0.5, "Tierra": 0.5, "Roca": 0.5, "Fantasma": 0.5},
    "Tierra": {"Fuego": 2.0, "Planta": 0.5, "Eléctrico": 2.0, "Veneno": 2.0, "Volador": 0.0, "Bicho": 0.5, "Roca": 2.0},
    "Volador": {"Planta": 2.0, "Eléctrico": 0.5, "Lucha": 2.0, "Bicho": 2.0, "Roca": 0.5},
    "Psíquico": {"Lucha": 2.0, "Veneno": 2.0, "Psíquico": 0.5},
    "Bicho": {"Fuego": 0.5, "Planta": 2.0, "Lucha": 0.5, "Veneno": 0.5, "Volador": 0.5, "Psíquico": 2.0, "Fantasma": 0.5},
    "Roca": {"Fuego": 2.0, "Hielo": 2.0, "Lucha": 0.5, "Tierra": 0.5, "Volador": 2.0, "Bicho": 2.0},
    "Fantasma": {"Normal": 0.0, "Psíquico": 0.0, "Fantasma": 2.0},
    "Dragón": {"Dragón": 2.0}
}

def calculate_damage(move: Move, attacker: Pokemon, defender: Pokemon) -> int:
    """
    Calcula el daño de un movimiento considerando:
    - Poder base del movimiento
    - Efectividad de tipos
    - STAB (Same-Type Attack Bonus)
    """
    # 1. Determinar efectividad contra cada tipo del defensor
    effectiveness = 1.0
    for defender_type in defender.types:
        effectiveness *= TYPE_EFFECTIVENESS.get(move.move_type, {}).get(defender_type, 1.0)
    
    # 2. Aplicar STAB (Same-Type Attack Bonus)
    stab = 1.5 if move.move_type in attacker.types else 1.0
    
    # 3. Fórmula de daño simplificada (sin stats, nivel, etc.)
    base_damage = move.power
    
    # 4. Cálculo final con variación aleatoria (85-100%)
    damage = int(base_damage * effectiveness * stab * random.uniform(0.85, 1.0))
    
    # 5. Mensajes de efectividad (opcional, para depuración)
    if effectiveness > 1:
        print(f"¡{move.name} es super efectivo contra {defender.name}!")
    elif effectiveness < 1:
        print(f"{move.name} no es muy efectivo contra {defender.name}...")
    elif effectiveness == 0:
        print(f"{move.name} no afecta a {defender.name}!")
    
    return damage