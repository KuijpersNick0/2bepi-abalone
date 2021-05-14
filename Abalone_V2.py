import math 
import time
import copy
import random

moves = {
    "NW":[-1, -1],
    "NE":[-1,  0],
    "E" :[ 0,  1],
    "SW":[ 1,  0],
    "SE":[ 1,  1],
    "W" :[ 0, -1]
}

"""
    ...
"""
node_count=0

def minimax(state, depth, maximizer, alpha, beta):
    move = -1
    
    if state.is_terminal():        
        return (-math.inf if maximizer else math.inf), -1
    elif depth == 0:         
        return heuristic(state, maximizer), -1

    if maximizer:       
        score = -math.inf
        # x est l'ancien score, on souhaite savoir si l'ancien score est plus grand que le meilleur score pour maximizer = True
        def shouldReplace(x): return x > score
    else:
        score = math.inf
        # x est l'ancien score, on souhaite savoir si l'ancien score est mieux classé (donc plus petit) que le meilleur score pour maximizer = False
        def shouldReplace(x): return x < score

    successors = state.legal_plays(maximizer) #maximizer c'est le turn
    boards = []

    # state.displayBoard()
    """
        On va parcourir l'ensemble des moves possibles
        Pour chaque move possible, le sélectionner et rappeler la fonction minimax mais avec l'autre joueur et en enlevant 1 de profondeur
        Idem pour la 3ème couche


    """

    if depth == 3:
        print("<<<< FIRST DEPTH >>>>")
    elif depth == 2:
        print("____ second depth ___")
    elif depth == 1:
        print("...")

    R_successors = reversed(successors)

    # for s in R_successors:
    #     print(s)

    for moveName in R_successors:        
        global node_count # permet de modifier une variable publique
        node_count += 1

        copyBoard = copy.deepcopy(state.board)
        newState = Board(copyBoard)

        newState.action(moveName[0], moveName[1], maximizer, True)  
        tempoScore = minimax(newState, depth - 1, not maximizer, alpha, beta)[0]

        if shouldReplace(tempoScore):          
            score = tempoScore
            move = moveName

        if maximizer:
            alpha = max(alpha, tempoScore)
        else:
            beta = min(beta, tempoScore)
        
        if alpha >= beta:
            break

        # print(score, move)

    return score, move

def heuristic(state, maximizer):    
    result = 0
    result += state.population(maximizer)

    if state.winner(maximizer) == True:
        result += 200
    elif state.winner(maximizer) == False:
        result -= 200

    result += 1 / state.closeCenter(maximizer)
    return result


