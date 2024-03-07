import os
import json
from pets.pet import Pet
from pets.frog import Frog
from pets.tortoise import Tortoise


class Penc:
    def __init__(self, directory: str):
        self.directory = os.path.abspath(directory)
        self.penc_file = os.path.join(self.directory, ".penc")

    def create(self) -> None:
        try:
            os.makedirs(self.directory, exist_ok=True)
            if not os.path.exists(self.penc_file):
                with open(self.penc_file, 'w') as f:
                    json.dump([], f)
            print(f"Penc at '{self.directory}' created.")
        except Exception as e:
            print(f"Error creating penc: {e}")

    def add_pet(self, pet) -> None:
        pets = self.read_pets()
        pets.append(pet.__dict__)
        with open(self.penc_file, 'w') as f:
            json.dump(pets, f)

    def get_pets(self) -> list[Pet]:
        try:
            pet_dicts = self.read_pets()
            pets = []
            for pet_dict in pet_dicts:
                pet_type = pet_dict.get('type', 'Pet')
                if pet_type == 'Tortoise':
                    pet = Tortoise(pet_dict['name'])
                elif pet_type == 'Frog':
                    pet = Frog(pet_dict['name'])
                else:
                    pet = Pet(pet_dict['name'])
                pet.__dict__.update(pet_dict)
                pets.append(pet)
            return pets
        except FileNotFoundError:
            print("Penc file not found.")
            return []

    def read_pets(self) -> list[dict]:
        try:
            with open(self.penc_file, 'r') as f:
                pet_dicts = json.load(f)
            return pet_dicts
        except FileNotFoundError:
            print("Penc file not found.")
            return []

    def update_pet(self, updated_pet: Pet) -> None:
        pets = self.read_pets()
        for i, pet in enumerate(pets):
            if pet['name'] == updated_pet.name:
                pets[i] = updated_pet.__dict__
                break
        else:
            print(f"Pet {updated_pet.name} not found.")
            return
        with open(self.penc_file, 'w') as f:
            json.dump(pets, f)

    def get_pet(self, name) -> Pet or None:
        pets = self.get_pets()
        for pet in pets:
            if pet.name == name:
                return pet
        print(f"Pet {name} not found in penc")
        return None
