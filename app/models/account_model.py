from database.db import Base
from sqlalchemy import Column, Integer, String


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False, unique=True)
    games_played_count = Column(Integer)
    game_won_count = Column(Integer)
    games_lost_count = Column(Integer)
    highest_achieved_score = Column(Integer)
    correct_guess_count = Column(Integer)
    wrong_guess_count = Column(Integer)
