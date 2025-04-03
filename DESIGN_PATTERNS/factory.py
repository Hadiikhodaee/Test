from abc import ABC, abstractmethod
from random import choice

class Base(ABC):
    choices = ["r", "p", "s"]
    @abstractmethod
    def take_action(self):
        pass

class Human(Base):
    def take_action(self):
        user_choice = input("R, P or S? =>")
        return user_choice
    
class Computer(Base):
    def take_action(self):
        return choice(self.choices)
    
class Game:
    def start_game():
        game_type = input("S or M? =>").lower()
        if game_type == 's':
            p1 = Human()
            p2 = Computer()
        elif game_type == 'm':
            p1 = Human()
            p2 = Human()

if __name__ == "__main__":
    Game.start_game()