import os
import json


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

    def read_pets(self) -> list[dict]:
        try:
            with open(self.penc_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Penc file not found.")
            return []
