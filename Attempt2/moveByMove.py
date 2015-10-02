#logic for connect-factour game
import random

# Here's what our JSON object might look like:

game_state={"grid": [
                    [ [54,""],[56,"X"],[63,"X"],[64,"O"],[72,""],[81,""] ],
                    [ ... ],
                    [ ... ],
                    [ ... ],
                    [ ... ],
                    [ [1,""],[2,""],[3,""],[4,"O"],[5,""],[6,"X"] ],
                    ],
            "coin1": 7,
            "coin2": 5,
            "upNext": "X",
            "gameOver": False
            }

def isMoveLegal(current_game_state, (coin1, coin2)):
    """ INPUT: json object representing the current game state,
    tuple with integers for coin1 and coin2 selected 
    
    OUTPUT: (True, "") if the move is legal, (False, "error message") if not
    """

    # step 1: check that one coin stayed the same
    if coin1 != current_game_state["coin1"] and coin2 != current_game_state["coin2"]:
        error_message = "Sorry, that move is illegal, please try again. You can only change one of the numbers from the number line."
        return (False, error_message)

    # step 2: check that the product is unclaimed in the grid
    product = coin1*coin2
    grid = current_game_state["grid"]
    for r in range(6):
        for c in range(6):
            if grid[r][c][0] == product:
                if square[1] != "":
                    error_message = "Sorry, that move is illegal, please try again. That square is already taken"
                    return (False, error_message)

    return (True, "")

## THIS FUNCTION IS NOT DONE OR CORRECT (just copy-pasted so far)
def isGameOver(current_game_state):
    #horizontal
    grid = current_game_state["grid"]
    for row in grid:
        ownerList = [gs.owner for gs in row]
        for x in xrange(3):
            if row[x].isTaken:
                owner = ownerList[x]
            else:
                continue
            if ownerList[x+1] == owner and ownerList[x+2] == owner and ownerList[x+3] == owner:
                self.isOver = True
                self.winner = owner
                return True

    #vertical
    for x in range(6): #go through every column
        ownerList = [grid[y][x].owner for y in xrange(6)]
        for y in range(3): #we only need to look starting at the top three rows
            if grid[y][x].isTaken:
                owner = ownerList[y]
            else:
                continue
            if ownerList[y+1] == owner and ownerList[y+2] == owner and ownerList[y+3] == owner:
                self.isOver = True
                self.winner = owner
                return True


    #diagonal
    for y in xrange(3):
        for x in xrange(3): 
            if grid[y][x].isTaken:
                owner = grid[y][x].owner
            else:
                continue
            if owner == grid[y+1][x+1].owner and owner == grid[y+2][x+2].owner  and owner == grid[y+3][x+3].owner : 
                self.isOver = True
                self.winner = owner
                return True

    for y in xrange(3,6):
        for x in xrange(3): 
            if grid[y][x].isTaken:
                owner = grid[y][x].owner
            else:
                continue
            if owner == grid[y-1][x+1].owner  and owner == grid[y-2][x+2].owner  and owner == grid[y-3][x+3].owner : 
                self.isOver = True
                self.winner = owner
                return True




productSet = set()
for i in xrange(1,10):
    for j in xrange(1,10):
        productSet.add(i*j)

productList = sorted(productSet)

