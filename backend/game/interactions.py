from game.board import apply_move
from game.move import Move
from game.state import State
from pydantic import BaseModel
class InvalidInteractionError(Exception):
    pass
def vote(presidentCandidate, chancellorCandidate, state: State):
    #render: show voting
    #note: print() is temporary
    print(f"Players, now place your votes for or against Player {presidentCandidate} as president and Player {chancellorCandidate} as chancellor")
    votes = []
    votesYes=0
    votesNo=0
    #note: this is temporary
    for i in range(0,state.numOfPlayers):
        if state.isDead[i]:
            votes.append("Dead")
            continue
        playerVote=input(f"Player {i}, vote Y/N").upper()
        if playerVote == 'Y':
            votes.append("Y")
            votesYes+=1
        elif playerVote == 'N':
            votes.append("N")
            votesNo+=1
        else:
            raise InvalidInteractionError(
                f"Player {i} inputed an ununderstandable vote {playerVote}"
            )
    #note: print() is temporary, for debugging
    print(f"There were {votesYes} votes for Yes and {votesNo} votes for No")
    print(f"The vote list is:")
    print(votes)
    if votesYes > votesNo:
        #note:print() is temporary
        print(f"The vote has passed")
        return "Y"
    else:
        print(f"The vote hasn't passed")
        return "N"

def elections(state: State):
    presidentCandidate = (state.prevPresidentCandidate + 1) % state.numOfPlayers
    if(state.isDead[presidentCandidate]):
        while(state.isDead[presidentCandidate]):
            presidentCandidate = (presidentCandidate + 1) % state.numOfPlayers
    #render: show the presidential candidate
    #note: print() is temporary, remove when adding rendering
    print(f"Player {presidentCandidate} is now running for president. Player {presidentCandidate}, choose your chancellor")
    chancellorCandidate = ask(presidentCandidate,"chooseChancellor")
    if chancellorCandidate == state.prevChancellor:
        raise InvalidInteractionError(
            f"Player {chancellorCandidate} was the Chancellor the round before, therefore they cannot be nominated again"
        )
    if not 0 <= chancellorCandidate < state.numOfPlayers:
        raise InvalidInteractionError(
            f"Player {chancellorCandidate} doesn't exist (players are numbered [0,{state.numOfPlayers}))"
        )
    #render: show the chosen chancellor
    #note: print() is temporary
    print(f"Player {chancellorCandidate} has been chosen as a candiate for Chancellor.")
    
    electionOutcome = vote(presidentCandidate,chancellorCandidate,state)
    if electionOutcome == 'Y':
        govMove = Move()
        govMove.moveType="NewGov"
        govMove.newChancellor=chancellorCandidate
        govMove.newPresident=presidentCandidate
        apply_move(state,govMove)
    else:
        state.calendarState+=1
        if(state.calendarState==3):
            state.calendarState=0
            randMove= Move()
            randMove.moveType="PlaceRandom"
            apply_move(state,randMove)
            

