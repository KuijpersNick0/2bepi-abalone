import random
import time
from collections import defaultdict
import math
from abc import ABC, abstractmethod

class MCTS_V2:
    def __init__(self, coef_exploration=1):
        self.Q = defaultdict(int) #les "wins" de chaque node
        self.N = defaultdict(int) #les visites de chaque node
        self.children =dict() #les enfants de chaque node
        self.coef_exploration = coef_exploration

    def choose(self, node):
        #choisit le meilleur node, continuation de la game
        if node.is_terminal():
            raise RuntimeError(f"choose called on terminal {node}")

        if node not in self.children:
            return node.randomPlay(current_player)

        def score(n):
            if self.N[n] == 0:
                return float("-inf") 
            return self.Q[n] + self.N[n]
        return max(self.children[node],key = score)

    def do_rollout(self, node):
        #on recherche une node en plus
        path = self._select(node)
        leaf = path[-1]
        self._expand(leaf)
        reward = self._simulate(leaf)
        self._backpropagate(path, reward)

    def _select(self, node):
        #Cherche des nodes de nodes inexploré
        path = []
        while True:
            path.append(node)
            if node not in self.children or not self.children[node]:
                #Pas exploré ou terminal
                return path
            unexplored = self.children[node] - self.children.keys()

            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self._uct_select(node)  # On cherche 1 plus loin

    def _expand(self, node):
        #Update le children dict avec les enfants du node
        if node in self.children:
            return #deja dedans
        self.children[node] = node.legal_plays(current_player)

    def _simulate(self, node):
        #simule le gain ou pas
        invert_winner = True
        while True:
            if node.is_terminal():
                winner = node.winner()
                return 1 - winner if invert_winner else winner
            node = node.randomPlay(current_player)
            invert_winner = not invert_winner

    def _backpropagate(self, path, winner):
        #on remonte winner
        for node in reversed(path):
            self.N[node] += 1
            self.Q[node] += winner
            winner = 1 - winner # 1 pour moi, 0 pour mon enemie

    def _uct_select(self, node):
        #UCB1 methode équilibre exploration/exploitation
        
        #Tout les enfants node devraient etre explorées
        assert all(n in self.children for n in self.children[node])

        log_N_vertex = math.log(self.N[node])

        def uct(n):
            return self.Q[n] / self.N[n] + self.coef_exploration * math.sqrt(log_N_vertex /self.N[n])

        return max(self.children[node], key=uct)

class Node(ABC):
    #la representation d'un état (un node)

    @abstractmethod
    def legal_plays(self, current_player):
        return set()

    @abstractmethod
    def randomPlay(self, current_player):
        return None

    @abstractmethod
    def is_terminal(self):
        return True

    @abstractmethod
    def winner(self):
        return 0

    #@abstractmethod
    #def __hash__(self):
    #    "Nodes must be hashable"
    #    return 123456789

    #@abstractmethod
    #def __eq__(node1, node2):
    #    "Nodes must be comparable"
    #    return True

board = [
        ["W", "W", "W", "W", "W", "X", "X", "X", "X"],
        ["W", "W", "W", "W", "W", "W", "X", "X", "X"],
        ["E", "E", "W", "W", "W", "E", "E", "X", "X"],
        ["E", "E", "E", "E", "E", "E", "E", "E", "X"],
        ["E", "E", "E", "E", "E", "E", "E", "E", "E"],
        ["X", "E", "E", "E", "E", "E", "E", "E", "E"],
        ["X", "X", "E", "E", "B", "B", "B", "E", "E"],
        ["X", "X", "X", "B", "B", "B", "B", "B", "B"],
        ["X", "X", "X", "X", "B", "B", "B", "B", "B"]]

moves = {
        "NW":[-1, -1],
        "NE":[-1,  0],
        "E" :[ 0,  1],
        "SW":[ 1,  0],
        "SE":[ 1,  1],
        "W" :[ 0, -1]}     

current_player = "W"

