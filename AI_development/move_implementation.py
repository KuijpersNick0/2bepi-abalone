
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
    "SE":[ 1,  1],
    "SW":[ 1,  0],
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
        Checks if all marbles have the right color.
    """
    for marble in marblesArray:
        if board[marble[0]][marble[1]] != 'W' and board[marble[0]][marble[1]] != 'B':
            return "caseWithoutMarbleError"
        else:
            if board[marble[0]][marble[1]] != color:
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
        return "chainError"
    
    if vectorChain == None and opponent is False:
        return "soloMarbleInfo"

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
    
        currentValue = board[lastMarble[0]][lastMarble[1]]
        try:
            nextValue = board[lastMarble[0] + vectorMove[0]][lastMarble[1] + vectorMove[1]] 
        except:
            return "allyOutOfBoardError"

        if nextValue == 'X':
            return "outLimitError"
        elif nextValue == currentValue:
            return "sameValueError"
        elif nextValue == 'E':
            marblesMoved = []
            for marble in marblesArray:
                marblesMoved.append([marble[0] + vectorMove[0], marble[1] + vectorMove[1]])
            updateBoard(marblesArray, marblesMoved)
            return True
        else:
            try: # ! test [CHECKED]
                lastOpponentMarbleValue = board[lastMarble[0] + len(marblesArray) * vectorMove[0]][lastMarble[1] + len(marblesArray) * vectorMove[1]]
            except:
                lastOpponentMarbleValue = board[lastMarble[0] + (len(marblesArray) - 1) * vectorMove[0]][lastMarble[1] + (len(marblesArray) - 1) * vectorMove[1]]
            
            if lastOpponentMarbleValue != 'E' and lastOpponentMarbleValue == 'X':
                return "NonEmptyError"
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

                updateBoard(opponentMarbles, opponentMarblesMoved)
                updateBoard(marblesArray, marblesMoved)
                return True
                
    return "nonAlignedError"

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
        return "singleMarbleInfo"

    for marble in marblesArray:
        nextMarbleValue = board[marble[0] + moves[moveName][0]][marble[1] + moves[moveName][1]]
        currentMarbleValue = board[marble[0]][marble[1]]
        if nextMarbleValue == currentMarbleValue:
            return "allyPresenceError"
        elif nextMarbleValue == 'X':
            return "outLimitError"
        elif nextMarbleValue == 'E':
            pass
        else:
            if board[marble[0] + 2 * moves[moveName][0]][marble[1] + 2 * moves[moveName][1]] == nextMarbleValue:
                return "opponentMoveError"

        updatedMarbles.append([marble[0] + moves[moveName][0], marble[1] + moves[moveName][1]])
    
    updateBoard(marblesArray, updatedMarbles)
    return True

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
            return "outLimitError"
        elif nextValue == currentValue:
            return "allyPresenceError"
        elif nextValue == 'E':
            pass
        else:
            return "opponentMoveError"

        marbleMoved = [[marblesArray[0][0] + moves[moveName][0], marblesArray[0][1] + moves[moveName][1]]]
        updateBoard(marblesArray, marbleMoved)
        return True
    
    return "notAsingleMarbleError"

def updateBoard(oldPositions, newPositions):
    """
        Adds changes into the last board.
    """
    color = board[oldPositions[0][0]][oldPositions[0][1]]

    for marble in oldPositions:
        board[marble[0]][marble[1]] = 'E'
    
    for marble in newPositions:
        board[marble[0]][marble[1]] = f"{color}"

def Action(marblesArray, moveName, color):
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
        if lm is not True:
            if am is not True:
                if sm is not True:
                    print(f"lineMove  : {lm}")
                    print(f"arrowMove : {am}")
                    print(f"soloMove  : {sm}")
                    return False

def legalMoves(marblesArray):
    legalMoves = []

    for moveName in moves:
        if lineMove(marblesArray, moveName) or arrowMove(marblesArray) or soloMove(marblesArray):
            legalMoves.append([marblesArray, moveName])

    return legalMoves


if __name__ == '__main__':
    # Action([[2,3],[2,4]], "SE", "W")
    # Action([[3,4],[3,5]], "SW", "W")
    # Action([[4,4],[4,5]], "SW", "W")
    # Action([[8,8],[7,8]], "NE", 'B')
    # Action([[7,7]], "NE", 'B')
    # Action([[0,0],[1,1],[2,2]], "SE", 'W')
    # Action([[3,3]], "SE", 'W')
    # Action([[2,2]], "SE", 'W')
    # Action([[3,3],[4,4],[5,5]], "SE", 'W')
    # Action([[6,6],[5,5]], "SE", 'W')
    # Action([[6,6],[7,7]], "SE", 'W')
    # Action([[8,8]], 'SW', 'W')
    Action([[8,8],[7,7],[6,6]], 'NW', 'B')
    Action([[7,8]], 'NW', 'B')
    Action([[8,6],[7,5],[6,4]], "NW", 'B')
    Action([[8,7],[7,6],[6,5]], "NW", 'B')
    # Action([[0,0],[0,1]], 'NE', 'W') # ! [CHECKED] peut-être que ça passe de l'autre côté, à tester !
    # Action([[1,5]], 'NE', 'W')
    # Action([[8,8],[7,7]], "SE", 'W')
    # Action([[8,6], [7,6]], "NE", 'B')
    # Action([[6,5],[7,6]], 'NW', 'B')
    
    displayBoard(board)
    # print(board)

    print("")
