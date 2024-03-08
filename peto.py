import argparse
from services.penc_operations import list_pets, add_pet, feed_pet, play_with_pet, \
    create_penc, show_pet


def peto():
    parser = argparse.ArgumentParser(description="Manage your Peto pences and pets.")
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    create_parser = subparsers.add_parser('penc', help='Create a new Peto enclosure (penc) in the current directory.')
    create_parser.add_argument('penc_name', nargs='?', default="", help='The name of the penc to create (optional)')

    subparsers.add_parser('list', help='List all pets in the current penc')

    add_parser = subparsers.add_parser('add', help='Add a pet to the current penc')
    add_parser.add_argument('pet_name', help='The name of the pet to add')
    group = add_parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--turtle', action='store_true', help='Add a Turtle pet')
    group.add_argument('--frog', action='store_true', help='Add a Frog pet')

    show_parser = subparsers.add_parser('show', help='Show a specific pet')
    show_parser.add_argument('pet_name', help='The name of the pet to show')

    feed_parser = subparsers.add_parser('feed', help='Feed a specific pet')
    feed_parser.add_argument('pet_name', help='The name of the pet to feed')

    play_parser = subparsers.add_parser('play', help='Play with a specific pet')
    play_parser.add_argument('pet_name', help='The name of the pet to play with')
    play_parser.add_argument('toy', help='URL of the toy to play with')

    args = parser.parse_args()

    if args.command == 'penc':
        penc = create_penc(args.penc_name)
        if not penc:
            print("Error creating penc.")
    elif args.command == 'list':
        list_pets()
    elif args.command == 'add':
        add_pet(args.pet_name, [args.turtle, args.frog])
    elif args.command == 'show':
        show_pet(args.pet_name)
    elif args.command == 'feed':
        feed_pet(args.pet_name)
    elif args.command == 'play':
        play_with_pet(args.pet_name, args.toy)
    else:
        parser.print_help()


if __name__ == "__main__":
    peto()
