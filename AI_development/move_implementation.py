import random
import time
from typing import Counter

board = [
    ["W", "W", "W", "W", "W", "X", "X", "X", "X"],
    ["W", "W", "W", "W", "W", "W", "X", "X", "X"],
    ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
    ["E", "E", "E", "E", "E", "E", "E", "E", "X"],
    ["E", "E", "E", "E", "E", "E", "E", "E", "E"],
    ["X", "E", "E", "E", "E", "E", "E", "E", "E"],
    ["X", "X", "E", "E", "B", "B", "B", "E", "E"],
    ["X", "X", "X", "B", "B", "B", "B", "B", "B"],
    ["X", "X", "X", "X", "B", "B", "B", "B", "B"]
]

moves = {
    "NW":[-1, -1],
    "NE":[-1,  0],
    "E" :[ 0,  1],
    "SW":[ 1,  0],
    "SE":[ 1,  1],
    "W" :[ 0, -1]
}

def displayBoard(board):
    """
        Shows the Abalone board.
    """
    result = "\n\t [ CURRENT BOARD ]\n\n"
    for index,row in enumerate(board):
        if index == 0 or index == 8:
            result += "        "
        elif index == 1 or index == 7:
            result += "      "
        elif index == 2 or index == 6:
            result += "    "
        elif index == 3 or index == 5:
            result += "  "
        elif index == 5:
            result += ""
        for case in row:
            if case == "X":
                pass
            elif case == "E":
                result += " .  "
            else:
                result += f" {case}  "
        result += "\n"
    
    print(result)

def existingDirection(moveName):
    """
        Checks if the direction exists.
    """
    if moves.get(moveName) is None:
        return False
    return True

def aligned(vector01, vector02):
    """
        Check if 2 vectors are aligned or not.
    """
    sum = [vector01[0] + vector02[0], vector01[1] + vector02[1]]
    product = [2*i for i in vector01]
    if product == sum or sum == [0, 0]:
        return True
    
    return False

def colored(marblesArray, color):
    """
    ! FIX BUGS WITH COLOR    
        Checks if all marbles have the right color.
    """
    for marble in marblesArray:
        if board[marble[0]][marble[1]] != 'W' and board[marble[0]][marble[1]] != 'B':
            print("no marble here", marblesArray, marble, board[marble[0]][marble[1]])
            return "caseWithoutMarbleError"
        else:
            if board[marble[0]][marble[1]] != color:
                print("wrong color marble")
                return "wrongColorError"

    return True

def chain(marblesArray, move=None):
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
            return chain(marblesArray[1:], move=move)

    for currentMove in moves.values():
        if marblesArray[0] == [marblesArray[1][0] + currentMove[0], marblesArray[1][1] + currentMove[1]]:
            return chain(marblesArray[1:], move=currentMove)
    
    return "marblesChainError"

def lineMove(marblesArray, moveName, opponent=False):
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
    vectorChain = chain(marblesArray)
    lastMarble = marblesArray[0]

    if vectorChain == "lengthChainError" or vectorChain == "marblesChainError":
        return False, "chainError", marblesArray, moveName
    
    if vectorChain == None and opponent is False:
        return "soloMarbleInfo", marblesArray, moveName

    if (aligned(vectorMove, vectorChain)):
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


        currentValue = board[lastMarble[0]][lastMarble[1]]
        try:
            nextValue = board[lastMarble[0] + vectorMove[0]][lastMarble[1] + vectorMove[1]] 
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
                lastOpponentMarbleValue = board[lastMarble[0] + len(marblesArray) * vectorMove[0]][lastMarble[1] + len(marblesArray) * vectorMove[1]]
            except:
                try:
                    lastOpponentMarbleValue = board[lastMarble[0] + (len(marblesArray) - 1) * vectorMove[0]][lastMarble[1] + (len(marblesArray) - 1) * vectorMove[1]]
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
                    opponentValue = board[lastMarble[0] + i * vectorMove[0]][lastMarble[1] + i * vectorMove[1]]
                    if(opponentValue == 'E'):
                        break
                    opponentMarbles.append([lastMarble[0] + i * vectorMove[0], lastMarble[1] + i * vectorMove[1]])

                if len(opponentMarbles) == 1:
                    soloMove(opponentMarbles, moveName, opponent=True)
                else:
                    lineMove(opponentMarbles, moveName, opponent=True)

                return True, marblesArray, marblesMoved, opponentMarbles, opponentMarblesMoved
                
    return False, "nonAlignedError", marblesArray, moveName

