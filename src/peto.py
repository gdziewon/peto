#!/usr/bin/env python3
from argparse import ArgumentParser

from services.penc_operations import PencOperations


def peto():
    parser = ArgumentParser(description="Manage your Peto pences and pets.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    create_parser = subparsers.add_parser(
        "penc", help="Create a new Peto enclosure (penc) in the current directory."
    )
    create_parser.add_argument(
        "penc_name",
        nargs="?",
        default="",
        help="The name of the penc to create (optional)",
    )

    subparsers.add_parser("list", help="List all pets in the current penc")

    add_parser = subparsers.add_parser("add", help="Add a pet to the current penc")
    add_parser.add_argument("species", help="The species of the pet to add")
    add_parser.add_argument("pet_name", help="The name of the pet to add")

    show_parser = subparsers.add_parser("show", help="Show a specific pet")
    show_parser.add_argument(
        "pet_name", nargs="?", default=None, help="The name of the pet to show"
    )
    show_parser.add_argument("-a", "--all", action="store_true", help="Show all pets")

    feed_parser = subparsers.add_parser("feed", help="Feed a specific pet")
    feed_parser.add_argument("pet_name", help="The name of the pet to feed")

    play_parser = subparsers.add_parser("play", help="Play with a specific pet")
    play_parser.add_argument("pet_name", help="The name of the pet to play with")
    play_parser.add_argument("toy", help="URL of the toy to play with")

    kill_parser = subparsers.add_parser("kill", help="Kill a specific pet")
    kill_parser.add_argument(
        "pet_name", nargs="?", default=None, help="The name of the pet to kill"
    )
    kill_parser.add_argument("-a", "--all", action="store_true", help="Kill all pets")

    args = parser.parse_args()

    penc_op = PencOperations()
    if args.command == "penc":
        penc = PencOperations.create_penc(args.penc_name)
        if not penc:
            print("Error creating penc.")
    elif args.command == "list":
        penc_op.list_pets()
    elif args.command == "add":
        penc_op.add_pet(args.pet_name, args.species)
    elif args.command == "show":
        if args.all:
            penc_op.show_all_pets()
        elif args.pet_name:
            penc_op.show_pet(args.pet_name)
        else:
            print("Please specify a pet name or use the --all option.")
    elif args.command == "feed":
        penc_op.feed_pet(args.pet_name)
    elif args.command == "play":
        penc_op.play_with_pet(args.pet_name, args.toy)
    elif args.command == "kill":
        if args.all:
            penc_op.kill_all_pets()
        elif args.pet_name:
            penc_op.kill_pet(args.pet_name)
        else:
            print("Please specify a pet name or use the --all option.")


if __name__ == "__main__":
    peto()
