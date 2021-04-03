"""
    state = {depth: 0, currentPlayer:'W'}

"""
import random

states = []
blackWins = 0
whiteWins = 0

def run_simulation(color, blackWins, whiteWins, states=[], depth=0, move=None):
    if blackWins == 6 or whiteWins == 6:
        return 1, color

    print(blackWins, whiteWins)

    if color == 'B':
        blackWins += random.choice((0,1))
        states.append(['B', blackWins])
        color = 'W'
    else:
        whiteWins += random.choice((0,1))
        states.append(['W', whiteWins])
        color = 'B'
    
    return run_simulation(color, blackWins, whiteWins, states, depth + 1)


print(run_simulation('W', blackWins, whiteWins))
