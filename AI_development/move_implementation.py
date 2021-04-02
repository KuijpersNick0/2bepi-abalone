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


def displayGrid(board):
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
        Check if all marbles have the right color.
    """
    for marble in marblesArray:
        if color != 'W' or color != 'B':
            print(f"[ERROR] there is no marble in this case - marble : {marblesArray}")
            return False
        if board[marble[0]][marble[1]] != color:
            print(f"[ERROR] wrong color - marbles : {marblesArray}, color :{color}")
            return False
    return True

def chain(marblesArray, move=None):
    """
        Check if all marbles make a chain with a direction.\n
        Return the direction if True.
    """
    if len(marblesArray) > 3:
        return False
    
    if len(marblesArray) == 1:
        return move

    marblesArray.sort()
    # print(marblesArray)
    
    if move is not None:
        if marblesArray[0] == [marblesArray[1][0] + move[0], marblesArray[1][1] + move[1]]:
            # print(f"My move is {move}")
            return chain(marblesArray[1:], move=move)

    for currentMove in moves.values():
        # print("loop in moves...")
        if marblesArray[0] == [marblesArray[1][0] + currentMove[0], marblesArray[1][1] + currentMove[1]]:
            # print(f"found move : {currentMove} !")
            return chain(marblesArray[1:], move=currentMove)
    
    return False

def lineMove(marblesArray, moveName):
    """
        Do the line move or return False
    """
    vectorMove = moves[moveName]
    vectorChain = chain(marblesArray)
    lastMarble = marblesArray[0]
    # print(lastMarble)

    if vectorChain is None:
        return False

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
    
        # print(lastMarble)
        # print(board[lastMarble[0]][lastMarble[1]])

        nextValue = board[lastMarble[0] + vectorMove[0]][lastMarble[1] + vectorMove[1]] 
        if nextValue == 'X':
            print(f"[ERROR] movement out of board - marbles : {marblesArray}, move : {moveName}")
            return False
        elif nextValue == board[lastMarble[0]][lastMarble[1]]:
            # print(nextValue, board[lastMarble[0]][lastMarble[1]])
            print("[ERROR] there is already one of your marbles there - marbles : {marblesArray}, move : {moveName}")
            return False
        elif nextValue == 'E':
            marblesMoved = []
            for marble in marblesArray:
                marblesMoved.append([marble[0] + vectorMove[0], marble[1] + vectorMove[1]])

            return marblesMoved
    return False

def arrowMove(marblesArray, moveName):
    updatedMarbles = []
    for marble in marblesArray:
        nextMarbleValue = board[marble[0] + moves[moveName][0]][marble[1] + moves[moveName][1]]
        currentMarbleValue = board[marble[0]][marble[1]]
        if nextMarbleValue == currentMarbleValue:
            print("[ERROR] there is already one of your marbles there - marbles : {marblesArray}, move : {moveName}")
            return False
        elif nextMarbleValue == 'X':
            print("[ERROR] movement out of board - marbles : {marblesArray}, move : {moveName}")
            return False
        
        updatedMarbles.append([marble[0] + moves[moveName][0], marble[1] + moves[moveName][1]])
    return updatedMarbles

def soloMove(marblesArray, moveName):
    # print(marbleArray, moves[moveName])
    if len(marblesArray) == 1:
        nextValue = board[marblesArray[0][0] + moves[moveName][0]][marblesArray[0][1] + moves[moveName][1]]
        if nextValue == 'X':
            print(f"[ERROR] movement out of board - marbles : {marblesArray}, move : {moveName}")
            return False
        elif nextValue == board[marblesArray[0][0]][marblesArray[0][1]]:
            print("[ERROR] there is already one of your marbles there - marbles : {marblesArray}, move : {moveName}")
        return [[marblesArray[0][0] + moves[moveName][0], marblesArray[0][1] + moves[moveName][1]]]
    
    print("[ERROR] you don't move a single marble - marbles : {marblesArray}, move : {moveName}")
    return False

def updateBoard(oldPositions, newPositions):
    color = board[oldPositions[0][0]][oldPositions[0][1]]
    # print(color)
    # print(oldPositions)
    # print(newPositions)

    for marble in oldPositions:
        board[marble[0]][marble[1]] = 'E'
    
    for marble in newPositions:
        # print(marble)
        board[marble[0]][marble[1]] = f"{color}"

def sumito(marblesToMove):
    pass



def Action(marblesArray, moveName, color):
    newPositions = []
    print("")

    if not colored(marblesArray, color):
        return False

    if not existingDirection(moveName):
        print(f"[ERROR] wrong movement - marbles : {marblesArray}, move : {moveName}, color :{color}")
        return False

    if chain(marblesArray) is not None:
        if lineMove(marblesArray, moveName) is not False:
            # print("line ?")
            newPositions = lineMove(marblesArray, moveName)
        else:
            # print("arrow ?")
            newPositions = arrowMove(marblesArray, moveName)
    else:
        # print("solo ?")
        newPositions = soloMove(marblesArray, moveName)


    if not newPositions:
        # displayGrid(board)
        return False

    updateBoard(marblesArray, newPositions)   


if __name__ == '__main__':
    # Action([[0,0], [1, 0]], "SW", "W")
    # Action([[0,1],[1,2],[2,3]], "SE", "W")
    # Action([[6,4]], "NW", "B")
    Action([[5,3]], "NW", "B")
    displayGrid(board)

    print("")

