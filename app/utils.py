import logging
import logging.config
import random
from os import path
from typing import List

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


class Utilities:
    pass

    def get_random_animal_type(self) -> str:
        try:
            types = ["amphibians", "birds", "mammals", "reptiles", "vertebrates"]
            return types[random.randint(0, 4)]
        except Exception as e:
            logger.error(e)

    def get_animals(self, animal_type: str) -> List[str]:
        try:
            file = f"app/words/{animal_type}.txt"
            with open(file, "r") as word_file:
                words = [word.strip().lower() for word in word_file]
            return words
        except Exception as e:
            logger.error(e)

    def get_random_animal(self, animals: List[str]) -> str:
        try:
            return animals[random.randint(0, len(animals) - 1)]
        except Exception as e:
            logger.error(e)

    def get_easy_image_path(self, number_of_tries: int) -> str:
        try:
            return f"/static/stages/easy/{number_of_tries}.png"
        except Exception as e:
            logger.error(e)

    def get_medium_image_path(self, number_of_tries: int) -> str:
        try:
            return f"/static/stages/medium/{number_of_tries}.png"
        except Exception as e:
            logger.error(e)

    def get_hard_image_path(self, number_of_tries: int) -> str:
        try:
            return f"/static/stages/hard/{number_of_tries}.png"
        except Exception as e:
            logger.error(e)

    def create_game_board(self, lenght: int) -> str:
        try:
            board = ["_" for _ in range(0, lenght)]
            return board
        except Exception as e:
            logger.error(e)
