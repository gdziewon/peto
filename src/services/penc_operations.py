# services/penc_operations.py
from functools import wraps
from pathlib import Path
from typing import List, Optional

from termcolor import colored

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
            print(colored("No penc found in the current directory.", "red"))
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
            print(colored("No pets found in this penc.", "yellow"))
        return pets

    def _get_pet(self, pet_name: str) -> Optional[Pet]:
        """Fetch a pet by name; notify if not found."""
        pet = self.penc.get_pet(pet_name) if self.penc else None
        if not pet:
            print(colored(f"No pet named {colored(f'\'{pet_name}\'', 'yellow')} found in penc.", "red"))
        return pet

    def _get_pet_names(self) -> List[str]:
        return [pet.name for pet in self._get_all_pets()]

    def create_penc(self, penc_name: str = ".") -> Optional[Penc]:
        if self._get_current_penc():
            print(colored("Penc already exists", "red"))
            return None
        penc = Penc(Path(penc_name))
        if penc.create_penc():
            self.manager.add_penc(penc)
            self.signal_reload()
            msg = (
                colored("Penc at ", "green") +
                colored(f"'{penc.directory}'", "yellow") +
                colored(" created.", "green")
            )
            print(msg)
            return penc
        print(colored("Failed to create penc.", "red"))
        return None

    @check_penc
    def list_pets(self):
        pets = self._get_all_pets()
        if pets:
            print(colored("Pets in this penc:", "cyan"))
            for pet in pets:
                # The pet name is highlighted in blue and its emoji in magenta.
                print(colored(pet.name, "blue") + " " + colored(pet.emoji, "magenta"))

    @check_penc
    def add_pet(self, pet_name: str, species: str):
        if self.penc.get_pet(pet_name):
            msg = (
                colored("Pet ", "cyan") +
                colored(f"'{pet_name}'", "yellow") +
                colored(f" already exists in penc {self.penc.name}.", "cyan")
            )
            print(msg)
            return
        new_pet = PetFactory().create(pet_name, species, self.penc.directory)
        if new_pet and self.penc.add_pet(new_pet):
            msg = (
                colored("Pet ", "green") +
                colored(f"'{pet_name}'", "yellow") +
                colored(f" added as a {new_pet.species}.", "green")
            )
            print(msg)
        else:
            print(colored(f"Failed to add pet {colored(f'\'{pet_name}\'', 'yellow')}.", "red"))

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
            msg = (
                colored("Fed ", "green") +
                colored(f"'{pet_name}'", "yellow") +
                colored(".", "green")
            )
            print(msg)

    @check_penc
    def play_with_pet(self, pet_name: str, toy: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.play(toy)
            self.penc.update_pet_state(pet)
            msg = (
                colored("Played with ", "green") +
                colored(f"'{pet_name}'", "yellow") +
                colored(f" using {toy}.", "green")
            )
            print(msg)

    def confirm_action(self, action: str) -> bool:
        confirmation = input(colored(f"{action} [y/N]: ", "cyan"))
        return confirmation.strip().lower() == "y"

    @check_penc
    def kill_pet(self, pet_name: str):
        pet = self._get_pet(pet_name)
        if pet:
            if self.confirm_action(f"Are you sure you want to kill {colored(f'\'{pet_name}\'', 'yellow')}?"):
                if self.penc.kill_pet(pet_name):
                    print(colored(f"You monster, you killed {colored(f'\'{pet_name}\'', 'yellow')}. RIP.", "red"))
                else:
                    print(colored("Failed to kill pet.", "red"))
            else:
                print(colored(f"Killing aborted. {colored(f'\'{pet_name}\'', 'yellow')} is safe.", "yellow"))

    @check_penc
    def kill_all_pets(self):
        pets = self._get_all_pets()
        if pets:
            print(colored("Pets to be killed:", "red"))
            for pet in pets:
                print(colored(pet.name, "red"))
            if self.confirm_action("Kill all"):
                if self.penc.kill_all_pets():
                    print(colored("You disgust me, you killed all the pets... RIP.", "red"))
                else:
                    print(colored("Failed to kill all pets.", "red"))

