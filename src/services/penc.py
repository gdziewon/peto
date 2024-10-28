import json
from pathlib import Path
from typing import Optional

from pets.pet_base import Pet
from services.pet_factory import PetFactory
from utils.constants import PENC_FILE_EXTENSION


class Penc:
    def __init__(self, directory: Path):
        self.name = directory.name
        self.directory = directory.resolve()
        self.penc_file = self.directory / PENC_FILE_EXTENSION

    def create_penc(self) -> bool:
        """Create the directory and a JSON file to store pet data."""
        try:
            self.directory.mkdir(parents=True, exist_ok=True)
            if not self.penc_file.exists():
                self.penc_file.write_text("[]")
            return True
        except Exception:
            return False

    def _read_pets(self) -> list[dict]:
        """Read the list of pets from the penc file."""
        try:
            return json.loads(self.penc_file.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_pets(self, pets: list[dict]) -> bool:
        """Write the list of pets to the penc file."""
        try:
            self.penc_file.write_text(json.dumps(pets))
            return True
        except (FileNotFoundError, OSError):
            return False

    def _find_pet_index(self, pet_name: str) -> int:
        """Find the index of a pet in the list by name."""
        pets = self._read_pets()
        return next((i for i, pet in enumerate(pets) if pet["_name"] == pet_name), -1)

    def add_pet(self, pet: Pet) -> bool:
        """Add a pet to the penc if it doesn't already exist."""
        pets = self._read_pets()
        pet_data = pet.__dict__.copy()
        pet_data.pop("body")
        pet_data.pop("file")
        pets.append(pet_data)
        if self._write_pets(pets):
            pet.save_art()
            return True
        return False

    def kill_pet(self, pet_name: str) -> bool:
        """Remove a pet by name from the penc."""
        pets = self._read_pets()
        pet_index = self._find_pet_index(pet_name)
        if pet_index >= 0:
            pets.pop(pet_index)
            return self._write_pets(pets)
        return False

    def kill_all_pets(self) -> bool:
        """Remove all pets from the penc."""
        return self._write_pets([])

    def get_all_pets(self) -> list[Optional[Pet]]:
        """Return a list of all pets in the penc."""
        pet_dicts = self._read_pets()
        pets = []
        for pet_dict in pet_dicts:
            pet = PetFactory().create(
                pet_dict["_name"], pet_dict["species"], self.directory
            )
            if pet:
                pet.__dict__.update(pet_dict)
                pets.append(pet)
        return pets

    def update_pet_state(self, updated_pet: Pet) -> bool:
        """Update a specific pet's state in the penc."""
        pets = self._read_pets()
        pet_index = self._find_pet_index(updated_pet.name)
        if pet_index >= 0:
            pets[pet_index] = updated_pet.__dict__
            return self._write_pets(pets)
        return False

    def update_all_pets(self) -> bool:
        """Update the state of all pets in the penc."""
        pets = self.get_all_pets()
        for pet in pets:
            pet.update()
            if not self.update_pet_state(pet):
                return False
        return True

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Retrieve a pet by name from the penc."""
        pets = self.get_all_pets()
        for pet in pets:
            if pet.name == pet_name:
                return pet
        return None
