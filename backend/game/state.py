from pydantic import BaseModel
from typing import List, Any
class State(BaseModel):
    numOfPlayers: int
    roles: List[char]
    policyTiles: List[char]
    discardPile: List[char]
    numberOfLiberalPolicies: int
    numberOfFascistPolicies: int
    currentPresident: int
    currentChancellor: int
    prevChancellor: int
    numOfDeadPlayers: int
    isDead: List[bool]
    lastPlacedPolicy: char 
    calendarState: int
    prevPresidentCandidate: int
