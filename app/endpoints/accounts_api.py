import crud.account_crud
from database.db import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas.account_schemas import AccountResponse, AccountCreate, AccountUpdate

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

router = APIRouter()


@router.post("", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    if crud.account_crud.get_account_by_email(db, email=account.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.account_crud.create_account(db=db, account=account)


@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    try:
        db_account = crud.account_crud.read_account(db, account_id)
        return db_account
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Account not found")


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int, account: AccountUpdate, db: Session = Depends(get_db)
):
    try:
        db_account = crud.account_crud.update_account(db, account_id, account)
        return db_account
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Account not found")


@router.delete("/{account_id}", response_model=AccountResponse)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    try:
        db_account = crud.account_crud.delete_account(db, account_id)
        return db_account
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Account not found")


@router.get("", response_model=AccountResponse)
def read_accounts(db: Session = Depends(get_db)):
    db_accounts = crud.account_crud.read_all_accounts(db)
    if db_accounts:
        return db_accounts
    raise HTTPException(status_code=404, detail="No accounts found")
