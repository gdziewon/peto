import requests
from termcolor import colored

from utils.constants import (
    CODE_403_DECREASE,
    CODE_404_DECREASE,
    CODE_500_DECREASE,
    CODE_OTHER_DECREASE,
    DEFAULT_DECREASE,
    MOOD_INCREASE_DIVIDER,
)


def is_valid_toy(toy: str) -> bool:
    """Check that the toy URL starts with 'http://' or 'https://'."""
    return toy.startswith(("http://", "https://"))


def will_play(pet, toy: str) -> bool:
    """
    Determine if the pet is willing to play with the given toy.
    It returns False if the toy is invalid or has been used before.
    """
    if not is_valid_toy(toy):
        print(colored(f"Invalid toy {toy}", "red"))
        return False

    if toy in pet.memory:
        print(colored(f"{pet.name} already played with {toy}", "yellow"))
        return False

    return True


def change_mood(pet, mood_change: int):
    """Update the pet's mood by the given change value."""
    pet.mood += mood_change
    print(colored(f"{pet.name}'s mood is now {pet.mood}/100", "cyan"))


def calculate_mood_change(pet, response: requests.Response) -> int:
    """
    Calculate the mood change based on the response status code.
    Uses the length of the 'text' field from the response JSON for mood increase.
    """
    status_code = response.status_code
    match status_code:
        case 200:
            print(colored(f"Playing with {pet.name} was successful", "green"))
            try:
                data = response.json()
                text_value = data.get("text", "")
                if not text_value:
                    print(colored("No 'text' field found in the response.", "yellow"))
                return int(len(text_value) / MOOD_INCREASE_DIVIDER) if text_value else 5
            except ValueError:  # If response isn't JSON
                print(colored("Response was not valid JSON.", "yellow"))
                return 5  # Fallback mood increase
        case 404:
            print(colored(f"{pet.name} lost the toy!", "red"))
            return CODE_404_DECREASE
        case 403:
            print(colored(f"{pet.name} was not allowed to play with the toy", "red"))
            return CODE_403_DECREASE
        case 500:
            print(colored(f"{pet.name} broke the toy!", "red"))
            return CODE_500_DECREASE
        case _:
            print(colored(f"{pet.name} was unable to play with the toy", "red"))
            return CODE_OTHER_DECREASE


def play_action(pet, toy: str):
    """
    Perform the play action:
      - Validate the toy URL.
      - Retrieve the toy's response with a timeout.
      - Print only the 'text' portion of the response (if available).
      - Update the pet's mood based on the response.
      - Record the toy in the pet's memory.
    """
    if not is_valid_toy(toy):
        print(colored(f"Invalid toy {toy}", "red"))
        change_mood(pet, DEFAULT_DECREASE)
        return

    print(colored(f"{pet.name} is playing with {toy}", "cyan"))

    try:
        headers = {"Accept": "application/json"}
        response = requests.get(toy, headers=headers, timeout=5)

        if response.status_code == 200:
            try:
                if "application/json" in response.headers.get("Content-Type", ""):
                    data = response.json()
                    toy_text = data.get("text", "No text found")
                else:
                    toy_text = "No valid JSON content returned by the API."
                print(colored(f"Toy made noise!: {toy_text}", "green"))
            except ValueError:
                print(colored("Failed to parse JSON response.", "yellow"))
                toy_text = "No text found."
        else:
            print(
                colored(
                    f"Toy did not respond correctly. Status: {response.status_code}",
                    "red",
                )
            )

        mood_change = calculate_mood_change(pet, response)
        change_mood(pet, mood_change)
    except requests.RequestException as e:
        print(
            colored(f"{pet.name} didn't have fun with {toy} due to error: {e}", "red")
        )
        change_mood(pet, DEFAULT_DECREASE)

    pet.memory.append(toy)
