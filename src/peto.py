#!/usr/bin/env python3
import os
import subprocess
from argparse import ArgumentParser
from pathlib import Path

from services.penc_operations import PencOperations

PETO = Path(__file__).resolve().parents[1]
SERVICE_PID_FILE = PETO / ".peto_service.pid"
os.environ["PETO"] = str(PETO)


def start_service():
    if SERVICE_PID_FILE.exists():
        with SERVICE_PID_FILE.open("r") as f:
            pid = int(f.read().strip())
            if not (Path("/proc") / f"{pid}").exists():
                SERVICE_PID_FILE.unlink()

    subprocess.Popen(
        [str(PETO / "src/services/peto_service.py")],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )


def create_penc(args, penc_op):
    penc = penc_op.create_penc(args.penc_name)
    if not penc:
        print("Error creating penc.")


def list_pets(_, penc_op):
    penc_op.list_pets()


def add_pet(args, penc_op):
    penc_op.add_pet(args.pet_name, args.species)


def show_pet(args, penc_op):
    if args.all:
        penc_op.show_all_pets()
    elif args.pet_name:
        penc_op.show_pet(args.pet_name)
    else:
        print("Please specify a pet name or use the --all option.")


def feed_pet(args, penc_op):
    penc_op.feed_pet(args.pet_name)


def play_with_pet(args, penc_op):
    penc_op.play_with_pet(args.pet_name, args.toy)


def kill_pet(args, penc_op):
    if args.all:
        penc_op.kill_all_pets()
    elif args.pet_name:
        penc_op.kill_pet(args.pet_name)
    else:
        print("Please specify a pet name or use the --all option.")


def peto():
    parser = ArgumentParser(description="Manage your Peto pences and pets.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # penc
    create_parser = subparsers.add_parser(
        "penc", help="Create a new Peto enclosure (penc) in the current directory."
    )
    create_parser.add_argument(
        "penc_name",
        nargs="?",
        default="",
        help="The name of the penc to create (optional)",
    )
    create_parser.set_defaults(func=create_penc)

    # list
    subparsers.add_parser(
        "list", help="List all pets in the current penc"
    ).set_defaults(func=list_pets)

    # add
    add_parser = subparsers.add_parser("add", help="Add a pet to the current penc")
    add_parser.add_argument("species", help="The species of the pet to add")
    add_parser.add_argument("pet_name", help="The name of the pet to add")
    add_parser.set_defaults(func=add_pet)

    # show
    show_parser = subparsers.add_parser("show", help="Show a specific pet")
    show_parser.add_argument(
        "pet_name", nargs="?", default=None, help="The name of the pet to show"
    )
    show_parser.add_argument("-a", "--all", action="store_true", help="Show all pets")
    show_parser.set_defaults(func=show_pet)

    # feed
    feed_parser = subparsers.add_parser("feed", help="Feed a specific pet")
    feed_parser.add_argument("pet_name", help="The name of the pet to feed")
    feed_parser.set_defaults(func=feed_pet)

    # play
    play_parser = subparsers.add_parser("play", help="Play with a specific pet")
    play_parser.add_argument("pet_name", help="The name of the pet to play with")
    play_parser.add_argument("toy", help="URL of the toy to play with")
    play_parser.set_defaults(func=play_with_pet)

    # kill
    kill_parser = subparsers.add_parser("kill", help="Kill a specific pet")
    kill_parser.add_argument(
        "pet_name", nargs="?", default=None, help="The name of the pet to kill"
    )
    kill_parser.add_argument("-a", "--all", action="store_true", help="Kill all pets")
    kill_parser.set_defaults(func=kill_pet)

    args = parser.parse_args()

    start_service()
    penc_op = PencOperations()

    if not args.command:
        parser.print_help()
    else:
        args.func(args, penc_op)


if __name__ == "__main__":
    peto()