def arrowMove(marblesArray, moveName, opponent=False):
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
            nextMarbleValue = board[marble[0] + moves[moveName][0]][marble[1] + moves[moveName][1]]
            currentMarbleValue = board[marble[0]][marble[1]]
            if nextMarbleValue == currentMarbleValue:
                return False, "allyPresenceError", marblesArray, moveName
            elif nextMarbleValue == 'X':
                return False, "outLimitError", marblesArray, moveName
            elif nextMarbleValue == 'E':
                pass
            else:
                try:
                    if board[marble[0] + 2 * moves[moveName][0]][marble[1] + 2 * moves[moveName][1]] == nextMarbleValue:
                        return False, "opponentMoveError", marblesArray, moveName
                except:
                    return False, "outOfRange"

            updatedMarbles.append([marble[0] + moves[moveName][0], marble[1] + moves[moveName][1]])
    
    if len(updatedMarbles) != 0:
        return True, marblesArray, updatedMarbles
    
    return False, "notAnArrowMoveError"

def soloMove(marblesArray, moveName, opponent=False):
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
        currentValue = board[marblesArray[0][0]][marblesArray[0][1]]
        try:
            nextValue = board[marblesArray[0][0] + moves[moveName][0]][marblesArray[0][1] + moves[moveName][1]]
        except:
            nextValue = board[marblesArray[0][0]][marblesArray[0][1]]

        if nextValue == 'X':
            return False, "outLimitError"
        elif nextValue == currentValue:
            return False, "allyPresenceError"
        elif nextValue == 'E':
            pass
        else:
            return False, "opponentMoveError"

        marbleMoved = [[marblesArray[0][0] + moves[moveName][0], marblesArray[0][1] + moves[moveName][1]]]
        return True, marblesArray, marbleMoved
    
    return False, "notAsingleMarbleError"

def updateBoard(oldPositions, newPositions):
    """
        Adds changes into the last board.
    """
    color = board[oldPositions[0][0]][oldPositions[0][1]]

    for marble in oldPositions:
        board[marble[0]][marble[1]] = 'E'
    
    for marble in newPositions:
        board[marble[0]][marble[1]] = f"{color}"

def action(marblesArray, moveName, color, update=False):
    """
        - Checks the marble's color\n
        - Checks the direction existence\n
        - Checks the marbles alignment\n
        \t- Tries making a lineMove\n
        \t- If lineMove returns an error, tries making an arrowMove\n
        \t- If arrowMove returns an error, tries making a soloMove\n
        - If lineMove, arrowMove and soloMove return errors, the program returns False
    """
    if colored(marblesArray, color) is not True:
        print(f"color error : '{color}'")
        return False

    if existingDirection(moveName) is False:
        print(f"direction error : '{moveName}'")
        return False

    if chain(marblesArray) != "lengthChainError" and chain(marblesArray) != "marblesChainError":
        
        lm = lineMove(marblesArray, moveName)
        am = arrowMove(marblesArray, moveName)
        sm = soloMove(marblesArray, moveName)
        if lm[0] is not True:
            if am[0] is not True:
                if sm[0] is not True:
                    print(f"lineMove  : {lm}")
                    print(f"arrowMove : {am}")
                    print(f"soloMove  : {sm}")
                    return False
                else:
                    # print("solo move")
                    updateBoard(sm[1], sm[2]) if update == True else None
            else:
                # print("arrow move")
                updateBoard(am[1], am[2]) if update == True else None
        else:
            # print("line move")
            updateBoard(lm[3], lm[4]) if (len(lm) == 4) and update == True else None
            updateBoard(lm[1], lm[2]) if update == True else None
    
        return moveName
    
    return False

