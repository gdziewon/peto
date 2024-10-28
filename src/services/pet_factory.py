from pathlib import Path
from typing import Optional

from pets.crocodile import Crocodile
from pets.frog import Frog
from pets.pet_base import Pet
from pets.turtle import Turtle


class PetFactory:
    _species_map = {
        "turtle": Turtle,
        "frog": Frog,
        "crocodile": Crocodile,
        "croc": Crocodile,
    }

    def __init__(self):
        pass

    def create(self, pet_name: str, species: str, directory: Path) -> Optional[Pet]:
        species = species.lower()
        pet_class = self._species_map.get(species)
        if pet_class:
            return pet_class(pet_name, directory)
        return None
