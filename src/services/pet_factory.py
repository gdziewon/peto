from pets.crocodile import Crocodile
from pets.frog import Frog
from pets.pet_base import Pet
from pets.turtle import Turtle


class PetFactory:
    def __init__(self, pet_name: str):
        self._pet_name = pet_name
        self._species_map = {
            "turtle": Turtle,
            "frog": Frog,
            "crocodile": Crocodile,
            "croc": Crocodile,
        }

    def create(self, species: str) -> Pet:
        species = species.lower()
        if species in self._species_map:
            return self._species_map[species](self._pet_name)
        else:
            return None

    @property
    def pet_name(self):
        return self._pet_name

    @pet_name.setter
    def pet_name(self, value):
        self._pet_name = value
