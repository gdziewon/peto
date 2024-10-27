import json
import os

from pets.pet_base import Pet
from services.pet_factory import PetFactory
from utils.constants import PENC_FILE_EXTENSION


class Penc:
    def __init__(self, directory: str):
        self._name = directory
        self._directory = os.path.abspath(directory)
        self._penc_file = os.path.join(self.directory, PENC_FILE_EXTENSION)

    def create_penc(self):
        """Create the directory and a JSON file to store pet data."""
        try:
            os.makedirs(self.directory, exist_ok=True)
            if not os.path.exists(self.penc_file):
                with open(self.penc_file, "w") as f:
                    json.dump([], f)
            print(f"Penc at '{self.directory}' created.")
        except Exception as e:
            print(f"Error creating penc: {e}")

    def _read_pets(self) -> list[dict]:
        """Read the list of pets from the penc file."""
        try:
            with open(self.penc_file, "r") as f:
                pet_dicts = json.load(f)
            return pet_dicts
        except FileNotFoundError:
            print("Penc file not found.")
            return []

    def _write_pets(self, pets: list[dict]):
        """Write the list of pets to the penc file."""
        try:
            with open(self.penc_file, "w") as f:
                json.dump(pets, f)
        except FileNotFoundError:
            print("Penc file not found.")
            return

    def _find_pet_index(self, pet_name: str) -> int:
        """Find the index of a pet in the list by name."""
        pets = self._read_pets()
        for i, pet in enumerate(pets):
            if pet["_name"] == pet_name:
                return i
        return -1

    def add_pet(self, pet: Pet) -> bool:
        """Add a pet to the penc if it doesn't already exist."""
        pets = self._read_pets()
        if any(pet.name == p["_name"] for p in pets):
            print(f"Pet {pet.name} already exists in penc {self.name}.")
            return False
        pets.append(pet.__dict__)
        self._write_pets(pets)
        return True

    def kill_pet(self, pet_name: str):
        """Remove a pet by name from the penc."""
        pets = self._read_pets()
        pet_index = self._find_pet_index(pet_name)
        if pet_index >= 0:
            pets.pop(pet_index)
            self._write_pets(pets)
        else:
            print(f"Pet {pet_name} not found.")

    def kill_all_pets(self):
        """Remove all pets from the penc."""
        self._write_pets([])

    def get_all_pets(self) -> list[Pet]:
        """Return a list of all pets in the penc."""
        pet_dicts = self._read_pets()
        pets = []
        for pet_dict in pet_dicts:
            pet = PetFactory(pet_dict["_name"]).create(pet_dict["_species"])
            if pet:
                pet.__dict__.update(pet_dict)
                pets.append(pet)
        return pets

    def update_pet_state(self, updated_pet: Pet):
        """Update a specific pet's state in the penc."""
        pets = self._read_pets()
        pet_index = self._find_pet_index(updated_pet.name)
        if pet_index >= 0:
            pets[pet_index] = updated_pet.__dict__
            self._write_pets(pets)
        else:
            print(f"Pet {updated_pet.name} not found.")

    def update_all_pets(self):
        """Update the state of all pets in the penc."""
        pets = self.get_all_pets()
        for pet in pets:
            pet.update()
            self.update_pet_state(pet)

    def get_pet(self, pet_name: str) -> Pet:
        """Retrieve a pet by name from the penc."""
        pets = self.get_all_pets()
        for pet in pets:
            if pet.name == pet_name:
                return pet
        print(f"Pet {pet_name} not found in penc {self.name}.")
        return None

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def directory(self):
        return self._directory

    @property
    def penc_file(self):
        return self._penc_file

    # Setters
    @name.setter
    def name(self, value):
        self._name = value

    @directory.setter
    def directory(self, value):
        self._directory = value

    @penc_file.setter
    def penc_file(self, value):
        self._penc_file = value
