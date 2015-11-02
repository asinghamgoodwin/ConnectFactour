import random

# Here's what our JSON object might look like:
# (also used for testing)

game_state={"grid": [
                    [ [54,""],[56,"X"],[63,""],[64,"X"],[72,"X"],[81,""] ],
                    [ [36,""],[40,"X"],[42,"O"],[45,""],[48,""],[49,""] ],
                    [ [25,""],[27,""],[28,""],[30,"O"],[32,""],[35,""] ],
                    [ [15,""],[16,"X"],[18,""],[20,""],[21,"O"],[24,""] ],
                    [ [7,""],[8,"O"],[9,""],[10,""],[12,""],[14,"O"] ],
                    [ [1,"O"],[2,""],[3,""],[4,"O"],[5,""],[6,"X"] ],
                    ],
            "coin1": 7,
            "coin2": 5,
            "upNext": "X",
            "gameOver": False
            }

def itWasMyTurn(upNext, player):
    return upNext == player

def isMoveLegal(current_game_state, (coin1, coin2)):
    """ INPUT: json object representing the current game state,
    tuple with integers for coin1 and coin2 selected 
    
    OUTPUT: (True, "") if the move is legal, (False, "error message") if not
    """

    # step 1: check that one coin stayed the same
    prevCoin1 = current_game_state["coin1"]
    prevCoin2 = current_game_state["coin2"]
    if (coin1 != prevCoin1 and coin1 != prevCoin2 and coin2 != prevCoin1 and coin2 != prevCoin2):
        error_message = "Illegal Move! You can only change one of the numbers."
        return (False, error_message)

    # step 2: check that the product is unclaimed in the grid
    product = int(coin1)*int(coin2)
    grid = current_game_state["grid"]
    for r in range(6):
        for c in range(6):
            if grid[r][c][0] == product:
                if grid[r][c][1] != "":
                    error_message = "Illegal Move! That square is already taken."
                    return (False, error_message)

    return (True, "")


def isGameOver(current_game_state):
    """ INPUT: json object representing the current game state
    
    OUTPUT: (Boolean, str) indicating whether the game is over
    and who the winner is (empty str if game isn't over)
    """

    #horizontal
    grid = current_game_state["grid"]
    for row in grid:
        ownerList = [gs[1] for gs in row]
        for i in xrange(3):
            if ownerList[i] != "":
                owner = ownerList[i]
            else:
                continue
            if ownerList[i+1] == owner and ownerList[i+2] == owner and ownerList[i+3] == owner:
                isOver = True
                winner = owner
                return (isOver, winner)

    #vertical
    for x in range(6): #go through every column
        ownerList = [grid[y][x][1] for y in xrange(6)]
        for y in range(3): #we only need to look starting at the top three rows
            if ownerList[y] != "":
                owner = ownerList[y]
            else:
                continue
            if ownerList[y+1] == owner and ownerList[y+2] == owner and ownerList[y+3] == owner:
                isOver = True
                winner = owner
                return (isOver, winner)


    #diagonal
    for y in xrange(3):
        for x in xrange(3): 
            if grid[y][x][1] != "":
                owner = grid[y][x][1]
            else:
                continue
            if owner == grid[y+1][x+1][1] and owner == grid[y+2][x+2][1] and owner == grid[y+3][x+3][1] : 
                isOver = True
                winner = owner
                return (isOver, winner)

    for y in xrange(3,6):
        for x in xrange(3): 
            if grid[y][x][1]:
                owner = grid[y][x][1]
            else:
                continue
            if owner == grid[y-1][x+1][1] and owner == grid[y-2][x+2][1] and owner == grid[y-3][x+3][1]: 
                isOver = True
                winner = owner
                return (isOver, winner)

    return (False, "")


## print "Tests!!!"
## print isMoveLegal(game_state, (7,1))[0] == True
## print isMoveLegal(game_state, (4,7))[0] == True
## print isMoveLegal(game_state, (7,9))[0] == False
## print isMoveLegal(game_state, (4,1))[0] == False

## print itWasMyTurn(game_state["upNext"], 'O') == False
## print itWasMyTurn(game_state["upNext"], 'X') == True

## print isGameOver(game_state)

