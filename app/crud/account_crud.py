from typing import List, Optional

from models.account_model import Account
from schemas.account_schemas import AccountCreate, AccountUpdate
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound


def create_account(db: Session, account: AccountCreate) -> Account:
    db_account = Account(
        username=account.username,
        name=account.name,
        surname=account.surname,
        password=account.password,
        email=account.email,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def read_account(db: Session, account_id: int) -> Optional[Account]:
    if account := db.query(Account).filter(Account.id == account_id).first():
        return account
    else:
        raise NoResultFound


def update_account(
    db: Session,
    account_id: int,
    account: AccountUpdate,
) -> Optional[Account]:
    db_account = read_account(db, account_id)
    if db_account:
        account_update = account.model_dump(exclude_unset=True)
        for key, value in account_update.items():
            setattr(db_account, key, value)
        db.commit()
        return db_account
    else:
        raise NoResultFound


def delete_account(db: Session, account_id: int) -> Optional[Account]:
    account = read_account(db, account_id)
    if account:
        db.delete(account)
        db.commit()
        return account
    else:
        raise NoResultFound


def read_all_accounts(db: Session) -> List[Account]:
    accounts = db.query(Account).all()
    if accounts:
        return accounts
    else:
        raise NoResultFound


def get_account_by_email(db: Session, email: str) -> Optional[Account]:
    db_account = db.query(Account).filter(Account.email == email).first()
    if db_account:
        return True
    else:
        return False