class Board(Node):    

    def __init__(self):
        self.current_player = current_player
        self.board = board
        self.moves = moves
        self.possibleDirections = list(moves.values())

    def current_player(self):
        return current_player

    #def next_state(self, marblesArray, moveName, player):
    #    self.action(marblesArray, moveName, player, True)
    #    if player == "W":
    #        current_player = "B"
    #    else:
    #        current_player = "W"
    #    return (player, board, (marblesArray,moveName))

    def displayBoard(self, board):
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

    def existingDirection(self, moveName):
        """
            Checks if the direction exists.
        """
        if self.moves.get(moveName) is None:
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
                # print("no marble here", marblesArray, marble, board[marble[0]][marble[1]])
                return "caseWithoutMarbleError"
            else:
                if self.board[marble[0]][marble[1]] != color:
                    # print("wrong color marble")
                    return "wrongColorError"

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

        for currentMove in self.moves.values():
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
        vectorMove = self.moves[moveName]
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
                nextMarbleValue = self.board[marble[0] + self.moves[moveName][0]][marble[1] + self.moves[moveName][1]]
                currentMarbleValue = self.board[marble[0]][marble[1]]
                if nextMarbleValue == currentMarbleValue:
                    return False, "allyPresenceError", marblesArray, moveName
                elif nextMarbleValue == 'X':
                    return False, "outLimitError", marblesArray, moveName
                elif nextMarbleValue == 'E':
                    pass
                else:
                    try:
                        if self.board[marble[0] + 2 * self.moves[moveName][0]][marble[1] + 2 * self.moves[moveName][1]] == nextMarbleValue:
                            return False, "opponentMoveError", marblesArray, moveName
                    except:
                        return False, "outOfRange"

                updatedMarbles.append([marble[0] + self.moves[moveName][0], marble[1] + self.moves[moveName][1]])
    
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
                nextValue = self.board[marblesArray[0][0] + self.moves[moveName][0]][marblesArray[0][1] + self.moves[moveName][1]]
            except:
                nextValue = self.board[marblesArray[0][0]][marblesArray[0][1]]

            if nextValue == 'X':
                return False, "outLimitError"
            elif nextValue == currentValue:
                return False, "allyPresenceError"
            elif nextValue == 'E':
                pass
            else:
                return False, "opponentMoveError"

            marbleMoved = [[marblesArray[0][0] + self.moves[moveName][0], marblesArray[0][1] + self.moves[moveName][1]]]
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

    def action(self, marblesArray, moveName, color, update=False):
        """
            - Checks the marble's color\n
            - Checks the direction existence\n
            - Checks the marbles alignment\n
            \t- Tries making a lineMove\n
            \t- If lineMove returns an error, tries making an arrowMove\n
            \t- If arrowMove returns an error, tries making a soloMove\n
            - If lineMove, arrowMove and soloMove return errors, the program returns False
        """
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

    def possibleChainsFromPoint(self, lengthChain, referenceMarble, possibleDirections, currentMarble=None, move=None, chain=[], chainsList=[]):            
        possibleDirections0 = self.possibleDirections
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
            possibleDirections0.remove(move)
            return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, None, None, [], chainsList)

        color = self.board[referenceMarble[0]][referenceMarble[1]]

        if move is None:
            for myMove in possibleDirections0:
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
                            return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, None, myMove, [], chainsList)
                        return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, None, myMove, chain, chainsList)

                if nextMarble[0] != -1 and nextMarble[0] != 9 and nextMarble[1] != -1 and nextMarble[1] != 9:
                    nextMarbleColor = self.board[nextMarble[0]][nextMarble[1]]  
                    if nextMarbleColor == color:
                        return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, currentMarble, myMove, chain, chainsList)
                else:
                    possibleDirections0.remove(myMove)
                    return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, None, None, [], chainsList)
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
                    return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, nextMarble, move, chain, chainsList)
            
            previousMarble = [referenceMarble[0] - move[0], referenceMarble[1] - move[1]]
            if (previousMarble[0] != -1 and previousMarble[0] != 9) and (previousMarble[1] != -1 and previousMarble[1] != 9):
                previousMarbleColor = self.board[previousMarble[0]][previousMarble[1]]

                if previousMarbleColor == color:
                    chain.append(previousMarble)
                    chain.sort()
                    if chainsList.__contains__(chain) is not True and len(chain) == lengthChain:
                        chainsList.append(chain)
                        return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, previousMarble, move, [], chainsList)

            possibleDirections0.remove(move)
            return self.possibleChainsFromPoint(lengthChain, referenceMarble, possibleDirections0, None, None, [], chainsList)

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
        myMoves = list(self.moves.keys())

        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if value == color:
                    chosenBoxes.append([i,j])
           
        randomMarble = random.choice(chosenBoxes)
        chains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(self.moves.values()))
        randomMove = random.choice(myMoves)
    
        possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(self.moves.values()))
        
        while possibleChains == "notMoveFoundError":
            if len(chosenBoxes) > 1:
                chosenBoxes.remove(randomMarble)
                randomMarble = random.choice(chosenBoxes)
                possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(self.moves.values()))
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
                    possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(self.moves.values()))
                    while possibleChains == "notMoveFoundError":
                        if len(chosenBoxes) > 1:
                            chosenBoxes.remove(randomMarble)
                            randomMarble = random.choice(chosenBoxes)
                            possibleChains = self.possibleChainsFromPoint(randomLength, randomMarble, None, None, [], [], list(self.moves.values()))
                        else:
                            return False
                    randomChain = random.choice(possibleChains)
                elif len(chosenBoxes) == 1:
                    possibleChain =  self.possibleChainsFromPoint(randomLength, chosenBoxes[0], None, None, [], [], list(self.moves.values()))
                    chosenBoxes.remove(randomMarble)
                else:
                    return False
            a = self.action(randomChain, randomMove, color, True)
    
        return color, randomChain, a
        
    def opposingMarblesOut(self, yourColor):
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

    def legal_plays(self, player):
        allMoves = set()

        chosenBoxes = []
        myMoves = list(self.moves.keys())
        lengthChains = 2
    
        for i,row in enumerate(self.board):
            for j,value in enumerate(row):
                if value == player:
                    chosenBoxes.append([i,j])

        for i in range(lengthChains):
            for j in chosenBoxes:
                possibleChains = self.possibleChainsFromPoint(i, j, None, None, [], [], list(self.moves.values())) #Peut-etre enlever les doublons je comprends pas parfaitement la methode

        for i in possibleChains:
            for j in myMoves:
                if self.action(i, j, player, False) != False:
                    allMoves.append(i,j)
        return allMoves

    def is_terminal(self):        
        if len(self.legal_plays(current_player)) == 0 :
            return True
        else:
            return False

    def winner(self, player, board):

        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")

        winner = " "
        scoreWhite = self.opposingMarblesOut('B')
        scoreBlack = self.opposingMarblesOut('W')

        if scoreBlack == 6:
            winner0 = "W"
        elif scoreWhite == 6:
            winner0 = "B"

        if player == winner0:
            winner = 1
        else: 
            winner = 0

        return winner

