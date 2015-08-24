#logic for connect-factour game
import random

#grid = [[],[],[],[],[],[]]

productSet = set()
for i in xrange(1,10):
    for j in xrange(1,10):
        productSet.add(i*j)

# print len(productSet)
productList = sorted(productSet)
#print productList

class gridSquare():
    def __init__(self, y, x, number):
        self.y = y
        self.x = x
        self.number = number
        self.isTaken = False
        self.owner = None

    def take(self, gamer): #called when someone legally takes this square
        self.isTaken = True
        self.owner = gamer

    def text(self): #what should show up in the square
        if self.isTaken:
            return self.owner
        return str(self.number)

#for y in xrange(6):
#    for x in xrange(5,-1,-1):
#        grid[y].insert(0, gridSquare(y, x, productList[-1]))
#        productList.pop()

#for row in grid:
#    print [gs.number for gs in row]


class game():
    def __init__(self, gamer1, gamer2, gameID=None):
        self.gamer1 = gamer1
        self.gamer2 = gamer2 #instances of the gamer class
        self.gameID = gameID #for later when we have a database
        self.grid = [[],[],[],[],[],[]]
        myProductList = productList[:]
        for y in xrange(6):
            for x in xrange(5,-1,-1):
                self.grid[y].insert(0, gridSquare(y, x, myProductList[-1]))
                myProductList.pop()
        self.factor0 = random.randint(1,9)
        self.factor1 = random.randint(1,9)
        self.factors = [self.factor0, self.factor1]

    def executeMove(self, gamer, whichFactor, newFactor): #whichFactor is 0 or 1
        #changing the coins on the factor line
        self.factors[whichFactor] = newFactor
        number = self.factor0*self.factor1

        #changing the square in the grid
        for y in range(6):
            for x in range(6):
                if self.grid[y][x].number == number:
                    self.grid[y][x].take(gamer)

    def textBoard(self):
        for row in self.grid:
            print [gs.text() for gs in row]

        print "Factor0 = "+str(self.factor0)
        print "Factor1 = "+str(self.factor1)

class gamer():
    def __init__(self, letter):
        self.letter = letter #'X' or 'O'
        self.myTurn = False


def playTextGame():
    player1 = gamer('X')
    player2 = gamer('O')
    myGame = game(player1, player2)
    myGame.textBoard()
    whichFactor = int(raw_input("Player1, which factor do you want to change (0, 1)? "))
    newFactor = int(raw_input("What do you want to change it to?"))
    myGame.executeMove(player1,whichFactor, newFactor)
    myGame.textBoard()