def possibleChainsFromPoint(lengthChain, referenceMarble, currentMarble=None, move=None, chain=[], chainsList=[], possibleDirections=list(moves.values())):    
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
        return possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections)

    color = board[referenceMarble[0]][referenceMarble[1]]

    if move is None:
        for myMove in possibleDirections:
            nextMarble = [currentMarble[0] + myMove[0], currentMarble[1] + myMove[1]]
            previousMarble = [currentMarble[0] - myMove[0], currentMarble[1] - myMove[1]]
            
            if ((previousMarble[0] != -1 and previousMarble[0] != 9) and (previousMarble[1] != -1 and previousMarble[1] != 9)) and ((nextMarble[0] != -1 and nextMarble[0] != 9) and (nextMarble[1] != -1 and nextMarble[1] != 9)):
                nextMarbleColor = board[nextMarble[0]][nextMarble[1]]
                previousMarbleColor = board[previousMarble[0]][previousMarble[1]]
                if previousMarbleColor == color and nextMarbleColor == color:
                    doubleNeighbourChain = [previousMarble, currentMarble, nextMarble]
                    doubleNeighbourChain.sort()
                    if chainsList.__contains__(doubleNeighbourChain) is not True and lengthChain == 3:
                        chainsList.append(doubleNeighbourChain)
                        return possibleChainsFromPoint(lengthChain, referenceMarble, None, myMove, [], chainsList, possibleDirections)
                    return possibleChainsFromPoint(lengthChain, referenceMarble, None, myMove, chain, chainsList, possibleDirections)

            if nextMarble[0] != -1 and nextMarble[0] != 9 and nextMarble[1] != -1 and nextMarble[1] != 9:
                nextMarbleColor = board[nextMarble[0]][nextMarble[1]]  
                if nextMarbleColor == color:
                    return possibleChainsFromPoint(lengthChain, referenceMarble, currentMarble, myMove, chain, chainsList, possibleDirections)
            else:
                possibleDirections.remove(myMove)
                return possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections)
        if len(chainsList) > 0:
            chainsList.sort()
            return chainsList

        return "notMoveFoundError"
    else:
        nextMarble = [currentMarble[0] + move[0], currentMarble[1] + move[1]]
        if (nextMarble[0] != -1 and nextMarble[0] != 9) and (nextMarble[1] != -1 and nextMarble[1] != 9):
            nextMarbleColor = board[nextMarble[0]][nextMarble[1]]

            if nextMarbleColor == color:
                chain.append(nextMarble)
                return possibleChainsFromPoint(lengthChain, referenceMarble, nextMarble, move, chain, chainsList, possibleDirections)
            
        previousMarble = [referenceMarble[0] - move[0], referenceMarble[1] - move[1]]
        if (previousMarble[0] != -1 and previousMarble[0] != 9) and (previousMarble[1] != -1 and previousMarble[1] != 9):
            previousMarbleColor = board[previousMarble[0]][previousMarble[1]]

            if previousMarbleColor == color:
                chain.append(previousMarble)
                chain.sort()
                if chainsList.__contains__(chain) is not True and len(chain) == lengthChain:
                    chainsList.append(chain)
                    return possibleChainsFromPoint(lengthChain, referenceMarble, previousMarble, move, [], chainsList, possibleDirections)

        possibleDirections.remove(move)
        return possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections)

def randomPlay(color):
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

    for i,row in enumerate(board):
        for j,value in enumerate(row):
            if value == color:
                chosenBoxes.append([i,j])
    
    randomMarble = random.choice(chosenBoxes)
    chains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    randomMove = random.choice(myMoves)
    
    possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    
    while possibleChains == "notMoveFoundError":
        if len(chosenBoxes) > 1:
            chosenBoxes.remove(randomMarble)
            randomMarble = random.choice(chosenBoxes)
            possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
        else:
            print("no marbles")
            return False
    
    randomChain = random.choice(possibleChains)
    a = action(randomChain, randomMove, color, False)

    while a is False:
        if myMoves != []:
            randomMove = random.choice(myMoves)
            myMoves.remove(randomMove)
        else:
            if len(chosenBoxes) > 1:
                chosenBoxes.remove(randomMarble)
                randomMarble = random.choice(chosenBoxes)
                possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
                while possibleChains == "notMoveFoundError":
                    if len(chosenBoxes) > 1:
                        chosenBoxes.remove(randomMarble)
                        randomMarble = random.choice(chosenBoxes)
                        possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
                    else:
                        return False
                randomChain = random.choice(possibleChains)
            else:
                return possibleChainsFromPoint(randomLength, chosenBoxes[0], None, None, [], [], list(moves.values()))

        a = action(randomChain, randomMove, color, True)
        


def opposingMarblesOut(yourColor):
    counter = 0
    opposingColor = ''

    # ! COMMENT FAIRE CETTE CONDITION TERNAIRE ?
    # opposingColor = 'W' if(yourColor == 'B') else opposingColor = 'B'

    if yourColor == 'B':
        opposingColor = 'W'
    else:
        opposingColor = 'B'

    for row in board:
        for box in row:
            if box == opposingColor:
                counter += 1
    
    return 14 - counter

if __name__ == '__main__':
    displayBoard(board)
    scoreWhite = opposingMarblesOut('B')
    scoreBlack = opposingMarblesOut('W')
    
    i = 0
    while scoreBlack < 6 and scoreWhite < 6:
        scoreWhite = opposingMarblesOut('B')
        scoreBlack = opposingMarblesOut('W')

        color = random.choice(('W', 'B'))
        print(randomPlay(color))
        i += 1

    displayBoard(board)
    if scoreBlack == 6:
        winner = "Black"
    else:
        winner = "White"

    print(f"the winner is : {winner}")