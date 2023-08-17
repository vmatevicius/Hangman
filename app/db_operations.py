import logging
import logging.config
from os import path
from typing import Dict, List

from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.account_model import Account

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


class DBoperatorions:
    pass

    def get_account(self, id: int) -> Account:
        try:
            account = Account.query.get(id)
            if account:
                logger.info(f"'{account.username}' account retrieved successfully")
                return account
            else:
                logger.error(
                    f"tried to retrieve account with id '{id}', but it does not exist"
                )
                return None
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"an arror: '{error}' occured while getting account")

    def get_all_accounts(self) -> Account:
        try:
            accounts = Account.query.all()
            logger.info("accounts retrieved successfully")
            return accounts
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"an arror: '{error}' occured while getting all accounts")

    def create_account(
        self, username: str, name: str, surname: str, hashed_password: str, email: str
    ) -> Account:
        try:
            account = Account(
                username=username,
                name=name,
                surname=surname,
                password=hashed_password,
                email=email,
            )
            db.session.add(account)
            db.session.commit()
            logger.info(f"'{account.username}' account created successfully")
            return account
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"an arror: '{error}' occured while creating account")

    def retrieve_accounts_game_data(
        self, accounts: List[Account]
    ) -> List[Dict[str, int]]:
        try:
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
            logger.info(" accounts game data retrieved successfully")
            return unsorted_user_score_data
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while retrieving accounts game data"
            )

    def get_account_by_username(self, username: str) -> Account:
        try:
            account = Account.query.filter_by(username=username).first()
            if account:
                logger.info(f"'{account.username}' account retrieved successfully")
                return account
            else:
                logger.error(
                    f"tried to retrieve account with username '{username}', but it does not exist"
                )
                return None
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while getting account by username"
            )

    def update_account_after_lost_game(
        self, account: Account, good_guesses: int, wrong_guesses: int
    ) -> bool:
        try:
            account.games_played_count += 1
            account.games_lost_count += 1
            account.correct_guess_count += good_guesses
            account.wrong_guess_count += wrong_guesses
            db.session.commit()
            logger.info(f"'{account.username}' loss updated successfully")
            return True
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while updating account after lost game"
            )

    def update_account_after_won_game(
        self, account: Account, good_guesses: int, wrong_guesses: int, points: int
    ) -> bool:
        try:
            account.games_played_count += 1
            account.games_won_count += 1
            account.correct_guess_count += good_guesses
            account.wrong_guess_count += wrong_guesses
            account.score += points
            db.session.commit()
            logger.info(f"'{account.username}' victory updated successfully")
            return True
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while updating account after won game"
            )
