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
    if color != 'W' and color != 'B':
        return False

    for marble in marblesArray:
        if board[marble[0]][marble[1]] != 'W' and board[marble[0]][marble[1]] != 'B':
            return False
        else:
            if board[marble[0]][marble[1]] != color:
                return False

    return True

def chain(marblesArray, move=None):
    """
        Checks if all marbles are aligned.
    """

    if len(marblesArray) == 1:
        return move
        
    marblesArray.sort()
    color = board[marblesArray[0][0]][marblesArray[0][1]]
    
    if len(marblesArray) > 3:
        return False
    elif not colored(marblesArray, color):
        return False

    if move is not None:
        if marblesArray[0] == [marblesArray[1][0] + move[0], marblesArray[1][1] + move[1]]:
            return chain(marblesArray[1:], move=move)

    for currentMove in moves.values():
        if [marblesArray[0][0] + currentMove[0], marblesArray[0][1] + currentMove[1]] == marblesArray[1]:
            return chain(marblesArray[1:], move=currentMove)
    
    return False

def lineMove(marblesArray, moveName):
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

    # if vectorChain:
    #     return False, "chainError", marblesArray, moveName

    if vectorChain is False:
        return False
    elif len(marblesArray) == 1:
        return False
    
    # if vectorChain == None and opponent is False:
    #     return "soloMarbleInfo", marblesArray, moveName

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
            # return False, "outOfLimitError", marblesArray, moveName
            return False

        marblesArray.sort()
        if len(marblesArray) == 2:
            if (marblesArray[0][0] == 0 or marblesArray[0][1] == 0) and (moveName == "NE" or moveName == "NW"):
                # return False, "outOfLimitError"
                return False
            elif (marblesArray[-1][0] == 8 or marblesArray[-1][1] == 8) and (moveName == "SE" or moveName == "SW"):
                # return False, "outOfLimitError"
                return False


        currentValue = board[lastMarble[0]][lastMarble[1]]
        try:
            nextValue = board[lastMarble[0] + vectorMove[0]][lastMarble[1] + vectorMove[1]] 
        except:
            # return False, "allyOutOfBoardError", marblesArray, moveName
            return False

        if nextValue == 'X':
            # return False, "outLimitError", marblesArray, moveName
            return False
        elif nextValue == currentValue:
            # return False, "sameValueError", marblesArray, moveName
            return False
        elif nextValue == 'E':
            marblesMoved = []
            for marble in marblesArray:
                marblesMoved.append([marble[0] + vectorMove[0], marble[1] + vectorMove[1]])
            return True, marblesArray, marblesMoved
            # return True
        else:
            try: # ! test [CHECKED]
                lastOpponentMarbleValue = board[lastMarble[0] + len(marblesArray) * vectorMove[0]][lastMarble[1] + len(marblesArray) * vectorMove[1]]
            except:
                try:
                    lastOpponentMarbleValue = board[lastMarble[0] + (len(marblesArray) - 1) * vectorMove[0]][lastMarble[1] + (len(marblesArray) - 1) * vectorMove[1]]
                except:
                    # return False, "outOfRange"
                    return False
                    
            if lastOpponentMarbleValue != 'E' and lastOpponentMarbleValue == 'X':
                # return False, "NonEmptyError", marblesArray, moveName
                return False
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
                    soloMove(opponentMarbles, moveName)
                else:
                    lineMove(opponentMarbles, moveName)

                return True, marblesArray, marblesMoved, opponentMarbles, opponentMarblesMoved
                # return True
                
    # return False, "nonAlignedError", marblesArray, moveName
    return False

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
        False

    for marble in marblesArray:
        if ((moveName.__contains__('S') and marble[0] != 8) or (moveName.__contains__('N') and marble[0] != 0)) and ((moveName.__contains__('W') and marble[1] != 0) or (moveName.__contains__('E') and marble[1] != 8)): 
            nextMarbleValue = board[marble[0] + moves[moveName][0]][marble[1] + moves[moveName][1]]
            currentMarbleValue = board[marble[0]][marble[1]]
            if nextMarbleValue == currentMarbleValue:
                # return False, "allyPresenceError", marblesArray, moveName
                return False
            elif nextMarbleValue == 'X':
                # return False, "outLimitError", marblesArray, moveName
                return False
            elif nextMarbleValue == 'E':
                pass
            else:
                try:
                    if board[marble[0] + 2 * moves[moveName][0]][marble[1] + 2 * moves[moveName][1]] == nextMarbleValue:
                        # return False, "opponentMoveError", marblesArray, moveName
                        return False
                except:
                    # return False, "outOfRange"
                    return False

            updatedMarbles.append([marble[0] + moves[moveName][0], marble[1] + moves[moveName][1]])
    
    if len(updatedMarbles) != 0:
        return True, marblesArray, updatedMarbles
        # return True
    
    # return False, "notAnArrowMoveError"
    return False

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
            # return False, "outLimitError"
            return False
        elif nextValue == currentValue:
            # return False, "allyPresenceError"
            return False
        elif nextValue == 'E':
            pass
        else:
            # return False, "opponentMoveError"
            return False

        marbleMoved = [[marblesArray[0][0] + moves[moveName][0], marblesArray[0][1] + moves[moveName][1]]]
        return True, marblesArray, marbleMoved
        # return True
    
    # return False, "notAsingleMarbleError"
    return False

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
        # print(f"color error : '{color}'")
        return False, None

    if existingDirection(moveName) is False:
        # print(f"direction error : '{moveName}'")
        return False, None

    if chain(marblesArray) != "lengthChainError" and chain(marblesArray) != "marblesChainError":
        
        lm = lineMove(marblesArray, moveName)
        am = arrowMove(marblesArray, moveName)
        sm = soloMove(marblesArray, moveName)
        if lm is False:
            if am is False:
                if sm is False:
                    # print(f"lineMove  : {lm}")
                    # print(f"arrowMove : {am}")
                    # print(f"soloMove  : {sm}")
                    return False, None
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
    
        return True, moveName
        # return True
    
    return False, None

