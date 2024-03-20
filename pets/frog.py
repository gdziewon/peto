from pets.pet_base import Pet
from pets.actions.playing import play_action
from pets.actions.eating import eat_action
from utils.constants import INITIAL_JUMP_HEIGHT, PREFERRED_FOOD_FROG


class Frog(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self.preferred_food = PREFERRED_FOOD_FROG
        self._jump_height = INITIAL_JUMP_HEIGHT

    def show(self):
        super().show()
        print(f"Jump height: {self.jump_height}/100")

    def eat(self):
        eat_action(self)

    def play(self, toy):
        print(f"{self.name} is jumping around")
        play_action(self, toy)

    def update(self):
        super().update()

    @property
    def jump_height(self):
        return self._jump_height

    @jump_height.setter
    def jump_height(self, value):
        value = Pet.get_correct_value(value)
        self._jump_height = value
