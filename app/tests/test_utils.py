from typing import List
import unittest
import utils
from tests.data_for_tests.utils_test_data import amphibians


class TestUtils(unittest.TestCase):
    def test_get_random_animal_type(self):
        self.assertIn(
            utils.get_random_animal_type(),
            ["amphibians", "birds", "mammals", "reptiles", "vertebrates"],
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

    def test_get_easy_image_path(self):
        self.assertEqual(
            utils.get_easy_image_path(number_of_tries=3), "/static/stages/easy/3.png"
        )
        self.assertNotEqual(utils.get_easy_image_path(number_of_tries=2), "cats")
        self.assertIsInstance(utils.get_easy_image_path(number_of_tries=1), str)

    def test_get_medium_image_path(self):
        self.assertEqual(
            utils.get_medium_image_path(number_of_tries=3),
            "/static/stages/medium/3.png",
        )
        self.assertNotEqual(utils.get_medium_image_path(number_of_tries=2), "cats")
        self.assertIsInstance(utils.get_medium_image_path(number_of_tries=1), str)

    def test_get_hard_image_path(self):
        self.assertEqual(
            utils.get_hard_image_path(number_of_tries=3), "/static/stages/hard/3.png"
        )
        self.assertNotEqual(utils.get_hard_image_path(number_of_tries=2), "cats")
        self.assertIsInstance(utils.get_hard_image_path(number_of_tries=1), str)

    def test_create_game_board(self):
        self.assertEqual(utils.create_game_board(lenght=5), ["_", "_", "_", "_", "_"])
        self.assertNotEqual(utils.create_game_board(lenght=5), "cats")
        self.assertIsInstance(utils.create_game_board(lenght=5), List)


if __name__ == "__main__":
    unittest.main()