def play_game():
    tree = MCTS_V2()
    game = Board()
    game.displayBoard(board)
    
    games = 0
   
    while True:
        for _ in range(50):
            tree.do_rollout(game)
        game = tree.choose(game)         
        games+=1
        print(games)
        if game.terminal:
            break





if __name__ == '__main__':
    #scoreWhite = opposingMarblesOut('B')
    #scoreBlack = opposingMarblesOut('W')
    #color = random.choice(('W', 'B'))
    
    #while scoreBlack < 6 and scoreWhite < 6:
    #    scoreWhite = opposingMarblesOut('B')
    #    scoreBlack = opposingMarblesOut('W')

    #    if color == 'B':
    #        color = 'W'
    #    elif color == 'W':
    #        color = 'B'

    #    randomPlay(color)
    #displayBoard(board)
    #print(scoreBlack, scoreWhite)
    #if scoreBlack == 6:
    #    winner = "White"
    #else:
    #    winner = "Black"

    #print(f"the winner is : {winner}")


    #test = Board()
    #test.displayBoard(board)
    #test.randomPlay("W")
    #test.displayBoard(board)

    
    #simu = MonteCarloTreeSearch(board, current_player="W")
    #simu.get_play()

    #from Abalone_V2 import MCTS_V2, Node, Board
    
    play_game()
 