class Board:
    def __init__(self, board):
        self.board = board

    # def new_abalone(self):
    #     copy = self.board
    #     return Board(copy)
    
    def myColor(self, maximizer):
        yourColor= ""
        if maximizer == True:
            yourColor = "W"
        else:
            yourColor = "B"

        return yourColor

    def closeCenter(self, maximizer):
        myColor = self.myColor(maximizer)       
        marbles = set()
        result = 0
        for i,row in enumerate(self.board):         
            for j,value in enumerate(row):
                if value == myColor:
                    marbles.add((i,j))
        
        # for i in marbles:
        #     result += self.distance(i)

        return self.distance(marbles)

    def distance(self, marbles):
        center = [4,4]
        sum = 0

        for marble in marbles:
            rowDistance = abs(marble[0] - center[0])
            colDistance = abs(marble[1] - center[1])

            result = rowDistance + colDistance
            sum += result

        return sum
 

        #dist= sqrt[(x2-x1)^2 +(y2-y1)^2]
        # dist2 = math.sqrt((marble[0] - 4)**2 + (marble[1] - 4)**2)         
        #dist = ((abs(marbles[0] - 4) + abs(marbles[1] - 4))/2)

        # return dist2

    def population(self, maximizer):
        color = self.myColor(maximizer)
        counter = 0

        for i, row in enumerate(self.board):
            for j, value in enumerate(row):
                if value == color:
                    for move in list(moves.values()):
                        try:
                            if self.board[i + move[0]][j + move[1]] == color:
                                counter += 1
                        except:
                            # lorqu'on se trouve aux abords du plateau, on peut recevoir une erreur pour certains mouvements faits
                            pass

        return counter

    def opposingMarblesOut(self, maximizer):
        yourColor = self.myColor(maximizer)
        counter = 0
        opposingColor = ''

        # ! COMMENT FAIRE CETTE CONDITION TERNAIRE ?
        # opposingColor = 'W' if(yourColor == 'B') else opposingColor = 'B'

        if yourColor == 'B':
            opposingColor = 'W'
        else:
            opposingColor = 'B'

        for row in self.board:                
            for box in row:
                if box == opposingColor:
                    counter += 1

        return 14 - counter

    def legal_plays(self, maximizer):        
        color = self.myColor(maximizer)
        allMoves = []      
        chosenBoxes = []
        possibleChains = []
        myMoves = list(moves.keys())
        lengthChains = [1, 2, 3]               

        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if value == color:
                    chosenBoxes.append([i,j])                          
                
        for i in lengthChains:
            for j in chosenBoxes:
                chains = self.possibleChainsFromPoint(i, j, None, None, [], [], possibleDirections=list(moves.values()))                     
                if chains != "notMoveFoundError":
                    for elem in chains:
                        possibleChains.append(elem)                                  

        for chain in possibleChains:               
            for move in myMoves:                           
                if self.action(chain, move, maximizer) is not False:                    
                    allMoves.append((chain,move))
        
        # for move in allMoves:
        #     print(move)
      
        return allMoves

    def is_terminal(self):
        scoreWhite = self.opposingMarblesOut(False)
        scoreBlack = self.opposingMarblesOut(True)

        if scoreBlack == 6 or scoreWhite == 6:
            return True
        
        return False

    def winner(self, maximizer):
            color = self.myColor(maximizer)
            scoreWhite = self.opposingMarblesOut('B')
            scoreBlack = self.opposingMarblesOut('W')
        
            if scoreBlack == 6 and color == "W":
                return True
            elif scoreBlack == 6 and color == "B":
                return False
            elif scoreWhite == 6 and color == "B":
                return True
            elif scoreWhite == 6 and color == "W":
                return False

            return None

    def displayBoard(self):
        """
            Shows the Abalone board.
        """
        chainsult = "\n\t [ CURRENT BOARD ]\n\n"
        for index,row in enumerate(self.board):
            if index == 0 or index == 8:
                chainsult += "        "
            elif index == 1 or index == 7:
                chainsult += "      "
            elif index == 2 or index == 6:
                chainsult += "    "
            elif index == 3 or index == 5:
                chainsult += "  "
            elif index == 5:
                chainsult += ""
            for case in row:
                if case == "X":
                    pass
                elif case == "E":
                    chainsult += " .  "
                else:
                    chainsult += f" {case}  "
            chainsult += "\n"
    
        print(chainsult)

    def existingDirection(self, moveName):
        """
            Checks if the direction exists.
        """
        if moves.get(moveName) is None:
            return False
        return True

    def aligned(self, vector01, vector02):
        """
            Check if 2 vectors are aligned or not.
        """
        sum = [vector01[0] + vector02[0], vector01[1] + vector02[1]]
        product = [2*i for i in vector01]
        if product == sum or sum == [0, 0]:
            return True
    
        return False

    def colored(self, marblesArray, color):
        """
        ! FIX BUGS WITH COLOR    
            Checks if all marbles have the right color.
        """
        for marble in marblesArray:
            if self.board[marble[0]][marble[1]] != 'W' and self.board[marble[0]][marble[1]] != 'B':
                # print("no marble here", marblesArray, marble, self.board[marble[0]][marble[1]])
                return False
            else:
                if self.board[marble[0]][marble[1]] != color:
                    # print("wrong color marble")
                    return False

        return True

    def chain(self, marblesArray, move=None):
        """
            Checks if all marbles are aligned.
        """
        if len(marblesArray) > 3:
            return "lengthChainError"
    
        if len(marblesArray) == 1:
            return move

        marblesArray.sort()
        if move is not None:
            if marblesArray[0] == [marblesArray[1][0] + move[0], marblesArray[1][1] + move[1]]:
                return self.chain(marblesArray[1:], move=move)

        for currentMove in moves.values():
            if marblesArray[0] == [marblesArray[1][0] + currentMove[0], marblesArray[1][1] + currentMove[1]]:
                return self.chain(marblesArray[1:], move=currentMove)
    
        return "marblesChainError"

    def lineMove(self, marblesArray, moveName, opponent=False):
        """
            - Checks the chain\n
            - Checks lhe list (more than one marble ?)\n
            - Checks the alignment between the move and the chain\n
                - Finds the chain's last marble\n
                - Tries to find the next color\n
                    - Next color is out of range, returns an error\n
                    - Next color == 'X' (out of limit), returns an error\n
                    - Next color == actual color ('W' == 'W'), return an error\n
                    - Next color == 'E' (empty), you can move your chain\n
                    - Next color == opposing color, looks at the opponent chain and checks if the box behind the string is empty or out of board
        """
        vectorMove = moves[moveName]
        vectorChain = self.chain(marblesArray)
        lastMarble = marblesArray[0]

        if vectorChain == "lengthChainError" or vectorChain == "marblesChainError":
            return False, "chainError", marblesArray, moveName
    
        if vectorChain == None and opponent is False:
            return "soloMarbleInfo", marblesArray, moveName

        if (self.aligned(vectorMove, vectorChain)):
            if vectorMove == [-1, -1]:
                lastMarble =  min(marblesArray)
            elif vectorMove == [1, 1]:
                lastMarble = max(marblesArray)
            elif vectorMove == [1, 0]:
                for marble in marblesArray[1:]:
                    if marble[0] > lastMarble[0]:
                        lastMarble = marble
            elif vectorMove == [-1, 0]:
                for marble in marblesArray[1:]:
                    if marble[0] < lastMarble[0]:
                        lastMarble = marble
            elif vectorMove == [0, 1]:
                for marble in marblesArray[1:]:
                    if marble[1] > lastMarble[1]:
                        lastMarble = marble
            elif vectorMove == [0, -1]:
                for marble in marblesArray[1:]:
                    if marble[1] < lastMarble[1]:
                        lastMarble = marble
    
            if len(marblesArray) == 3 and (lastMarble[0] == 0 or lastMarble[1] == 0 or lastMarble[0] == 8 or lastMarble[1] == 8):
                return False, "outOfLimitError", marblesArray, moveName

            marblesArray.sort()
            if len(marblesArray) == 2:
                if (marblesArray[0][0] == 0 or marblesArray[0][1] == 0) and (moveName == "NE" or moveName == "NW"):
                    return False, "outOfLimitError"
                elif (marblesArray[-1][0] == 8 or marblesArray[-1][1] == 8) and (moveName == "SE" or moveName == "SW"):
                    return False, "outOfLimitError"


            currentValue = self.board[lastMarble[0]][lastMarble[1]]
            try:
                nextValue = self.board[lastMarble[0] + vectorMove[0]][lastMarble[1] + vectorMove[1]] 
            except:
                return False, "allyOutOfBoardError", marblesArray, moveName

            if nextValue == 'X':
                return False, "outLimitError", marblesArray, moveName
            elif nextValue == currentValue:
                return False, "sameValueError", marblesArray, moveName
            elif nextValue == 'E':
                marblesMoved = []
                for marble in marblesArray:
                    marblesMoved.append([marble[0] + vectorMove[0], marble[1] + vectorMove[1]])
                return True, marblesArray, marblesMoved
            else:
                try: # ! test [CHECKED]
                    lastOpponentMarbleValue = self.board[lastMarble[0] + len(marblesArray) * vectorMove[0]][lastMarble[1] + len(marblesArray) * vectorMove[1]]
                except:
                    try:
                        lastOpponentMarbleValue = self.board[lastMarble[0] + (len(marblesArray) - 1) * vectorMove[0]][lastMarble[1] + (len(marblesArray) - 1) * vectorMove[1]]
                    except:
                        return False, "outOfRange"
                    
                if lastOpponentMarbleValue != 'E' and lastOpponentMarbleValue == 'X':
                    return False, "NonEmptyError", marblesArray, moveName
                else:
                    marblesMoved = []
                    opponentMarbles = []
                    opponentMarblesMoved = []
                
                    for marble in marblesArray:
                        marblesMoved.append([marble[0] + vectorMove[0], marble[1] + vectorMove[1]])

                    for i in range(1, len(marblesArray)):
                        opponentValue = self.board[lastMarble[0] + i * vectorMove[0]][lastMarble[1] + i * vectorMove[1]]
                        if(opponentValue == 'E'):
                            break
                        opponentMarbles.append([lastMarble[0] + i * vectorMove[0], lastMarble[1] + i * vectorMove[1]])

                    if len(opponentMarbles) == 1:
                        self.soloMove(opponentMarbles, moveName, opponent=True)
                    else:
                        self.lineMove(opponentMarbles, moveName, opponent=True)

                    return True, marblesArray, marblesMoved, opponentMarbles, opponentMarblesMoved
                
        return False, "nonAlignedError", marblesArray, moveName

    def arrowMove(self, marblesArray, moveName, opponent=False):
        """
            - Checks the list only one marble ?)\n
            - Iterates the list\n
                - Next box == actual color ('B' == 'B'), returns error\n
                - Next box  == 'X' (out of limit), returns error\n
                - Next box == 'E' (empty), you can move your marble there\n
                - Next box == opposing color, checks if there is an empty box behind its position\n
            \n
            For each marbles, if the next box is 'E' or the opposing color (with an empty box behind), you can move your chain !
        """
        updatedMarbles = []
        if len(marblesArray) == 1:
            return "singleMarbleInfo", marblesArray, moveName

        for marble in marblesArray:
            if ((moveName.__contains__('S') and marble[0] != 8) or (moveName.__contains__('N') and marble[0] != 0)) and ((moveName.__contains__('W') and marble[1] != 0) or (moveName.__contains__('E') and marble[1] != 8)): 
                nextMarbleValue = self.board[marble[0] + moves[moveName][0]][marble[1] + moves[moveName][1]]
                currentMarbleValue = self.board[marble[0]][marble[1]]
                if nextMarbleValue == currentMarbleValue:
                    return False, "allyPchainsenceError", marblesArray, moveName
                elif nextMarbleValue == 'X':
                    return False, "outLimitError", marblesArray, moveName
                elif nextMarbleValue == 'E':
                    pass
                else:
                    try:
                        if self.board[marble[0] + 2 * moves[moveName][0]][marble[1] + 2 * moves[moveName][1]] == nextMarbleValue:
                            return False, "opponentMoveError", marblesArray, moveName
                    except:
                        return False, "outOfRange"

                updatedMarbles.append([marble[0] + moves[moveName][0], marble[1] + moves[moveName][1]])
    
        if len(updatedMarbles) != 0:
            return True, marblesArray, updatedMarbles
    
        return False, "notAnArrowMoveError"

    def soloMove(self, marblesArray, moveName, opponent=False):
        """
            - Checks the # of marbles in list\n
            - Checks the next box\n
                - Next box == 'X' (out of limit), returns an error\n
                - Next box == actual color ('W' == 'W'), returns an error\n
                - Next box == 'E' (empty), you can move your marble there\n
                - Next box == opposing color, returns an error (you have to move at least 2 allies to push your opponent)\n
            \n
            So if the next box is 'E', you can move your marble and update your board !
        """
        if len(marblesArray) == 1:
            currentValue = self.board[marblesArray[0][0]][marblesArray[0][1]]
            try:
                nextValue = self.board[marblesArray[0][0] + moves[moveName][0]][marblesArray[0][1] + moves[moveName][1]]
            except:
                nextValue = self.board[marblesArray[0][0]][marblesArray[0][1]]

            if nextValue == 'X':
                return False, "outLimitError"
            elif nextValue == currentValue:
                return False, "allyPchainsenceError"
            elif nextValue == 'E':
                pass
            else:
                return False, "opponentMoveError"

            marbleMoved = [[marblesArray[0][0] + moves[moveName][0], marblesArray[0][1] + moves[moveName][1]]]
            return True, marblesArray, marbleMoved
    
        return False, "notAsingleMarbleError"

    def updateBoard(self, oldPositions, newPositions):
        """
            Adds changes into the last board.
        """
        color = self.board[oldPositions[0][0]][oldPositions[0][1]]

        for marble in oldPositions:
            self.board[marble[0]][marble[1]] = 'E'
    
        for marble in newPositions:
            self.board[marble[0]][marble[1]] = f"{color}"

    def action(self, marblesArray, moveName, maximizer, update=False):
        """
            - Checks the marble's color\n
            - Checks the direction existence\n
            - Checks the marbles alignment\n
            \t- Tries making a lineMove\n
            \t- If lineMove returns an error, tries making an arrowMove\n
            \t- If arrowMove returns an error, tries making a soloMove\n
            - If lineMove, arrowMove and soloMove return errors, the program returns False
        """
        color = self.myColor(maximizer)

        if self.colored(marblesArray, color) is not True:
            # print(f"color error : '{color}'")
            return False

        if self.existingDirection(moveName) is False:
            # print(f"direction error : '{moveName}'")
            return False

        if self.chain(marblesArray) != "lengthChainError" and self.chain(marblesArray) != "marblesChainError":
        
            lm = self.lineMove(marblesArray, moveName)
            am = self.arrowMove(marblesArray, moveName)
            sm = self.soloMove(marblesArray, moveName)
            if lm[0] is not True:
                if am[0] is not True:
                    if sm[0] is not True:
                        # print(f"lineMove  : {lm}")
                        # print(f"arrowMove : {am}")
                        # print(f"soloMove  : {sm}")
                        return False
                    else:
                        # print("solo move")
                        self.updateBoard(sm[1], sm[2]) if update == True else None
                else:
                    # print("arrow move")
                    self.updateBoard(am[1], am[2]) if update == True else None
            else:
                # print("line move")
                self.updateBoard(lm[3], lm[4]) if (len(lm) == 4) and update == True else None
                self.updateBoard(lm[1], lm[2]) if update == True else None
    
            return moveName
    
        return False

    def possibleChainsFromPoint(self, lengthChain, referenceMarble, currentMarble=None, move=None, chain=[], chainsList=[], possibleDirections=list(moves.values())):    
        if currentMarble is None:
            currentMarble = referenceMarble
    
        if len(chain) == 0:
            chain.append(currentMarble)
    
        chain.sort()

        if lengthChain == 1:
            chainsList.append(chain)
            return chainsList
        elif lengthChain == len(chain):
            chainsList.append(chain)
            possibleDirections.remove(move)
            return self.possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections)

        color = self.board[referenceMarble[0]][referenceMarble[1]]

        if move is None:
            for myMove in possibleDirections:
                nextMarble = [currentMarble[0] + myMove[0], currentMarble[1] + myMove[1]]
                previousMarble = [currentMarble[0] - myMove[0], currentMarble[1] - myMove[1]]
            
                if ((previousMarble[0] != -1 and previousMarble[0] != 9) and (previousMarble[1] != -1 and previousMarble[1] != 9)) and ((nextMarble[0] != -1 and nextMarble[0] != 9) and (nextMarble[1] != -1 and nextMarble[1] != 9)):
                    nextMarbleColor = self.board[nextMarble[0]][nextMarble[1]]
                    previousMarbleColor = self.board[previousMarble[0]][previousMarble[1]]
                    if previousMarbleColor == color and nextMarbleColor == color:
                        doubleNeighbourChain = [previousMarble, currentMarble, nextMarble]
                        doubleNeighbourChain.sort()
                        if chainsList.__contains__(doubleNeighbourChain) is not True and lengthChain == 3:
                            chainsList.append(doubleNeighbourChain)
                            return self.possibleChainsFromPoint(lengthChain, referenceMarble, None, myMove, [], chainsList, possibleDirections)
                        return self.possibleChainsFromPoint(lengthChain, referenceMarble, None, myMove, chain, chainsList, possibleDirections)

                if nextMarble[0] != -1 and nextMarble[0] != 9 and nextMarble[1] != -1 and nextMarble[1] != 9:
                    nextMarbleColor = self.board[nextMarble[0]][nextMarble[1]]  
                    if nextMarbleColor == color:
                        return self.possibleChainsFromPoint(lengthChain, referenceMarble, currentMarble, myMove, chain, chainsList, possibleDirections)
                else:
                    possibleDirections.remove(myMove)
                    return self.possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections)
            if len(chainsList) > 0:
                chainsList.sort()
                return chainsList

            return "notMoveFoundError"
        else:
            nextMarble = [currentMarble[0] + move[0], currentMarble[1] + move[1]]
            if (nextMarble[0] != -1 and nextMarble[0] != 9) and (nextMarble[1] != -1 and nextMarble[1] != 9):
                nextMarbleColor = self.board[nextMarble[0]][nextMarble[1]]

                if nextMarbleColor == color:
                    chain.append(nextMarble)
                    return self.possibleChainsFromPoint(lengthChain, referenceMarble, nextMarble, move, chain, chainsList, possibleDirections)
            
            previousMarble = [referenceMarble[0] - move[0], referenceMarble[1] - move[1]]
            if (previousMarble[0] != -1 and previousMarble[0] != 9) and (previousMarble[1] != -1 and previousMarble[1] != 9):
                previousMarbleColor = self.board[previousMarble[0]][previousMarble[1]]

                if previousMarbleColor == color:
                    chain.append(previousMarble)
                    chain.sort()
                    if chainsList.__contains__(chain) is not True and len(chain) == lengthChain:
                        chainsList.append(chain)
                        return self.possibleChainsFromPoint(lengthChain, referenceMarble, previousMarble, move, [], chainsList, possibleDirections)

            possibleDirections.remove(move)
            return self.possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections)

    def randomPlay(self, color):
        """
            Choose one random chain with one random move in the board.\n
            The method returns :
                - the color
                - the length of the chain
                - the marble
                - the chain built from this marble
                - the move
        """
        randomLength = random.choice((1,2,3))
        chosenBoxes = []
        myMoves = list(moves.keys())

        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if value == color:
                    chosenBoxes.append([i,j])
    
        randomMarble = random.choice(chosenBoxes)
        chains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
        randomMove = random.choice(myMoves)
    
        possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    
        while possibleChains == "notMoveFoundError":
            if len(chosenBoxes) > 1:
                chosenBoxes.remove(randomMarble)
                randomMarble = random.choice(chosenBoxes)
                possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
            else:
                # print("no marbles")
                return False
    
        randomChain = random.choice(possibleChains)
        a = self.action(randomChain, randomMove, color, False)

        while a is False:
            if myMoves != []:
                randomMove = random.choice(myMoves)
                myMoves.remove(randomMove)
            else:
                if len(chosenBoxes) > 1:
                    chosenBoxes.remove(randomMarble)
                    randomMarble = random.choice(chosenBoxes)
                    possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
                    while possibleChains == "notMoveFoundError":
                        if len(chosenBoxes) > 1:
                            chosenBoxes.remove(randomMarble)
                            randomMarble = random.choice(chosenBoxes)
                            possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
                        else:
                            return False
                    randomChain = random.choice(possibleChains)
                elif len(chosenBoxes) == 1:
                    possibleChain =  self.possibleChainsFromPoint(randomLength, chosenBoxes[0], None, None, [], [], list(moves.values()))
                    chosenBoxes.remove(randomMarble)
                else:
                    return False
            a = self.action(randomChain, randomMove, color, True)
    
        return color, randomChain, a
        

