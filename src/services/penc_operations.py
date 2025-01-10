from functools import wraps
from pathlib import Path
from typing import List, Optional

from pets.pet_base import Pet
from services.penc import Penc
from services.penc_manager import PencManager
from services.pet_factory import PetFactory
from utils.constants import PENC_FILE_EXTENSION
from utils.utils import get_tmp


def check_penc(method):
    """Decorator to ensure the penc exists before executing the method."""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.penc:
            print("No penc found in the current directory.")
            return
        return method(self, *args, **kwargs)

    return wrapper


class PencOperations:
    def __init__(self):
        self.penc = self._get_current_penc()
        self.manager = PencManager()
        self.reload_signal = Path(get_tmp() / ".reload")

    @staticmethod
    def _get_current_penc() -> Optional[Penc]:
        penc_file = Path.cwd() / PENC_FILE_EXTENSION
        return Penc(Path.cwd()) if penc_file.exists() else None

    def signal_reload(self):
        self.reload_signal.touch()

    def _get_all_pets(self) -> List[Pet]:
        pets = self.penc.get_all_pets() if self.penc else []
        if not pets:
            print("No pets found in this penc.")
        return pets

    def _get_pet(self, pet_name: str) -> Optional[Pet]:
        """Fetch a pet by name; notify if not found."""
        pet = self.penc.get_pet(pet_name) if self.penc else None
        if not pet:
            print(f"No pet named '{pet_name}' found in penc.")
        return pet

    def _get_pet_names(self) -> List[str]:
        return [pet.name for pet in self._get_all_pets()]

    def create_penc(self, penc_name: str = ".") -> Optional[Penc]:
        if self._get_current_penc():
            print("Penc already exists")
            return None
        penc = Penc(Path(penc_name))
        if penc.create_penc():
            self.manager.add_penc(penc)
            self.signal_reload()
            print(f"Penc at '{penc.directory}' created.")
            return penc
        print("Failed to create penc.")
        return None

    @check_penc
    def list_pets(self):
        pets = self._get_all_pets()
        if pets:
            print("Pets in this penc:")
            for pet in pets:
                print(f"{pet.name} {pet.emoji}")

    @check_penc
    def add_pet(self, pet_name: str, species: str):
        if self.penc.get_pet(pet_name):
            print(f"Pet {pet_name} already exists in penc {self.penc.name}.")
            return
        new_pet = PetFactory().create(pet_name, species, self.penc.directory)
        if new_pet and self.penc.add_pet(new_pet):
            print(f"Pet '{pet_name}' added as a {new_pet.species}.")
        else:
            print(f"Failed to add pet '{pet_name}'.")

    @check_penc
    def show_pet(self, pet_name: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.show()

    @check_penc
    def show_all_pets(self):
        for pet_name in self._get_pet_names():
            self.show_pet(pet_name)

    @check_penc
    def feed_pet(self, pet_name: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.eat()
            self.penc.update_pet_state(pet)
            print(f"Fed {pet_name}.")

    @check_penc
    def play_with_pet(self, pet_name: str, toy: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.play(toy)
            self.penc.update_pet_state(pet)
            print(f"Played with {pet_name} using {toy}.")

    def confirm_action(self, action: str) -> bool:
        confirmation = input(f"{action} [y/N]: ")
        return confirmation.strip().lower() == "y"

    @check_penc
    def kill_pet(self, pet_name: str):
        pet = self._get_pet(pet_name)
        if pet:
            if self.confirm_action(f"Are you sure you want to kill {pet_name}?"):
                if self.penc.kill_pet(pet_name):
                    print(f"You monster, you killed {pet_name}. RIP.")
                else:
                    print("Failed to kill pet.")
            else:
                print(f"Killing aborted. {pet_name} is safe.")

    @check_penc
    def kill_all_pets(self):
        pets = self._get_all_pets()
        if pets:
            print("Pets to be killed:")
            for pet in pets:
                print(pet.name)
            if self.confirm_action("Kill all"):
                if self.penc.kill_all_pets():
                    print("You disgust me, you killed all the pets... RIP.")
                else:
                    print("Failed to kill all pets.")
