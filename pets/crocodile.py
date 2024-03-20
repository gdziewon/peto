from pets.pet_base import Pet
from pets.actions.playing import play_action
from pets.actions.eating import eat_action
from utils.constants import INITIAL_BITE_FORCE, PREFERRED_FOOD_CROCODILE


class Crocodile(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self.preferred_food = PREFERRED_FOOD_CROCODILE
        self._bite_force = INITIAL_BITE_FORCE

    def show(self):
        super().show()
        print(f"Bite force: {self.bite_force}/100")

    def eat(self):
        eat_action(self)

    def play(self, toy: str):
        print(f"{self.name} is snapping its jaws")
        play_action(self, toy)

    def update(self):
        super().update()

    @property
    def bite_force(self):
        return self._bite_force

    @bite_force.setter
    def bite_force(self, value: int):
        value = Pet.get_correct_value(value)
        self._bite_force = value
