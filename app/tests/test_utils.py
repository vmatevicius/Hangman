import unittest
from typing import List

from app.utils import Utilities
from app.tests.data_for_tests.utils_test_data import amphibians, valid_leters

utils = Utilities()

class TestUtils(unittest.TestCase):
    def test_get_random_animal_type(self):
        self.assertIn(
            utils.get_random_animal_type(),
            ["amphibians", "birds", "mammals", "reptiles"],
        )
        self.assertNotEqual(utils.get_random_animal_type(), "dog")
        self.assertIsInstance(utils.get_random_animal_type(), str)

    def test_get_animals(self):
        self.assertEqual(utils.get_animals(animal_type="amphibians"), amphibians)
        self.assertNotEqual(utils.get_animals(animal_type="amphibians"), "cats")
        self.assertIsInstance(utils.get_animals(animal_type="amphibians"), List)

    def test_get_random_animal(self):
        self.assertIn(utils.get_random_animal(animals=amphibians), amphibians)
        self.assertNotEqual(utils.get_random_animal(animals=amphibians), "cats")
        self.assertIsInstance(utils.get_random_animal(animals=amphibians), str)

    def test_get_image_path(self):
        self.assertEqual(
            utils.get_image_path(number_of_tries=3, difficulty="easy"), "/static/stages/easy/3.png"
        )
        self.assertNotEqual(utils.get_image_path(number_of_tries=2, difficulty="easy"), "cats")
        self.assertIsInstance(utils.get_image_path(number_of_tries=1, difficulty="easy"), str) 
        
    def test_create_game_board(self):
        self.assertEqual(utils.create_game_board(lenght=5), ["_", "_", "_", "_", "_"])
        self.assertNotEqual(utils.create_game_board(lenght=5), "cats")
        self.assertIsInstance(utils.create_game_board(lenght=5), List)
    
    def test_get_valid_leter(self):
        self.assertIn(utils.get_valid_leter(word="word", free_letters=valid_leters), valid_leters)
        self.assertNotEqual(utils.get_valid_leter(word="word", free_letters=valid_leters), "A")
        self.assertIsInstance(utils.get_valid_leter(word="word", free_letters=valid_leters), str)
        
    def test_get_true_or_false_value(self):
        self.assertIn(utils.get_true_or_false_value(), [True,False])
        self.assertIsInstance(utils.get_true_or_false_value(), bool)
    
    def test_get_credit_count(self):
        self.assertEqual(utils.get_credit_count(difficulty="easy"), 5)
        self.assertEqual(utils.get_credit_count(difficulty="medium"), 10)
        self.assertEqual(utils.get_credit_count(difficulty="hard"), 15)
        self.assertIsInstance(utils.get_credit_count(difficulty="easy"), int)
        
if __name__ == "__main__":
    unittest.main()