def possibleChainsFromPoint(lengthChain, referenceMarble, currentMarble=None, move=None, chain=[], chainsList=[], possibleDirections=list(moves.values())):    
    if currentMarble is None: # Vérifie si c'est la première boucle de la récursivité
        currentMarble = referenceMarble
    
    if len(chain) == 0: # Vérifie si c'est la première boucle de la récursivité
        chain.append(currentMarble)
    
    chain.sort()

    if lengthChain == 1: # Si la chaîne ne doit posséder qu'un seul élément
        chainsList.append(chain)
        return True, chainsList
    elif lengthChain == len(chain): # Si la chaîne a atteint la longueur désirée
        chainsList.append(chain) # Ajouter à la liste de chaînes possibles
        possibleDirections.remove(move) # Enlever le move utilisé
        return possibleChainsFromPoint(lengthChain, referenceMarble, None, None, [], chainsList, possibleDirections) # Refaire l'opération mais avec un move en moins

    color = board[referenceMarble[0]][referenceMarble[1]]

    if move is None: # S'il n'y a pas encore de move choisi
        for myMove in possibleDirections:
            nextMarble = [currentMarble[0] + myMove[0], currentMarble[1] + myMove[1]] # Regarder le pion suivant avec le move actuel
            previousMarble = [currentMarble[0] - myMove[0], currentMarble[1] - myMove[1]] # Regarder le pion précédent avec le move actuel
            
            # Vérifie si les pions limitrophes ne dépassent pas les limites du plateau de jeu
            if ((previousMarble[0] != -1 and previousMarble[0] != 9) and (previousMarble[1] != -1 and previousMarble[1] != 9)) and ((nextMarble[0] != -1 and nextMarble[0] != 9) and (nextMarble[1] != -1 and nextMarble[1] != 9)):
                nextMarbleColor = board[nextMarble[0]][nextMarble[1]] # Enregistrer la couleur du pion précédent
                previousMarbleColor = board[previousMarble[0]][previousMarble[1]] # Enregistrer la couleur du pion suivant
                
                if previousMarbleColor == color and nextMarbleColor == color: # Si les deux pions limitrophes possèdent la même couleur que celle du pion de référence
                    doubleNeighbourChain = [previousMarble, currentMarble, nextMarble]
                    doubleNeighbourChain.sort()
                    if chainsList.__contains__(doubleNeighbourChain) is not True and lengthChain == 3: # Vérifie si la liste de chaînes ne possède pas déjà cette dernière et si la longueur souhaitée est 3
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
            return True, chainsList

        return False
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
    possibleLengths = [1, 2, 3]
    randomLength = random.choice(possibleLengths)
    chosenBoxes = []
    myMoves = list(moves.keys())

    for i,row in enumerate(board): # Ajoute à une liste tous les éléments qui correspondent à la couleur choisie
        for j,value in enumerate(row):
            if value == color:
                chosenBoxes.append([i,j])
    
    print(chosenBoxes)
    randomMarble = random.choice(chosenBoxes) # Sélectionne un pion aléatoire parmi la liste créée
    randomMove = random.choice(myMoves) # Choisi un mouvement aléatoire    
    possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))[1] # Retourne l'ensemble des chaînes possible à partir d'une coordonnée et d'une longueur
    randomChain = random.choice(possibleChains)
    
    act = action(randomChain, randomMove, color, True)
    while act[0] is False:
        if len(myMoves) > 1:
            myMoves.remove(randomMove)
            print("MOVE DISPO : ")
            randomMove = random.choice(myMoves)
        elif len(myMoves) == 1:
            if len(possibleChains) > 1:
                possibleChains.remove(randomChain)
                print("CHAINES DISPO : ", possibleChains)
                randomChain = random.choice(possibleChains)
            elif len(possibleChains) == 1:
                if len(chosenBoxes) > 1:
                    chosenBoxes.remove(randomMarble)
                    print("PIONS DISPO : ", chosenBoxes)
                    randomMarble = random.choice(chosenBoxes)
                elif len(chosenBoxes) == 1:
                    print(chosenBoxes)
                    return "SUMITO"
        
        act = action(randomChain, randomMove, color, True)

    """
        Si avec la longueur indiquée il n'y a pas de mouvement possible pour le pion, prendre une autre longueur
        Après avoir pris toutes les longueurs, s'il n'y a toujours pas de mouvement disponibles, changer de pion
        Après avoir regardés tous les pions, s'il n'y a plus de mouvements possible sur le plateau SUMITO
    """

    # if possibleChains is False:
    #     print("FPINEROGNEROBUE___________________ETGBOTBGIOJJ ")
    #     # raise Exception()
    #     if len(possibleLengths) > 0:
    #         possibleLengths.remove(randomLength)
    #         randomLength = random.choice(possibleLengths)
    #         possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    #     elif len(possibleLengths) == 0:
    #         if len(chosenBoxes) > 0:
    #             possibleLengths = [1, 2, 3]
    #             randomLength = random.choice(possibleLengths)
    #             chosenBoxes.remove(randomMarble)
    #             randomMarble = random.choice(chosenBoxes)
    #             possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    #         elif len(chosenBoxes) == 0:
    #             print("SUMITO")
    #             return False

    return act

    # randomChain = random.choice(possibleChains)
    # act = action(randomChain, randomMove, color, True)


    # while possibleChains is False:
    #     if len(chosenBoxes) > 1:
    #         chosenBoxes.remove(randomMarble)
    #         randomMarble = random.choice(chosenBoxes)
    #         # possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    #         return possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    #     else:
    #         # print("no marbles")
    #         return False
    
    # randomChain = random.choice(possibleChains)
    # a = action(randomChain, randomMove, color, False)

    # while a is False:
    #     if myMoves != []:
    #         randomMove = random.choice(myMoves)
    #         myMoves.remove(randomMove)
    #     else:
    #         if len(chosenBoxes) > 1:
    #             chosenBoxes.remove(randomMarble)
    #             randomMarble = random.choice(chosenBoxes)
    #             possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    #             while possibleChains is False:
    #                 if len(chosenBoxes) > 1:
    #                     chosenBoxes.remove(randomMarble)
    #                     randomMarble = random.choice(chosenBoxes)
    #                     possibleChains = possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(moves.values()))
    #                 else:
    #                     return False
    #             randomChain = random.choice(possibleChains)
    #         elif len(chosenBoxes) == 1:
    #             possibleChain =  possibleChainsFromPoint(randomLength, chosenBoxes[0], None, None, [], [], list(moves.values()))
    #             chosenBoxes.remove(randomMarble)
    #         else:
    #             return False
    #     a = action(randomChain, randomMove, color, True)
    
    # return color, randomChain, a
        
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

    print(randomPlay("W"))

    color = random.choice(["W", "B"])
    result = randomPlay(color)

    while result[0] is True:
        color = random.choice(["W", "B"])
        result = randomPlay(color)
        print(result)
        time.sleep(.01)


    # scoreWhite = opposingMarblesOut('B')
    # scoreBlack = opposingMarblesOut('W')
    # color = random.choice(('W', 'B'))
    
    # while scoreBlack < 6 and scoreWhite < 6:
    #     scoreWhite = opposingMarblesOut('B')
    #     scoreBlack = opposingMarblesOut('W')

    #     if color == 'B':
    #         color = 'W'
    #     elif color == 'W':
    #         color = 'B'

    #     print(randomPlay(color))

    # displayBoard(board)
    # print(scoreBlack, scoreWhite)
    # if scoreBlack == 6:
    #     winner = "Black"
    # else:
    #     winner = "White"

    # print(f"the winner is : {winner}")