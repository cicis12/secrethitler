from game.move import Move
from game.state import State
from pydantic import BaseModel
import random
class InvalidMoveError(Exception):
    pass
def reshuffle(state: State):
    discard_copy = state.discardPile.copy()
    state.discardPile.clear()
    random.shuffle(discard_copy)
    state.policyTiles = state.discardPile+state.policyTiles

#to be deleted
def DrawCards(state: State):
    if len(state.policyTiles) < 3:
        reshuffle(state)
    cards= []
    cards.add(state.policyTiles.pop())
    cards.add(state.policyTiles.pop())
    cards.add(state.policyTiles.pop())
    reutrn cards

def PlaceCard(state: State, cardType):
    if cardType == "L":
       state.numberOfLiberalPolicies+=1
    else:
        state.numberOfFascistPolicies+=1

def NewGov(state: State, newChancellor, newPresident):
    state.currentChancellor=move.newChancellor
    state.currentPresident=move.newPresident

def PlaceRandom(state: State):
    if len(state.policyTiles) < 1:
        reshuffle(state)
    card=state.policyTiles.pop()
    if card == 'L':
        state.numberOfLiberalPolicies+=1
    else:
        state.numberOfFascistPolicies+=1

def KillPlayer(state: State, playerToKill):
    try:
        if not state.isDead[move.playerToKill]:
            state.isDead[move.playerToKill] = True
        else:
            raise InvalidMoveError(
                f"Player tried to kill an already-dead player {move.playerToKill}"
            )
    except IndexError:
        raise InvalidMoveError("Invalid killPlayer index")

    
