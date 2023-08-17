import logging
import logging.config
import random
from os import path
from typing import List, Literal
from app.routes import render_template, request, flash, redirect, g
from app.models.account_model import Account
from app.db_operations import DBoperatorions

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")

db_operations = DBoperatorions()

EASY_MODE_POINTS = 10
MEDIUM_MODE_POINTS = 20
HARD_MODE_POINTS = 30


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

    def get_image_path(
        self, number_of_tries: int, difficulty: Literal["easy", "medium", "hard"]
    ) -> str:
        try:
            return f"/static/stages/{difficulty}/{number_of_tries}.png"
        except Exception as e:
            logger.error(e)

    def create_game_board(self, lenght: int) -> str:
        try:
            board = ["_" for _ in range(0, lenght)]
            return board
        except Exception as e:
            logger.error(e)

    def launch_game(self, g, tries: int, difficulty: Literal["easy", "medium", "hard"]):
        g.good_guesses = 0
        g.wrong_guesses = 0

        g.usable_letters = "abcdefghijklmnopqrstuvwxyz"
        g.animal_type = self.get_random_animal_type()
        g.word_to_guess = self.get_random_animal(self.get_animals(g.animal_type))
        g.wrong_letters = []
        g.empty_spots = len(g.word_to_guess)
        g.visuals = self.create_game_board(len(g.word_to_guess))
        g.image = self.get_image_path(tries, difficulty)

        print(g.keys())
        return render_template(
            "easy.html",
            animal_type=g.animal_type,
            tries=tries,
            wrong_letters=g.wrong_letters,
            visuals=g.visuals,
            usable_letters=g.usable_letters,
            image=g.image,
        )

    def add_letter(
        self,
        g,
        tries: int,
        difficulty: Literal["easy", "medium", "hard"],
        user: Account,
    ):
        guess = request.form["letter"]
        g.usable_letters = g.usable_letters.replace(guess, "")
        succeeded = False
        for index, letter in enumerate(g.word_to_guess):
            if letter == guess:
                good_guesses += 1
                succeeded = True
                g.visuals[index] = letter
                empty_spots -= 1
        if succeeded == False:
            g.wrong_letters.append(guess)
            wrong_guesses += 1
            tries -= 1
            if tries == 0:
                db_operations.update_account_after_lost_game(
                    user, good_guesses, wrong_guesses
                )
                flash(f"Secret word was - {g.word_to_guess}", "danger")
                return redirect("/defeat")

        if empty_spots == 0:
            db_operations.update_account_after_won_game(
                user, good_guesses, wrong_guesses, EASY_MODE_POINTS
            )
            flash(f"Secret word was - {g.word_to_guess}", "danger")
            return redirect("/victory")

        image = self.get_image_path(tries, difficulty)

        print(g.keys())
        return render_template(
            "easy.html",
            animal_type=g.animal_type,
            tries=tries,
            wrong_letters=g.wrong_letters,
            visuals=g.visuals,
            usable_letters=g.usable_letters,
            image=image,
        )
