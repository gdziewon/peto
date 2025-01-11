import random
from abc import ABC, abstractmethod
from pathlib import Path

from termcolor import colored

from pets.art.art_dict import art
from utils.constants import (
    HEALTH_LOSS_RATE,
    HUNGER_GAIN_RATE,
    INITIAL_AGE,
    INITIAL_HEALTH,
    INITIAL_HUNGER,
    INITIAL_MOOD,
    MOOD_LOSS_RATE,
)


class Pet(ABC):
    def __init__(self, name: str, directory: Path):
        self._name = name
        self.species = self.__class__.__name__
        self.file = directory / f"{self._name}.peto"
        self._health = INITIAL_HEALTH
        self.age = INITIAL_AGE
        self._mood = INITIAL_MOOD
        self._hunger = INITIAL_HUNGER
        self.preferred_food = None
        self.stomach = []
        self.memory = []
        self.body = self.load_art()
        self.emoji = art[self.species]["emoji"]
        self._minutes = 0

    def load_art(self) -> str:
        if self.file.exists():
            return self.file.read_text()
        else:
            body = random.choice(art[self.species]["body"])
            return body

    def save_art(self):
        self.file.write_text(self.body)

    def get_color(value: int) -> str:
        return "green" if value > 70 else "yellow" if value > 40 else "red"

    @abstractmethod
    def show(self) -> None:
        """
        Display the creature's information with colored output.
        """
        self.update()

        print(colored(self.body, "green"), "\n")

        details = [
            ("Name: ", self.name, "blue"),
            ("Species: ", self.species, "magenta"),
            ("Age: ", f"{int(self.age)}", "yellow"),
            ("Health: ", f"{int(self.health)}/100", Pet.get_color(int(self.health))),
            ("Mood: ", f"{int(self.mood)}/100", Pet.get_color(int(self.mood))),
            (
                "Hunger: ",
                f"{int(self.hunger)}/100",
                Pet.get_color(100 - int(self.hunger)),
            ),
        ]

        for label, value, color in details:
            print(colored(label, "cyan") + colored(value, color))

    @abstractmethod
    def update(self):
        self.hunger += HUNGER_GAIN_RATE * 1000
        if self.hunger >= 100:
            self.health -= HEALTH_LOSS_RATE
        self.mood -= (2 * self.hunger) + 50 - self.health * 1000 * MOOD_LOSS_RATE
        self._minutes += 1
        self._age = self._minutes / 60

    @abstractmethod
    def eat(self) -> None:
        pass

    @abstractmethod
    def play(self, toy: str) -> None:
        pass

    @staticmethod
    def _get_correct_value(value: int) -> int:
        return max(0, min(value, 100))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value.strip()

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value: int):
        self._health = Pet._get_correct_value(value)

    @property
    def mood(self):
        return self._mood

    @mood.setter
    def mood(self, value: int):
        self._mood = Pet._get_correct_value(value)

    @property
    def hunger(self):
        return self._hunger

    @hunger.setter
    def hunger(self, value: int):
        self._hunger = Pet._get_correct_value(value)
