from pets.pet import Pet
from pets.frog import Frog
from pets.tortoise import Tortoise
import argparse
from utils.penc import Penc
import os


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


def list_pets() -> None:
    penc = get_current_penc()
    if penc:
        pets = penc.get_pets()
        if pets:
            print("Pets in this penc:")
            for pet in pets:
                print(pet.name)
        else:
            print("No pets found in this penc.")


def add_pet(pet_name: str, is_tortoise=False, is_frog=False) -> None:
    penc = get_current_penc()
    if penc:
        species_flags = [is_tortoise, is_frog]
        if sum(species_flags) > 1:
            print("Error: Please specify only one species for the pet.")
            return

        if any(pet.name == pet_name for pet in penc.get_pets()):
            print(f"Pet '{pet_name}' already exists in the penc.")
            return

        if is_tortoise:
            new_pet = Tortoise(pet_name)
            species = 'Tortoise'
        elif is_frog:
            new_pet = Frog(pet_name)
            species = 'Frog'
        else:
            new_pet = Pet(pet_name)
            species = 'Pet'

        penc.add_pet(new_pet)
        print(f"Pet '{pet_name}' added to the penc as a {species}.")


def show_pet(pet_name) -> None:
    pet = get_pet_from_current_penc(pet_name)
    if pet:
        pet.show()


def feed_pet(pet_name) -> None:
    pet = get_pet_from_current_penc(pet_name)
    if pet:
        pet.eat()
        penc = get_current_penc()
        penc.update_pet(pet)
        print(f"Fed {pet_name}.")


def play_with_pet(pet_name, toy) -> None:
    pet = get_pet_from_current_penc(pet_name)
    if pet:
        pet.play(toy)
        penc = get_current_penc()
        penc.update_pet(pet)
        print(f"Played with {pet_name} using {toy}.")


def peto():
    parser = argparse.ArgumentParser(description="Manage your Peto pences and pets.")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    create_parser = subparsers.add_parser('create', help='Create a new Peto enclosure (penc) in the current directory.')
    create_parser.add_argument('penc_name', nargs='?', default="", help='The name of the penc to create (optional)')

    list_parser = subparsers.add_parser('list', help='List all pets in the current penc')

    add_parser = subparsers.add_parser('add', help='Add a pet to the current penc')
    add_parser.add_argument('pet_name', help='The name of the pet to add')
    add_parser.add_argument('--tortoise', action='store_true', help='Add a Tortoise pet')
    add_parser.add_argument('--frog', action='store_true', help='Add a Frog pet')

    show_parser = subparsers.add_parser('show', help='Show a specific pet')
    show_parser.add_argument('pet_name', help='The name of the pet to show')

    feed_parser = subparsers.add_parser('feed', help='Feed a specific pet')
    feed_parser.add_argument('pet_name', help='The name of the pet to feed')

    play_parser = subparsers.add_parser('play', help='Play with a specific pet')
    play_parser.add_argument('pet_name', help='The name of the pet to play with')
    play_parser.add_argument('toy', help='URL of the toy to play with')

    args = parser.parse_args()

    if args.command == 'create':
        penc_name = args.penc_name if args.penc_name else "."
        penc = Penc(penc_name)
        penc.create()
    elif args.command == 'list':
        list_pets()
    elif args.command == 'add':
        add_pet(args.pet_name, is_tortoise=args.tortoise, is_frog=args.frog)
    elif args.command == 'show':
        pet = get_pet_from_current_penc(args.pet_name)
        if pet:
            pet.show()
    elif args.command == 'feed':
        feed_pet(args.pet_name)
    elif args.command == 'play':
        play_with_pet(args.pet_name, args.toy)
    else:
        parser.print_help()


if __name__ == "__main__":
    peto()
