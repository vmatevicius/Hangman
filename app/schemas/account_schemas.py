from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    username: str
    name: str
    surname: str
    password: str
    email: EmailStr

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "xxxAntanasxxx",
                "name": "Antantas",
                "surname": "Fontanas",
                "password": "1234",
                "email": "antantas123@gmail.com",
            }
        }


class AccountResponse(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    password: str
    email: EmailStr
    games_played_count: int
    games_won_count: int
    games_lost_count: int
    correct_guess_count: int
    wrong_guess_count: int
    highest_achieved_score: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "xxxAntanasxxx",
                "name": "Antantas",
                "surname": "Fontanas",
                "password": "1234",
                "email": "antantas123@gmail.com",
                "games_played_count": 0,
                "games_won_count": 0,
                "games_lost_count": 0,
                "correct_guess_count": 0,
                "wrong_guess_count": 0,
                "highest_achieved_score": 0,
            }
        }


class AccountUpdate(BaseModel):
    username: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    games_played_count: Optional[int]
    games_won_count: Optional[int]
    games_lost_count: Optional[int]
    correct_guess_count: Optional[int]
    wrong_guess_count: Optional[int]
    highest_achieved_score: Optional[int]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "xxxAntanasxxx",
                "name": "Antantas",
                "surname": "Fontanas",
                "password": "1234",
                "email": "antantas123@gmail.com",
                "games_played_count": 0,
                "games_won_count": 0,
                "games_lost_count": 0,
                "correct_guess_count": 0,
                "wrong_guess_count": 0,
                "highest_achieved_score": 0,
            }
        }
