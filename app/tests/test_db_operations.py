import unittest
from typing import List
from unittest.mock import MagicMock, patch

import db_operations

from app.models.account_model import Account


class TestUtils(unittest.TestCase):
    @patch("db_operations.Account.query")
    def test_get_account_success(self, mock_query):
        account_id = 1
        mock_account = Account(id=account_id, username="test_user")
        mock_query.get.return_value = mock_account
        result = db_operations.get_account(account_id)

        self.assertEqual(result, mock_account)
        self.assertNotEqual(result, "mock_account")
        self.assertIsInstance(result, Account)
        mock_query.get.assert_called_once_with(account_id)

    @patch("db_operations.Account.query")
    def test_get_account_none(self, mock_query):
        account_id = 0
        mock_query.get.return_value = None

        result = db_operations.get_account(account_id)

        self.assertIsNone(result)
        mock_query.get.assert_called_once_with(account_id)

    @patch("db_operations.Account.query")
    def test_get__all_accounts_success(self, mock_query):
        mock_account_1 = Account(id=1, username="test_user")
        mock_account_2 = Account(id=2, username="test_user_2")
        mock_accounts = [mock_account_1, mock_account_2]
        mock_query.all.return_value = mock_accounts

        result = db_operations.get_all_accounts()

        self.assertEqual(result, mock_accounts)
        self.assertNotEqual(result, "tests")
        self.assertIsInstance(result, List)
        mock_query.all.assert_called_once_with()

    @patch("db_operations.Account.query")
    def test_get__all_accounts_none(self, mock_query):
        mock_query.all.return_value = None

        result = db_operations.get_all_accounts()

        self.assertIsNone(result)
        mock_query.all.assert_called_once_with()

    @patch("db_operations.Account")
    @patch("db_operations.db.session")
    def test_create_account_success(self, mock_session, mock_account):
        username = "test_user"
        name = "Test"
        surname = "User"
        hashed_password = "hashed_password"
        email = "test@example.com"
        mock_account_instance = MagicMock()
        mock_account.return_value = mock_account_instance

        result = db_operations.create_account(
            username, name, surname, hashed_password, email
        )

        self.assertEqual(result, mock_account_instance)
        mock_account.assert_called_once_with(
            username=username,
            name=name,
            surname=surname,
            password=hashed_password,
            email=email,
        )
        self.assertNotEqual(result, "account")
        mock_session.add.assert_called_once_with(mock_account_instance)
        mock_session.commit.assert_called_once()

    def test_retrieve_accounts_game_data(self):
        mock_account_1 = Account(
            username="user1",
            score=100,
            games_won_count=5,
            games_played_count=10,
            games_lost_count=5,
        )
        mock_account_2 = Account(
            username="user2",
            score=150,
            games_won_count=7,
            games_played_count=12,
            games_lost_count=5,
        )
        mock_accounts = [mock_account_1, mock_account_2]

        result = db_operations.retrieve_accounts_game_data(mock_accounts)

        expected_data = [
            {
                "username": "user1",
                "score": 100,
                "games_won": 5,
                "games_played": 10,
                "games_lost": 5,
            },
            {
                "username": "user2",
                "score": 150,
                "games_won": 7,
                "games_played": 12,
                "games_lost": 5,
            },
        ]
        self.assertEqual(result, expected_data)
        self.assertNotEqual(result, ["foo"])
        self.assertIsInstance(result, List)

    @patch("db_operations.Account.query")
    def test_get_account_by_username_success(self, mock_query):
        username = "test_user"
        mock_account = Account(username="test_user")
        mock_query.filter_by.return_value.first.return_value = mock_account

        result = db_operations.get_account_by_username(username)

        self.assertEqual(result, mock_account)
        self.assertNotEqual(result, "mock_account")
        self.assertIsInstance(result, Account)
        mock_query.filter_by.assert_called_once_with(username=username)
        mock_query.filter_by.return_value.first.assert_called_once()

    @patch("db_operations.Account.query")
    def test_get_account_by_username_none(self, mock_query):
        username = "test_user"
        mock_query.filter_by.return_value.first.return_value = None

        result = db_operations.get_account_by_username(username)

        self.assertIsNone(result)
        self.assertNotEqual(result, "foo")
        mock_query.filter_by.assert_called_once_with(username=username)
        mock_query.filter_by.return_value.first.assert_called_once()

    @patch("db_operations.db.session")
    def test_update_account_after_lost_game(self, mock_session):
        mock_account = Account(
            username="test_user",
            games_played_count=5,
            games_lost_count=3,
            correct_guess_count=20,
            wrong_guess_count=10,
        )
        good_guesses = 5
        wrong_guesses = 6
        result = db_operations.update_account_after_lost_game(
            mock_account, good_guesses, wrong_guesses
        )
        self.assertTrue(result)
        self.assertEqual(mock_account.games_played_count, 6)
        self.assertNotEqual(mock_account.games_played_count, 7)
        self.assertEqual(mock_account.games_lost_count, 4)
        self.assertEqual(mock_account.correct_guess_count, 25)
        self.assertEqual(mock_account.wrong_guess_count, 16)
        mock_session.commit.assert_called_once()

    @patch("db_operations.db.session")
    def test_update_account_after_won_game(self, mock_session):
        mock_account = Account(
            username="test_user",
            games_played_count=5,
            games_won_count=3,
            correct_guess_count=20,
            wrong_guess_count=10,
            score=20,
        )
        points = 30
        good_guesses = 5
        wrong_guesses = 6
        result = db_operations.update_account_after_won_game(
            mock_account, good_guesses, wrong_guesses, points
        )
        self.assertTrue(result)
        self.assertEqual(mock_account.games_played_count, 6)
        self.assertNotEqual(mock_account.games_played_count, 7)
        self.assertEqual(mock_account.games_won_count, 4)
        self.assertEqual(mock_account.correct_guess_count, 25)
        self.assertEqual(mock_account.wrong_guess_count, 16)
        self.assertEqual(mock_account.score, 50)
        mock_session.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