if __name__ == '__main__':
    # state = Board([
    # ["W", "W", "W", "W", "W", "X", "X", "X", "X"],
    # ["W", "W", "W", "W", "W", "W", "X", "X", "X"],
    # ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
    # ["E", "E", "E", "E", "E", "E", "E", "E", "X"],
    # ["E", "E", "E", "E", "E", "E", "E", "E", "E"],
    # ["X", "E", "E", "E", "E", "E", "E", "E", "E"],
    # ["X", "X", "E", "E", "B", "B", "B", "E", "E"],
    # ["X", "X", "X", "B", "B", "B", "B", "B", "B"],
    # ["X", "X", "X", "X", "B", "B", "B", "B", "B"]])
    
    # state.displayBoard()
    # a,b= (minimax(state,3,True))   
    # print(a,b)

    b = Board([
    ["W", "W", "W", "W", "W", "X", "X", "X", "X"],
    ["W", "W", "W", "W", "W", "W", "X", "X", "X"],
    ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
    ["E", "E", "E", "E", "E", "E", "E", "E", "X"],
    ["E", "E", "E", "E", "E", "E", "E", "E", "E"],
    ["X", "E", "E", "E", "E", "E", "E", "E", "E"],
    ["X", "X", "E", "E", "B", "B", "B", "E", "E"],
    ["X", "X", "X", "B", "B", "B", "B", "B", "B"],
    ["X", "X", "X", "X", "B", "B", "B", "B", "B"]])

    # b = Board([
    # ["W", "W", "E", "E", "W", "X", "X", "X", "X"],
    # ["W", "W", "W", "E", "E", "E", "X", "X", "X"],
    # ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
    # ["E", "E", "E", "E", "W", "E", "E", "E", "X"],
    # ["E", "B", "W", "E", "E", "W", "E", "E", "E"],
    # ["X", "E", "B", "W", "B", "E", "E", "E", "E"],
    # ["X", "X", "E", "W", "E", "B", "B", "E", "E"],
    # ["X", "X", "X", "B", "E", "B", "B", "B", "B"],
    # ["X", "X", "X", "X", "E", "B", "B", "B", "B"]])

    # print(b.population(False))

    result = minimax(b, 3, True, -math.inf, math.inf)
    print(result)
    b.displayBoard()

    # a = [1, 2]
    # b = copy.copy(a)
    # c = copy.deepcopy(a)
    

    # print(id(a), id(b), id(c))