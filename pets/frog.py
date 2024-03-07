from pets.pet import Pet


class Frog(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self.species = "frog"
        self.preferred_food = ['.jpg', '.jpeg', '.png']
        self.jump_height = 10

    def show(self):
        super().show()
        print(f"Jump height: {self.jump_height}/100")
        return

    def eat(self):
        super().eat()
        return

    def play(self, toy):
        print(f"{self.name} is jumping around")
        super().play(toy)
        return
