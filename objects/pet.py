import json
from actions.playing import play
from actions.eating import eat


class Pet:
    def __init__(self, name: str):
        self.name = name
        self.health = 100
        self.age = 0
        self.mood = 50
        self.hunger = 50
        self.stomach = []
        self.knowledge = []

    def show(self) -> None:
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Health: {self.health}/100")
        print(f"Mood: {self.mood}/100")
        print(f"Hunger: {self.hunger}/100")
        print(f"Stomach: {self.stomach}")
        print(f"Knowledge: {self.knowledge}")

    def eat(self) -> None:
        eat(self)

    def play(self, toy: str) -> None:
        play(self, toy)

    def save(self) -> None:
        with open(f"{self.name}.json", 'w') as f:
            json.dump(self.__dict__, f)

    @classmethod
    def load(cls, name) -> 'Pet' or None:
        try:
            with open(f"{name}.json", 'r') as f:
                attributes = json.load(f)
                pet = cls(name)
                pet.__dict__.update(attributes)
                return pet
        except FileNotFoundError:
            print(f"No pet named '{name}' found.")
            return None
