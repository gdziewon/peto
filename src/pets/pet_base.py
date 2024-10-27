import random
import time
from abc import ABC, abstractmethod

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
    def __init__(self, name: str):
        self._name = name
        self._species = self.__class__.__name__
        self._health = INITIAL_HEALTH
        self._age = INITIAL_AGE
        self._mood = INITIAL_MOOD
        self._hunger = INITIAL_HUNGER
        self._preferred_food = None
        self._stomach = []
        self._memory = []
        self._body = random.choice(art[self.species]["body"])
        self._emoji = art[self.species]["emoji"]

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
        # TODO: enhance this
        self.health -= (self.hunger - 100) * 6000 * HEALTH_LOSS_RATE
        self.hunger += HUNGER_GAIN_RATE * 6000

        self.mood -= 6000 * MOOD_LOSS_RATE

    @abstractmethod
    def eat(self) -> None:
        pass

    @abstractmethod
    def play(self, toy: str) -> None:
        pass

    @staticmethod
    def _get_correct_value(value: int) -> int:
        if value > 100:
            value = 100
        elif value < 0:
            value = 0
        return value

    # Getters
    @property
    def name(self):
        return self._name

    @property
    def species(self):
        return self._species

    @property
    def health(self):
        return self._health

    @property
    def age(self):
        return self._age

    @property
    def mood(self):
        return self._mood

    @property
    def hunger(self):
        return self._hunger

    @property
    def preferred_food(self):
        return self._preferred_food

    @property
    def stomach(self):
        return self._stomach

    @property
    def memory(self):
        return self._memory

    @property
    def body(self):
        return self._body

    @property
    def emoji(self):
        return self._emoji

    # Setters
    @name.setter
    def name(self, value: str):
        value = value.strip()
        self._name = value

    @species.setter
    def species(self, value: str):
        self._species = value

    @health.setter
    def health(self, value: int):
        value = Pet._get_correct_value(value)
        self._health = value

    @age.setter
    def age(self, value: float):
        self._age = value

    @mood.setter
    def mood(self, value: int):
        value = Pet._get_correct_value(value)
        self._mood = value

    @hunger.setter
    def hunger(self, value: int):
        value = Pet._get_correct_value(value)
        self._hunger = value

    @preferred_food.setter
    def preferred_food(self, value: list[str]):
        self._preferred_food = value

    @stomach.setter
    def stomach(self, value: list[str]):
        self._stomach = value

    @memory.setter
    def memory(self, value: list[str]):
        self._memory = value

    @body.setter
    def body(self, value: str):
        self._body = value

    @emoji.setter
    def emoji(self, value: str):
        self._emoji = value
