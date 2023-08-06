from database.db import Base
from sqlalchemy import Column, Integer, String


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, index=True, nullable=False)
    games_played_count = Column(Integer, default=0)
    games_won_count = Column(Integer, default=0)
    games_lost_count = Column(Integer, default=0)
    correct_guess_count = Column(Integer, default=0)
    wrong_guess_count = Column(Integer, default=0)
    highest_achieved_score = Column(Integer, default=0)
