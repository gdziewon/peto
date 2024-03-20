from services.penc import Penc
import os
from pets.pet_base import Pet
from services.pet_factory import PetFactory


class PencOperations:
    def __init__(self):
        self.penc = self._get_current_penc()

    @staticmethod
    def _get_current_penc() -> Penc or None:
        current_dir = os.getcwd()
        penc_file = os.path.join(current_dir, ".penc")
        if os.path.exists(penc_file):
            return Penc(current_dir)
        else:
            return None

    def _get_pet(self, pet_name: str) -> Pet:
        if self.penc:
            return self.penc.get_pet(pet_name)
        else:
            print("No penc available to get pet from.")

    @staticmethod
    def create_penc(penc_name: str = None) -> Penc:
        penc_name = penc_name if penc_name else "."
        penc = Penc(penc_name)
        penc.create_penc()
        return penc

    def list_pets(self):
        if self.penc:
            pets = self.penc.get_all_pets()
            if pets:
                print("Pets in this penc:")
                for pet in pets:
                    print(pet.name)
            else:
                print("No pets found in this penc.")

    def add_pet(self, pet_name: str, species: str):
        if self.penc:
            new_pet = PetFactory(pet_name).create(species)
            if not new_pet:
                print(f"Failed to create pet '{pet_name}'.")

            if self.penc.add_pet(new_pet):
                print(f"Pet '{pet_name}' added to the penc as a {new_pet.species}.")
            else:
                print(f"Failed to add pet '{pet_name}'.")
        else:
            print("No penc found in the current directory.")

    def show_pet(self, pet_name: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.show()

    def feed_pet(self, pet_name: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.eat()
            self.penc.update_pet_state(pet)
            print(f"Fed {pet_name}.")

    def play_with_pet(self, pet_name: str, toy: str):
        pet = self._get_pet(pet_name)
        if pet:
            pet.play(toy)
            self.penc.update_pet_state(pet)
            print(f"Played with {pet_name} using {toy}.")

    def kill_pet(self, pet_name: str):
        print(f"Are you sure you want to kill {pet_name}? This action cannot be undone.")
        confirmation = input("Kill [y/N]: ")
        if confirmation.lower() != "y":
            print(f"Killing aborted. {pet_name} is safe.")
            return
        self.penc.kill_pet(pet_name)
        print(f"You monster, you killed {pet_name}. RIP.")
