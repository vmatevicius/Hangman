import logging
import logging.config
from os import path
from typing import Dict, List

from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.account_model import Account, Transaction

log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")


class DBoperations:
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
        self, username: str, name: str, surname: str, hashed_password: str, email: str, profile_picture: str
    ) -> Account:
        try:
            account = Account(
                username=username,
                name=name,
                surname=surname,
                password=hashed_password,
                email=email,
                profile_picture=profile_picture
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
                    "picture_path": account.profile_picture,
                    "tickets": account.reveal_ticket,
                    "credits": account.credits,
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
        self, account: Account, good_guesses: int, wrong_guesses: int, points: int, ticket: int, credits: int
    ) -> bool:
        try:
            account.games_played_count += 1
            account.games_won_count += 1
            account.correct_guess_count += good_guesses
            account.wrong_guess_count += wrong_guesses
            account.score += points
            account.reveal_ticket += ticket
            account.credits += credits
            db.session.commit()
            logger.info(f"'{account.username}' victory updated successfully")
            return True
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while updating account after won game"
            )

    def remove_user_ticket(self, account: Account ) -> bool:
        try:
            if account.reveal_ticket > 0:
                account.reveal_ticket -= 1
                db.session.commit()
                logger.info(f"'{account.username}' tickets removed successfully")
                return True
            else:
                return False
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while removing tickets"
            )
            
    def get_user_transactions(self, user: Account) -> List[Transaction]:
        try:
            transactions = Transaction.query.filter_by(account_id = user.id)
            logger.info("transactions retrieved successfully")
            return transactions
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"an arror: '{error}' occured while getting all transactions")
            
    def create_transaction(
        self,user: Account, price: int, amount: int) -> Transaction:
        try:
            transaction = Transaction(
                price=price,
                tickets=amount,
                account_id = user.id,
            )
            db.session.add(transaction)
            db.session.commit()
            logger.info(f" transaction for account with id '{transaction.account_id}' created successfully ")
            return transaction
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"an arror: '{error}' occured while creating transaction")
            
    def update_account_after_purchase(
        self, account: Account, tickets: int, credits: int
    ) -> bool:
        try:
            account.reveal_ticket += tickets
            account.credits -= credits
            db.session.commit()
            logger.info(f"'{account.username}' account after purchase updated successfully")
            return True
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while updating account after purchase"
            )
            
    def add_credits(
        self, account: Account, credits: int
    ) -> bool:
        try:
            account.credits += credits
            db.session.commit()
            logger.info(f"credits added to '{account.username}' account successfully")
            return True
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(
                f"an arror: '{error}' occured while adding credits"
            )