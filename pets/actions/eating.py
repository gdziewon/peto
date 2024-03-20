import os
import random
import hashlib
from utils.constants import NUTRITIONAL_VALUE_THRESHOLD, HAMMING_DISTANCE_THRESHOLD, FOOD_DIVIDER_FROG, \
    FOOD_DIVIDER_TURTLE, PENC_FILE_EXTENSION, FOOD_DIVIDER_CROCODILE


def generate_food_hash(food_path: str) -> str:
    with open(food_path, 'rb') as f:
        food_hash = hashlib.sha256(f.read()).hexdigest()
    return food_hash


def is_hash_similar(hash1: str, hash2: str) -> bool:
    hash1_bin = bin(int(hash1, 16))[2:].zfill(256)
    hash2_bin = bin(int(hash2, 16))[2:].zfill(256)

    hamming_distance = sum(c1 != c2 for c1, c2 in zip(hash1_bin, hash2_bin))

    return hamming_distance < HAMMING_DISTANCE_THRESHOLD


def will_eat(pet, food_name: str, nutritional_value: int, food_hash: str) -> bool:
    if nutritional_value > pet.hunger * NUTRITIONAL_VALUE_THRESHOLD:
        print(f"{pet.name} is not hungry enough to eat {food_name} ({nutritional_value} nutritional value)")
        return False

    for food in pet.stomach:
        if is_hash_similar(food_hash, food['hash']) or food_name == food['food_name']:
            print(f"{pet.name} doesn't want to eat {food_name} again")
            return False
    return True


def get_food(pet) -> str or None:
    print(f"{pet.name} is looking for food: {pet.preferred_food}")
    food_options = [f for f in os.listdir() if f.endswith(tuple(pet.preferred_food)) and f != PENC_FILE_EXTENSION]
    if not food_options:
        return None, None
    food_name = random.choice(food_options)
    food_path = os.path.join(os.getcwd(), food_name)
    return food_name, food_path


def calculate_nutritional_value(pet, food: str) -> int:
    size = os.path.getsize(food)
    food_divider = get_food_divider(pet)
    return int(size / food_divider)


def get_food_divider(pet):
    if pet.species == "Frog":
        return FOOD_DIVIDER_FROG
    elif pet.species == "Turtle":
        return FOOD_DIVIDER_TURTLE
    elif pet.species == "Crocodile":
        return FOOD_DIVIDER_CROCODILE
    else:
        print(f"Unknown species {pet.species}")
        return 0


def change_hunger(pet, nutritional_value: int):
    pet.hunger -= nutritional_value
    print(f"{pet.name}'s hunger is now {pet.hunger}/100")


def eat_action(pet):
    food_name, food_path = get_food(pet)
    if not food_name or not food_path:
        print(f"{pet.name} has no food to eat")
        return

    nutritional_value = calculate_nutritional_value(pet, food_path)
    food_hash = generate_food_hash(food_path)
    if not will_eat(pet, food_name, nutritional_value, food_hash):
        return

    print(f"{pet.name} is eating {food_name} ({nutritional_value} nutritional value)")
    change_hunger(pet, nutritional_value)

    pet.stomach.append({'food_name': food_name, 'hash': food_hash})
    os.remove(food_path)
