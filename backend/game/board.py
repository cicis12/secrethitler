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


def apply_move(state: State,move: Move) -> State:
    newState = state.copy(deep=True)

    if move.moveType == "DrawCards":
        if len(newState.policyTiles) < 3:
            reshuffle(newState)
        newState.policyTiles.pop()
        newState.policyTiles.pop()
        newState.policyTiles.pop()

    elif move.moveType == "PlaceCard":
        if move.cardType == "L":
            newState.numberOfLiberalPolicies+=1
        else:
            newState.numberOfFascistPolicies+=1

    elif move.moveType == "NewGov":
        newState.currentChancellor=move.newChancellor
        newState.currentPresident=move.newPresident

    elif move.moveType == "PlaceRandom":
        if len(newState.policyTiles) < 1:
            reshuffle(newState)
        card=newState.policyTiles.pop()
        if card == 'L':
            newState.numberOfLiberalPolicies+=1
        else:
            newState.numberOfFascistPolicies+=1
        
    elif move.moveType == "KillPlayer":
        try:
            if not newState.isDead[move.playerToKill]:
                newState.isDead[move.playerToKill] = True
            else:
                raise InvalidMoveError(
                    f"Player tried to kill an already-dead player {move.playerToKill}"
                )
        except IndexError:
            raise InvalidMoveError("Invalid killPlayer index")

    else:
        raise InvalidMoveError(
            f"Unknown move type: {move.moveType}"
        )
    return newState
    
