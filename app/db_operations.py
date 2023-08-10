from os import path
from typing import List, Dict
from app.models.account_model import Account
from app import db
import logging
import logging.config

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


def get_account(id: int) -> Account:
    account = Account.query.get(id)
    return account


def get_all_accounts() -> Account:
    accounts = Account.query.all()
    return accounts


def create_account(
    username: str, name: str, surname: str, hashed_password: str, email: str
) -> Account:
    account = Account(
        username=username,
        name=name,
        surname=surname,
        password=hashed_password,
        email=email,
    )
    db.session.add(account)
    db.session.commit()

    return account


def retrieve_accounts_game_data(accounts: List[Account]) -> List[Dict[str, int]]:
    unsorted_user_score_data = [
        {
            "username": account.username,
            "score": account.score,
            "games_won": account.games_won_count,
            "games_played": account.games_played_count,
            "games_lost": account.games_lost_count,
        }
        for account in accounts
    ]
    return unsorted_user_score_data


def get_account_by_username(username: str) -> Account:
    account = Account.query.filter_by(username=username).first()
    return account


def update_account_after_lost_game(
    account: Account, good_guesses: int, wrong_guesses: int
) -> bool:
    account.games_played_count += 1
    account.games_lost_count += 1
    account.correct_guess_count += good_guesses
    account.wrong_guess_count += wrong_guesses
    db.session.commit()
    return True


def update_account_after_won_game(
    account: Account, good_guesses: int, wrong_guesses: int, points: int
) -> bool:
    account.games_played_count += 1
    account.games_won_count += 1
    account.correct_guess_count += good_guesses
    account.wrong_guess_count += wrong_guesses
    account.score += points
    db.session.commit()
    return True
