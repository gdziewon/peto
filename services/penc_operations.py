from services.penc import Penc
import os
from pets.pet_base import Pet
from services.pet_factory import PetFactory


def get_pet_from_current_penc(pet_name: str) -> Pet or None:
    penc = get_current_penc()
    if penc:
        return penc.get_pet(pet_name)
    return None


def get_current_penc() -> Penc or None:
    current_dir = os.getcwd()
    penc_file = os.path.join(current_dir, ".penc")
    if os.path.exists(penc_file):
        return Penc(current_dir)
    else:
        print("No penc found in the current directory.")
        return None


def create_penc(penc_name: str = None) -> Penc:
    penc_name = penc_name if penc_name else "."
    penc = Penc(penc_name)
    penc.create()
    return penc


def list_pets():
    penc = get_current_penc()
    if penc:
        pets = penc.get_all_pets()
        if pets:
            print("Pets in this penc:")
            for pet in pets:
                print(pet.name)
        else:
            print("No pets found in this penc.")


def add_pet(pet_name: str, species: list[bool]):
    penc = get_current_penc()
    if penc:
        new_pet = PetFactory(pet_name).create(species)
        if not new_pet:
            print(f"Failed to create pet '{pet_name}'.")
            return

        if penc.add_pet(new_pet):
            print(f"Pet '{pet_name}' added to the penc as a {new_pet.species}.")
        else:
            print(f"Failed to add pet '{pet_name}'.")
    else:
        print("No penc found in the current directory.")


def show_pet(pet_name: str):
    pet = get_pet_from_current_penc(pet_name)
    if pet:
        pet.show()


def feed_pet(pet_name: str):
    pet = get_pet_from_current_penc(pet_name)
    if pet:
        pet.eat_action()
        penc = get_current_penc()
        penc.update_pet(pet)
        print(f"Fed {pet_name}.")


def play_with_pet(pet_name: str, toy: str):
    pet = get_pet_from_current_penc(pet_name)
    if pet:
        pet.play_action(toy)
        penc = get_current_penc()
        penc.update_pet(pet)
        print(f"Played with {pet_name} using {toy}.")