## 
## class gridSquare():
##     def __init__(self, y, x, number):
##         self.y = y
##         self.x = x
##         self.number = number
##         self.isTaken = False
##         self.owner = None
## 
##     def take(self, gamer): #called when someone legally takes this square
##         self.isTaken = True
##         self.owner = gamer
## 
##     def text(self): #what should show up in the square
##         if self.isTaken:
##             return self.owner.letter
##         return str(self.number)
## 
## 
## class game():
##     def __init__(self, gamer1, gamer2, gameID=None):
##         self.gamer1 = gamer1
##         self.gamer2 = gamer2 #instances of the gamer class
##         self.gameID = gameID #for later when we have a database
##         self.grid = [[],[],[],[],[],[]]
##         myProductList = productList[:]
##         for y in xrange(6):
##             for x in xrange(5,-1,-1):
##                 self.grid[y].insert(0, gridSquare(y, x, myProductList[-1]))
##                 myProductList.pop()
##         self.factor0 = random.randint(1,9)
##         self.factor1 = random.randint(1,9)
##         self.turn = self.gamer1
##         self.isOver = False
##         self.winner = None
## 
##     def isGameOver(self):
##         #horizontal
##         for row in self.grid:
##             ownerList = [gs.owner for gs in row]
##             for x in xrange(3):
##                 if row[x].isTaken:
##                     owner = ownerList[x]
##                 else:
##                     continue
##                 if ownerList[x+1] == owner and ownerList[x+2] == owner and ownerList[x+3] == owner:
##                     self.isOver = True
##                     self.winner = owner
##                     return True
## 
##         #vertical
##         for x in range(6): #go through every column
##             ownerList = [self.grid[y][x].owner for y in xrange(6)]
##             for y in range(3): #we only need to look starting at the top three rows
##                 if self.grid[y][x].isTaken:
##                     owner = ownerList[y]
##                 else:
##                     continue
##                 if ownerList[y+1] == owner and ownerList[y+2] == owner and ownerList[y+3] == owner:
##                     self.isOver = True
##                     self.winner = owner
##                     return True
## 
## 
##         #diagonal
##         for y in xrange(3):
##             for x in xrange(3): 
##                 if self.grid[y][x].isTaken:
##                     owner = self.grid[y][x].owner
##                 else:
##                     continue
##                 if owner == self.grid[y+1][x+1].owner and owner == self.grid[y+2][x+2].owner  and owner == self.grid[y+3][x+3].owner : 
##                     self.isOver = True
##                     self.winner = owner
##                     return True
## 
##         for y in xrange(3,6):
##             for x in xrange(3): 
##                 if self.grid[y][x].isTaken:
##                     owner = self.grid[y][x].owner
##                 else:
##                     continue
##                 if owner == self.grid[y-1][x+1].owner  and owner == self.grid[y-2][x+2].owner  and owner == self.grid[y-3][x+3].owner : 
##                     self.isOver = True
##                     self.winner = owner
##                     return True
## 
## 
##     def isLegal(self, whichFactor, newFactor):
##         if whichFactor == 0:
##             oldFactor = self.factor1
##         elif whichFactor == 1:
##             oldFactor=self.factor0
## 
##         #figure out which number was taken
##         number = oldFactor*newFactor
## 
##         for y in range(6):
##             for x in range(6):
##                 if self.grid[y][x].number == number:
##                     if self.grid[y][x].isTaken:
##                         return False
##                     return True
## 
##     def executeMove(self, gamer, whichFactor, newFactor): #whichFactor is 0 or 1
##         #changing the coins on the factor line
##         if whichFactor == 0:
##             self.factor0 = newFactor
##         elif whichFactor == 1:
##             self.factor1 = newFactor
## 
##         #figure out which number was taken
##         number = self.factor0*self.factor1
## 
##         #switch whose turn it is
##         if gamer == self.gamer1:
##             self.turn = self.gamer2
##         else:
##             self.turn = self.gamer1
## 
##         #changing the square in the grid
##         for y in range(6):
##             for x in range(6):
##                 if self.grid[y][x].number == number:
##                     self.grid[y][x].take(gamer)
##         self.isGameOver()
## 
## 
##     def textBoard(self):
##         for row in self.grid:
##             print [gs.text() for gs in row]
## 
##         print "Factor0 = "+str(self.factor0)
##         print "Factor1 = "+str(self.factor1)
## 
## class gamer():
##     def __init__(self, letter):
##         self.letter = letter #'X' or 'O'
##         self.myTurn = False
## 
## 
## def playTextGame():
##     player1 = gamer('X')
##     player2 = gamer('O')
##     myGame = game(player1, player2)
## #    for i in xrange(3):
## #        myGame.grid[3-i][i+1].take(player2)
##     myGame.textBoard()
##     while myGame.isOver == False:
##         currentPlayer = myGame.turn
##         whichFactor = int(raw_input("Player "+currentPlayer.letter+", which factor do you want to change (0, 1)? "))
##         newFactor = int(raw_input("What do you want to change it to?"))
##         if myGame.isLegal(whichFactor, newFactor):
##             myGame.executeMove(currentPlayer, whichFactor, newFactor)
##             myGame.textBoard()
##             if myGame.isOver:
##                 print "Player "+myGame.winner.letter+" wins!"
##                 return None
##         else:
##             print ("Sorry!That move won't work!")
## 
## 
## #playTextGame()
## 
## 
## 
## 
## 
## 
## 
