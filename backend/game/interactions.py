from game.board import *
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

def elections(state: State, presidentCandidate):
    #to be moved to the game engine

    #presidentCandidate = (state.prevPresidentCandidate + 1) % state.numOfPlayers
    #if(state.isDead[presidentCandidate]):
    #    while(state.isDead[presidentCandidate]):
    #        presidentCandidate = (presidentCandidate + 1) % state.numOfPlayers


    #render: show the presidential candidate
    #note: print() is temporary, remove when adding rendering
    print(f"Player {presidentCandidate} is now running for president. Player {presidentCandidate}, choose your chancellor")
    
    #ASK: ask for chancellor selection
    chancellorCandidate = input(f"Player {presidentCandidate}, choose your chancellor")

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
    
    #handling election results
    electionOutcome = vote(presidentCandidate,chancellorCandidate,state)
    if electionOutcome == 'Y':
        NewGov(state,chancellorCandidate,presidentCandidate)
    else:
        state.calendarState+=1
        if(state.calendarState==3):
            state.calendarState=0
            PlaceRandom(state)
            
def legislativeSession(state: State):
    cards = DrawCards(state)
    #render: show the cards to the president
    #note: print() is temporary
    print(f"President (Player {state.currentPresident}), these are the cards you've drawn")
    for i in range(0,3):
        print(f"{i+1}: {cards[i]}")

    #ASK: ask the president for  1/3 cards to be discarded
    selection = input(f"Choose one of these cards to be discarded (1/2/3)")
    
    assert 0<selection<=3, "Selection out of bounds"
    state.discardPile.add(cards.pop(selection))

    #render: show the cards to the chancellor
    #note: print() is temporary
    print(f"Chancellor (Player {state.currentChancellor}), these are the cards you've been given")
    for i in range(0,2):
        print(f"{i+1}: {cards[i]}")


    if not state.vetoRight:
        #ASK: ask the chancellor for 1/2 to be discarded
        selection = input(f"Choose one of these cards to be discarded (1/2)")

        assert 0<selection<=2, "Selection out of bounds"
        state.discardPile.add(cards.pop(selection))

        #render: put the card on the board
        #note: print() is temporary, for debugging
        print(f"A {cards[0]} policy has been introduced")

        PlaceCard(state,cards.pop())
    else:
        #ASK: ask the chancellor for 1/2 or 2/2 to be discarded
        selection=input(f"Choose one or both cards to be discarded (1/2/1 2)")
        selection = selection.strip().split()
        if(len(selection) == 2):
            state.discardPile.add(cards.pop())
            state.discardPile.add(cards.pop())
            print(f"All policies have been vetoed.")
        else:

            assert 0<selection<=2, "Selection out of bounds"
            state.discardPile.add(cards.pop(selection))

            #render: put the card on the board
            #note: print() is temporary, for debugging
            print(f"A {cards[0]} policy has been introduced")
        
            PlaceCard(state,cards.pop())

