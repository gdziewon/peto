import random
from abc import ABC, abstractmethod
from pathlib import Path

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

    @abstractmethod
    def show(self) -> None:
        self.update()
        print(self.body)
        print(f"Name: {self.name}")
        print(f"Species: {self.species}")
        print(f"Age: {int(self.age)}")
        print(f"Health: {int(self.health)}/100")
        print(f"Mood: {int(self.mood)}/100")
        print(f"Hunger: {int(self.hunger)}/100")

    @abstractmethod
    def update(self):
        self.health -= (self.hunger - 50) * 1000 * HEALTH_LOSS_RATE
        self.hunger += HUNGER_GAIN_RATE * 1000

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
