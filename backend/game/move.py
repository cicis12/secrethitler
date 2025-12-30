from pydantic import BaseModel
from typing import List, Union

class Move(BaseModel):
    moveType: str
    cardType: char = None
    newPresident: int = None
    newChancellor: int = None
    playerToKill: int = None