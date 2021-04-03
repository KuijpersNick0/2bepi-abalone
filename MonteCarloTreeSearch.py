import datetime
from random import choice
import csv
 
class MonteCarloTreeSearch(object):

    def __init__(self, board, **kwargs):
        self.board = board  
        self.states = [] #l'ensemble des nodes en quelque sorte

        self.wins = {} #les gainzzz
        self.plays = {} #les simulations (state, player)

        self.C = kwargs.get('C', 1.4) #notre variable dexploration au plus grand au + on explore

        self.max_moves = kwargs.get('max_moves', 1000) #le max de moves qu'on laisse la machine simuler

        seconds = kwargs.get('time', 300) #cb de temps on simule
        self.calculation_time = datetime.timedelta(seconds=seconds)

    with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["state", "wins", "plays","probability"])
    
    def writeMyCsv(self, state, wins,plays):
        pass

    def update(self, state):
        self.states.append(state)

    def get_play(self):

        # SI ON VEUT JOUER DES VRAIS GAMES SANS EXPLORER: DECOMMENT 
        '''
        state = self.states[-1] 
        Player = self.board.current_player(state) 
        legal = self.board.legal_plays(self.states[:]) #legal est une liste de tout les nodes qu'on peut explorer

        if not legal:
            return False
        if len(legal) == 1:
            return legal[0]
        '''
        games = 0 
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.calculation_time: #on simule jusqu'a ce qu'on veut que ça s'arrête
            self.run_simulation()
            games += 1

        '''
        moves_states = [(p, self.board.next_state(state, p)) for p in legal] #ON ENREGISTRE ICI LE MOVE QUI CORRESPONDS AU NODE
        percent_wins, move = max((self.wins.get((player, S), 0) / self.plays.get((player, S), 1), p) for p, S in moves_states)
        #tuple (%victoire, moves) EN GROS ON MET LES POIDS SUR LES NODES
        return move
        '''

    def run_simulation(self):
        plays, wins = self.plays, self.wins

        visited_states = set()
        states_copy = self.states[:] #on fait une copie des notre jeu pour pas déconner s'il y a  de la casse
        state = states_copy[-1]
        player = self.board.current_player(state)

        expand = True 
        for t in xrange(self.max_moves): 
            legal = self.board.legal_plays(states_copy)

            play = choice(legal) #choissis un play random
            state = self.board.next_state(state, play) 
            states_copy.append(state)

            '''
            #POUR JOUER SERIEUX
            moves_states = [(p, self.board.next_state(state, p)) for p in legal]

            if all(plays.get((player, S)) for p, S in moves_states):
                #SI ON A TOUT LES STATS GO LES JOUER

                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, move, state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                #OU SINON CHOIX RANDOM
                move, state = choice(moves_states)
            '''

            if expand and (player, state) not in self.plays: #on initialise si on l'as jamais joué
                #expand = False si on veut jouer des trucs safe
                self.plays[(player, state)] = 0
                self.wins[(player, state)] = 0

            visited_states.add((player, state))
            
            player = self.board.current_player(state)
            winner = self.board.winner(states_copy) #methode ds board qui check si on a gagné
            if winner:
                break #notre sortie seulement si on gagne


        for player, state in visited_states: #on soigne les stats enfin
            if (player, state) not in self.plays:
                continue
            self.plays[(player, state)] += 1
            if player == winner:
                self.wins[(player, state)] += 1


    
