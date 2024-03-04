import os
import random


def get_food() -> str or None:
    food_options = [f for f in os.listdir() if f != ".penc"]
    if not food_options:
        print("No food found")
        return None
    food_name = random.choice(food_options)
    return food_name, os.path.join(os.getcwd(), food_name)


def calculate_nutritional_value(food) -> int:
    size = os.path.getsize(food)
    return int(size / 1000)


def change_hunger(pet, nutritional_value: int):
    pet.hunger -= nutritional_value
    if pet.hunger < 0:
        pet.hunger = 0

    print(f"{pet.name}'s hunger is now {pet.hunger}/100")
    return


def eat(pet):
    food_name, food_path = get_food()
    if not food_name or not food_path:
        print(f"{pet.name} has no food to eat")
        return

    nutritional_value = calculate_nutritional_value(food_path)
    if nutritional_value > pet.hunger * 1.5:
        print(f"{pet.name} is not hungry enough to eat {food_name} ({nutritional_value} nutritional value)")
        return
    print(f"{pet.name} is eating {food_name} ({nutritional_value} nutritional value)")
    change_hunger(pet, nutritional_value)
    pet.stomach.append([food_name] * (nutritional_value + 1))
    os.remove(food_path)

    if pet.hunger < 30:
        print(f"{pet.name} is still hungry")
    else:
        print(f"{pet.name} is full")
    return
