from itertools import product
import math
from operator import pos

class GameState:
    def __init__(self, state):
        self.state = state


class Mastermind:
    def __init__(self, nr_of_colors, nr_of_balls, k):
        self.steps = 0
        self.nr_of_colors = nr_of_colors
        self.nr_of_balls = nr_of_balls
        self.k = k
        self.colors = {index: nr_of_balls for index in range(nr_of_colors)}
        self.answer = self.get_random_balls()
        self.all_posibilities = self.generate_all_posibilities()
        self.all_posibilities_copy = self.all_posibilities.copy()

    def initial_state(self):
        return [1 for elem in range(self.k)]

    def final_state(self, state_a, state_b):
        if self.steps <= 2 * self.nr_of_colors:
            # if state_a.state == state_b.state:
            if state_a == state_b:
                return 2 # castiga B
            else:
                return 0 # nu castiga nimeni inca
        else:
            return 1 # castiga A


    def get_random_balls(self):
        list_of_balls = []
        for key in self.colors:
            for i in range(self.colors[key]):
                list_of_balls.append(key)
        import random
        count = self.k
        state = []
        while count:
            index = random.randint(0, len(list_of_balls) - 1)
            state.append(list_of_balls[index])
            list_of_balls.pop(index)
            count -= 1
        return list(map(str, state))


    def evaluate(self, state):
        return self.number_of_common_colors(state)


    def generate_all_posibilities(self):
        posibilities = []
        for posibility in product("0123", repeat = self.k):
            posibilities.append(list(posibility))
        return posibilities


    def minimax(self, state, depth, alpha, beta, max_player):
        if depth == 0 or self.final_state(state, self.answer):
            return self.evaluate(state), state
            
        if self.all_posibilities.__contains__(state):
            self.all_posibilities.remove(state)

        if max_player:
            value = -math.inf
            best_possibility = None

            for possibility in self.all_posibilities:
                evaluation = self.minimax(possibility, depth - 1, alpha, beta, False)[0]
                value = max(value, evaluation)
                alpha = max(alpha, value)

                if value == evaluation:
                    best_possibility = possibility

                if value >= beta:
                    break
            return value, best_possibility

        else:
            value = math.inf
            best_possibility = None

            for possibility in self.all_posibilities:
                evaluation = self.minimax(possibility, depth - 1, alpha, beta, True)[0]
                value = min(value, evaluation)
                beta = min(beta, value)

                if value == evaluation:
                    best_possibility = possibility

                if value <= alpha:
                    break
            return value, best_possibility


    def number_of_common_colors(self, state1):
        counter = 0
        for i in range(len(self.answer)):
            if state1[i] == self.answer[i]:
                counter += 1
        return counter
    
    def play_game(self):
        game_ended = False
        print (f'Answer is  : {self.answer}')
        while not game_ended:
            value, guessed_state = self.minimax(self.initial_state, 3, -math.inf, math.inf, True)
            self.steps += 1
            print (f'Guessed state : {guessed_state} ----------------- answer : {self.answer}')
            state = cl.final_state(self.answer, guessed_state)
            if state == 1:
                game_ended = True
                print("A won!")
            elif state == 2:
                game_ended = True
                print("B won!")


cl = Mastermind(4, 3, 4)
cl.play_game()
