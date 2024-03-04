import requests


def is_valid_toy(toy: str) -> bool:
    return toy.startswith("http://") or toy.startswith("https://")


def calculate_mood_change(pet, response) -> int:
    status_code = response.status_code
    match status_code:
        case 200:
            print(f"Playing with {pet.name} was successful")
            length = len(response.content)
            return int(length / 100)
        case 404:
            print(f"{pet.name} lost the toy!")
            return -8
        case 403:
            print(f"{pet.name} was not allowed to play with the toy")
            return -5
        case 500:
            print(f"{pet.name} broke the toy!")
            return -10
        case _:
            print(f"{pet.name} was unable to play with the toy")
            return -1


def change_mood(pet, mood_change: int):
    pet.mood += mood_change
    print(f"Mood change: {mood_change}")
    if pet.mood > 100:
        pet.mood = 100
    elif pet.mood < 0:
        pet.mood = 0
    print(f"{pet.name}'s mood is now {pet.mood}/100")


def play(pet, toy: str):
    if not is_valid_toy(toy):
        print(f"Invalid toy {toy}")
        change_mood(pet, -3)
        return

    print(f"{pet.name} is playing with {toy}")
    response = requests.get(toy)
    if response:
        print(f"Toy made noise!: {response.content}")
        pet.knowledge.append(response.content)
        mood_change = calculate_mood_change(pet, response)
        change_mood(pet, mood_change)
    else:
        print(f"Playing with {pet.name} was unsuccessful")
        change_mood(pet, -3)
    return
