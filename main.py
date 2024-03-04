from objects.pet import Pet
import argparse
from objects.penc import Penc
import os


def get_current_penc():
    current_dir = os.getcwd()
    penc_file = os.path.join(current_dir, ".penc")
    if os.path.exists(penc_file):
        return Penc(current_dir)
    else:
        print("No penc found in the current directory.")
        return None


def list_pets():
    penc = get_current_penc()
    if penc:
        pets = penc.read_pets()
        if pets:
            print("Pets in this penc:")
            for pet in pets:
                print(pet['name'])
        else:
            print("No pets found in this penc.")


def add_pet(pet_name):
    penc = get_current_penc()
    if penc:
        if any(pet['name'] == pet_name for pet in penc.read_pets()):
            print(f"Pet '{pet_name}' already exists in the penc.")
            return
        new_pet = Pet(pet_name)
        penc.add_pet(new_pet)
        print(f"Pet '{pet_name}' added to the penc.")


def feed_pet(pet_name):
    pet = Pet.load(pet_name)
    if pet:
        pet.eat()
        pet.save()
        print(f"Fed {pet_name}.")


def play_with_pet(pet_name, toy):
    pet = Pet.load(pet_name)
    if pet:
        pet.play(toy)
        pet.save()
        print(f"Played with {pet_name} using {toy}.")


def peto():
    parser = argparse.ArgumentParser(description="Manage your Peto pences and pets.")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    create_parser = subparsers.add_parser('create', help='Create a new penc')
    create_parser.add_argument('penc_name', help='The name of the penc to create')

    list_parser = subparsers.add_parser('list', help='List all pets in the current penc')

    add_parser = subparsers.add_parser('add', help='Add a pet to the current penc')
    add_parser.add_argument('pet_name', help='The name of the pet to add')

    add_parser = subparsers.add_parser('feed', help='Add a pet to the current penc')
    add_parser.add_argument('pet_name', help='The name of the pet to add')

    feed_parser = subparsers.add_parser('feed', help='Feed a specific pet')
    feed_parser.add_argument('pet_name', help='The name of the pet to feed')

    play_parser = subparsers.add_parser('play', help='Play with a specific pet')
    play_parser.add_argument('pet_name', help='The name of the pet to play with')
    play_parser.add_argument('toy', help='URL of the toy to play with')

    args = parser.parse_args()

    if args.command == 'create':
        penc = Penc(args.penc_name)
        penc.create()
    elif args.command == 'list':
        list_pets()
    elif args.command == 'add':
        add_pet(args.pet_name)
    elif args.command == 'feed':
        feed_pet(args.pet_name)
    elif args.command == 'play':
        play_with_pet(args.pet_name, args.toy)
    else:
        parser.print_help()


if __name__ == "__main__":
    peto()
