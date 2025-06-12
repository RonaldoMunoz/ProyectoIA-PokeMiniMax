from dataclasses import dataclass
from typing import List
from src.battle.pokemondata import POKEMON_DATA

@dataclass
class Move:
    """Representa un ataque Pokémon"""
    name: str
    move_type: str
    power: int

class Pokemon:
    """Representa un Pokémon con sus atributos"""
    def __init__(self, name: str, types: List[str], hp: int, moves: List[Move]):
        self.name = name
        self.types = types
        self.max_hp = hp
        self.current_hp = hp
        self.moves = moves
        self.is_fainted = False
    
    def take_damage(self, damage: int):
        """Reduce los PS del Pokémon"""
        self.current_hp = max(0, self.current_hp - damage)
        if self.current_hp == 0:
            self.is_fainted = True
    
    
    def __str__(self):
        return f"{self.name} ({'/'.join(self.types)}) - PS: {self.current_hp}/{self.max_hp}"
def create_pokemon(name: str) -> Pokemon:
    data = POKEMON_DATA.get(name)
    if not data:
        raise ValueError(f"No se encontró el Pokémon '{name}' en los datos.")
    
    moves = [Move(m["name"], m["type"], m["power"]) for m in data["moves"]]
    return Pokemon(name=name, types=data["types"], hp=data["hp"], moves=moves)
def get_all_pokemon_names():
    return list(POKEMON_DATA.keys())
