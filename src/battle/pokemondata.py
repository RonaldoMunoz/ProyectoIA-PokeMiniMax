# pokemondata.py

POKEMON_DATA = {
    "Pikachu": {
        "types": ["Electric"],
        "hp": 50,
        "moves": [
            {"name": "Impactrueno", "type": "Electric", "power": 40},
            {"name": "Ataque Rápido", "type": "Normal", "power": 30},
            {"name": "Rayo", "type": "Electric", "power": 90},
        ]
    },
    "Charmander": {
        "types": ["Fire"],
        "hp": 65,
        "moves": [
            {"name": "Ascuas", "type": "Fire", "power": 40},
            {"name": "Arañazo", "type": "Normal", "power": 30},
        ]
    },
    "Bulbasaur": {
        "types": ["Grass", "Poison"],
        "hp": 68,
        "moves": [
            {"name": "Látigo Cepa", "type": "Grass", "power": 45},
            {"name": "Placaje", "type": "Normal", "power": 30},
        ]
    },
    "Squirtle": {
        "types": ["Water"],
        "hp": 66,
        "moves": [
            {"name": "Pistola Agua", "type": "Water", "power": 40},
            {"name": "Paclaje", "type": "Normal", "power": 30},
        ]
    },
    "Charizard": {
        "types": ["Fire", "Flying"],
        "hp": 78,
        "moves": [
            {"name": "Lanzallamas", "type": "Fire", "power": 90},
            {"name": "Garra Dragón", "type": "Dragon", "power": 80},
            {"name": "Giro Fuego", "type": "Fire", "power": 60},
            {"name": "Tajo Aéreo", "type": "Flying", "power": 75},
        ]
    },
    "Blastoise": {
        "types": ["Water"],
        "hp": 79,
        "moves": [
            {"name": "Hidrobomba", "type": "Water", "power": 110},
            {"name": "Rayo Hielo", "type": "Ice", "power": 90},
            {"name": "Cabezazo", "type": "Normal", "power": 70},
            {"name": "Pistola Agua", "type": "Water", "power": 40},
        ]
    },
    "Meowth": {
        "types": ["Normal"],
        "hp": 50,
        "moves": [
            {"name": "Arañazo", "type": "Normal", "power": 30},
            {"name": "Mordisco", "type": "Dark", "power": 60},
            {"name": "Día de Pago", "type": "Normal", "power": 40},
        ]
    },
}
