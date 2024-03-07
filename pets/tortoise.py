from pets.pet import Pet


class Tortoise(Pet):
    def __init__(self, name: str):
        super().__init__(name)
        self.species = "tortoise"
        self.preferred_food_types = [".txt", ".docx", ".pdf"]
        self.shell_strength = 10

    def show(self) -> None:
        super().show()
        print(f"Shell strength: {self.shell_strength}/100")

    def play(self, toy):
        print(f"{self.name} is too slow to play")
        return
