import logging
import logging.config
import random
from os import path
from typing import List, Literal

from flask import flash, redirect, render_template, request

from app.db_operations import DBoperations
from app.models.account_model import Account

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")

db_operations = DBoperations()

class Utilities:

    def get_credit_count(self, difficulty: Literal["easy", "medium", "hard"]) -> int:
        try: 
            if difficulty == "easy":
                return 5
            if difficulty == "medium":
                return 10
            if difficulty == "hard":
                return 15
        except Exception as e:
                logger.error(e)    
    def get_valid_leter(self, word: str, free_letters: str) -> str:
        while True:
            try:
                letter = word[random.randint(0,len(word) -1)]
                if letter in free_letters:
                    return letter
                else:
                    continue
            except Exception as e:
                logger.error(e)
    
    def get_true_or_false_value(self) -> bool:
        try:
            random_number = random.randint(1,3)
            if random_number == 1:
                return True
            else:
                return False
        except Exception as e:
            logger.error(e)
    
    def get_random_animal_type(self) -> str:
        try:
            types = ["amphibians", "birds", "mammals", "reptiles"]
            return types[random.randint(0, 3)]
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
        while True:
            try:
                animals[random.randint(0, len(animals) - 1)]
                if animals != None:
                    return animals[random.randint(0, len(animals) - 1)]
                else:
                    continue
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

    def launch_game(self, tries: int, difficulty: Literal["easy", "medium", "hard"],user: Account,) -> str:
        global good_guesses
        global wrong_guesses
        global word_to_guess
        global wrong_letters
        global empty_spots
        global visuals
        global animal_type
        global usable_letters
        global current_tries
        current_tries = tries

        good_guesses = 0
        wrong_guesses = 0

        usable_letters = "abcdefghijklmnopqrstuvwxyz"
        animal_type = self.get_random_animal_type()
        word_to_guess = self.get_random_animal(self.get_animals(animal_type))
        wrong_letters = []
        empty_spots = len(word_to_guess)
        visuals = self.create_game_board(len(word_to_guess))
        image = self.get_image_path(tries, difficulty)

        return render_template(
            f"{difficulty}.html",
            animal_type=animal_type,
            tries=tries,
            wrong_letters=wrong_letters,
            visuals=visuals,
            usable_letters=usable_letters,
            image=image,
            user=user,
        )

    def add_letter(self, difficulty: Literal["easy", "medium", "hard"], user: Account, points: int) -> str:
        global wrong_guesses
        global word_to_guess
        global wrong_letters
        global empty_spots
        global visuals
        global animal_type
        global good_guesses
        global usable_letters
        global current_tries

        ticket = 0

        guess = request.form["letter"]
        usable_letters = usable_letters.replace(guess, "")
        succeeded = False
        for index, letter in enumerate(word_to_guess):
            if letter == guess:
                good_guesses += 1
                succeeded = True
                visuals[index] = letter
                empty_spots -= 1
        if succeeded == False:
            wrong_letters.append(guess)
            wrong_guesses += 1
            current_tries -= 1
            if current_tries == 0:
                db_operations.update_account_after_lost_game(
                    user, good_guesses, wrong_guesses
                )
                flash(f"Secret word was - {word_to_guess}", "danger")
                return redirect("/defeat")
        if empty_spots == 0:
            if self.get_true_or_false_value == True:
                ticket = 1
            credits = self.get_credit_count(difficulty)
            db_operations.update_account_after_won_game(
                user, good_guesses, wrong_guesses, points, ticket, credits
            )
            flash(f"Secret word was - {word_to_guess}", "danger")
            return redirect("/victory")

        image = self.get_image_path(current_tries, difficulty)

        return render_template(
            f"{difficulty}.html",
            animal_type=animal_type,
            tries=current_tries,
            wrong_letters=wrong_letters,
            visuals=visuals,
            usable_letters=usable_letters,
            image=image,
            user=user,
        )
        
    def reveal_letter(self, difficulty: Literal["easy", "medium", "hard"], user: Account, points: int) -> str:
        global wrong_guesses
        global word_to_guess
        global wrong_letters
        global empty_spots
        global visuals
        global animal_type
        global good_guesses
        global usable_letters
        global current_tries
        
        if user.reveal_ticket == 0:
            flash(f"Not enough reveal tickets", "danger")
        if user.reveal_ticket > 0:
            revealed_letter = self.get_valid_leter(word_to_guess, usable_letters)
            usable_letters = usable_letters.replace(revealed_letter, "")
            for index, letter in enumerate(word_to_guess):
                if letter == revealed_letter:
                    visuals[index] = letter
                    empty_spots -= 1
            db_operations.remove_user_ticket(user)
        
        if empty_spots == 0:
            if self.get_true_or_false_value == True:
                ticket = 1
            else:
                ticket = 0
            credits = self.get_credit_count(difficulty)
            db_operations.update_account_after_won_game(
                user, good_guesses, wrong_guesses, points, ticket, credits
            )
            flash(f"Secret word was - {word_to_guess}", "danger")
            return redirect("/victory")

        image = self.get_image_path(current_tries, difficulty)
        
        return render_template(
            f"{difficulty}.html",
            animal_type=animal_type,
            tries=current_tries,
            wrong_letters=wrong_letters,
            visuals=visuals,
            usable_letters=usable_letters,
            image=image,
            user=user,
        )