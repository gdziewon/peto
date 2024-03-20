import os
import json
from pets.pet_base import Pet
from services.pet_factory import PetFactory
from utils.constants import PENC_FILE_EXTENSION


class Penc:
    def __init__(self, directory: str):
        self._name = directory
        self._directory = os.path.abspath(directory)
        self._penc_file = os.path.join(self.directory, PENC_FILE_EXTENSION)

    def create_penc(self):
        try:
            os.makedirs(self.directory, exist_ok=True)
            if not os.path.exists(self.penc_file):
                with open(self.penc_file, 'w') as f:
                    json.dump([], f)
            print(f"Penc at '{self.directory}' created.")
        except Exception as e:
            print(f"Error creating penc: {e}")

    def _read_pets(self) -> list[dict]:
        try:
            with open(self.penc_file, 'r') as f:
                pet_dicts = json.load(f)
            return pet_dicts
        except FileNotFoundError:
            print("Penc file not found.")
            return []

    def _write_pets(self, pets: list[dict]):
        try:
            with open(self.penc_file, 'w') as f:
                json.dump(pets, f)
        except FileNotFoundError:
            print("Penc file not found.")
            return

    def add_pet(self, pet: Pet) -> bool:
        pets = self._read_pets()
        if any(pet.name == p["_name"] for p in pets):
            print(f"Pet {pet.name} already exists in penc {self.name}.")
            return False
        pets.append(pet.__dict__)
        self._write_pets(pets)
        return True

    def kill_pet(self, pet_name: str):
        pets = self._read_pets()
        for i, pet in enumerate(pets):
            if pet['_name'] == pet_name:
                pets.pop(i)
                break
        else:
            print(f"Pet {pet_name} not found.")
            return
        self._write_pets(pets)

    def get_all_pets(self) -> list[Pet]:
        try:
            pet_dicts = self._read_pets()
            pets = []
            for pet_dict in pet_dicts:
                pet = PetFactory(pet_dict['_name']).create(pet_dict['_species'])
                if pet:
                    pet.__dict__.update(pet_dict)
                    pets.append(pet)
            return pets
        except FileNotFoundError:
            print("Penc file not found.")
            return []

    def update_pet_state(self, updated_pet: Pet):
        pets = self._read_pets()
        for i, pet in enumerate(pets):
            if pet['_name'] == updated_pet.name:
                pets[i] = updated_pet.__dict__
                break
        else:
            print(f"Pet {updated_pet.name} not found.")
            return
        self._write_pets(pets)

    def get_pet(self, pet_name: str) -> Pet or None:
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
