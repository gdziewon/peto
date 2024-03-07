from actions.playing import play
from actions.eating import eat


class Pet:
    def __init__(self, name: str):
        self.name = name
        self.species = self.__class__.__name__
        self.health = 100
        self.age = 0
        self.mood = 50
        self.hunger = 50
        self.preferred_food = [".exe"]
        self.stomach = []
        self.knowledge = []

    def show(self) -> None:
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Health: {self.health}/100")
        print(f"Mood: {self.mood}/100")
        print(f"Hunger: {self.hunger}/100")

    def eat(self) -> None:
        eat(self)

    def play(self, toy: str) -> None:
        play(self, toy)
