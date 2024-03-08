import requests
from utils.constants import MOOD_INCREASE_DIVIDER, CODE_404_DECREASE, CODE_403_DECREASE, CODE_500_DECREASE, CODE_OTHER_DECREASE, DEFAULT_DECREASE


def is_valid_toy(toy: str) -> bool:
    return toy.startswith(tuple(["http://", "https://"]))


def will_play(pet, toy: str) -> bool:
    if not is_valid_toy(toy):
        print(f"Invalid toy {toy}")
        return False

    if toy in pet.memory:
        print(f"{pet.name} already played with {toy}")
        return False

    return True


def calculate_mood_change(pet, response: requests.Response) -> int:
    status_code = response.status_code
    match status_code:
        case 200:
            print(f"Playing with {pet.name} was successful")
            length = len(response.content)
            return int(length / MOOD_INCREASE_DIVIDER)
        case 404:
            print(f"{pet.name} lost the toy!")
            return CODE_404_DECREASE
        case 403:
            print(f"{pet.name} was not allowed to play with the toy")
            return CODE_403_DECREASE
        case 500:
            print(f"{pet.name} broke the toy!")
            return CODE_500_DECREASE
        case _:
            print(f"{pet.name} was unable to play with the toy")
            return CODE_OTHER_DECREASE


def change_mood(pet, mood_change: int):
    pet.mood += mood_change
    print(f"{pet.name}'s mood is now {pet.mood}/100")


def play_action(pet, toy: str):
    if not is_valid_toy(toy):
        print(f"Invalid toy {toy}")
        change_mood(pet, DEFAULT_DECREASE)
        return

    print(f"{pet.name} is playing with {toy}")
    response = requests.get(toy)
    if response:
        print(f"Toy made noise!: {response.content}")
        mood_change = calculate_mood_change(pet, response)
        change_mood(pet, mood_change)
    else:
        print(f"{pet.name} didn't have fun with {toy}")
        change_mood(pet, DEFAULT_DECREASE)

    pet.memory.append(toy)
    return
