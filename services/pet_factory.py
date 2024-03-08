from pets.pet_base import Pet
from pets.frog import Frog
from pets.turtle import Turtle


class PetFactory:
    def __init__(self, pet_name: str):
        self._pet_name = pet_name
        self._species_map = {
            "Turtle": Turtle,
            "Frog": Frog
        }

    def create(self, species: list[bool] or str) -> Pet or None:
        if isinstance(species, list):
            return self._create_from_list(species)
        elif isinstance(species, str):
            return self._create_from_string(species)
        else:
            return None

    def _create_from_string(self, species: str) -> Pet or None:
        if species in self._species_map:
            return self._species_map[species](self._pet_name)
        else:
            return None

    def _create_from_list(self, species: list[bool]) -> Pet or None:
        species_str = "Turtle" if species[0] else "Frog" if species[1] else None
        return self._create_from_string(species_str)

    @property
    def pet_name(self):
        return self._pet_name

    @pet_name.setter
    def pet_name(self, value):
        self._pet_name = value
