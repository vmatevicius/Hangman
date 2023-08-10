from typing import List
import random


def get_random_animal_type() -> str:
    types = ["amphibians", "birds", "mammals", "reptiles", "vertebrates"]
    return types[random.randint(0, 4)]


def get_animals(animal_type: str) -> List[str]:
    file = f"app/words/{animal_type}.txt"
    with open(file, "r") as word_file:
        words = [word.strip().lower() for word in word_file]
    return words


def get_random_animal(animals: List[str]) -> str:
    return animals[random.randint(0, len(animals) - 1)]


def get_easy_image_path(number_of_tries: int) -> str:
    return f"/static/stages/easy/{number_of_tries}.png"


def get_medium_image_path(number_of_tries: int) -> str:
    return f"/static/stages/medium/{number_of_tries}.png"


def get_hard_image_path(number_of_tries: int) -> str:
    return f"/static/stages/hard/{number_of_tries}.png"


def create_game_board(lenght: int) -> str:
    board = ["_" for _ in range(0, lenght)]
    return board
