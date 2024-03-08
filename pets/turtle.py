from pets.pet_base import Pet
from pets.actions.eating import eat_action
from utils.constants import INITIAL_SHELL_STRENGTH, PREFERRED_FOOD_TURTLE


class Turtle(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self.preferred_food = PREFERRED_FOOD_TURTLE
        self._shell_strength = INITIAL_SHELL_STRENGTH

    def show(self):
        super().show()
        print(f"Shell strength: {self.shell_strength}/100")
        return

    def eat(self):
        eat_action(self)
        return

    def play(self, toy: str):
        print(f"{self.name} is too slow to play")
        return

    @property
    def shell_strength(self):
        return self._shell_strength

    @shell_strength.setter
    def shell_strength(self, value: int):
        value = Pet.get_correct_value(value)
        self._shell_strength = value
