from pydantic import BaseModel
from typing import List


class Participant(BaseModel):
    name: str
    power: int


class Battle(BaseModel):
    id: int
    participants: List[Participant]
    winner: str = None
