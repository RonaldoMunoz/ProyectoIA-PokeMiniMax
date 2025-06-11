from dataclasses import dataclass
from typing import List

@dataclass
class Move:
    """Representa un ataque Pokémon"""
    name: str
    move_type: str
    power: int
    accuracy: int = 100  # Para futuras expansiones

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
    
    def has_usable_move(self) -> bool:
        """Verifica si tiene al menos un movimiento usable"""
        return len(self.moves) > 0
    
    def __str__(self):
        return f"{self.name} ({'/'.join(self.types)}) - PS: {self.current_hp}/{self.max_hp}"