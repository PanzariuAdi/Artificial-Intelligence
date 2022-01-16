from os import read
import copy
import numpy as np

file = open("maze.txt", "r")
lines = file.readlines()
maze = []

for line in lines:
    line = list(map(int, line.split(" ")))
    maze.append(line)

n = len(maze)
N = n * n

location_to_state = dict()
for i in range (1, N + 1):
    location_to_state['L' + str(i)] = i - 1    
actions = [x for x in range(N)]

maze_states = []
c = 1
for i in range (n):
    line = []
    for j in range (n):
        cell = 'L' + str(c)
        line.append(cell)
        c = c + 1
    maze_states.append(line)
rewards = np.zeros((N, N), dtype = None, order = 'C')

for row in range (n):
    for col in range (n):
        if row > 0: # UP
            l_up = maze_states[row - 1][col]
            l_up = int(l_up[1:]) - 1
            l_curr = l_up + n

            if maze[row - 1][col] == 1:
                rewards[l_curr, l_up] = -1000
            else:
                rewards[l_curr, l_up] = 1
        if row < n - 1: # DOWN
            l_down = maze_states[row + 1][col]
            l_down = int(l_down[1:]) - 1
            l_curr = l_down - n

            if maze[row + 1][col] == 1:
                rewards[l_curr, l_down] = -1000
            else:
                rewards[l_curr, l_down] = 1
        if col > 0: # LEFT
            l_left = maze_states[row][col - 1]
            l_left = int(l_left[1:]) - 1
            l_curr = l_left + 1

            if maze[row][col - 1] == 1:
                rewards[l_curr, l_left] = -1000
            else:
                rewards[l_curr, l_left] = 1
        if col < n - 1:
            l_right = maze_states[row][col + 1]
            l_right = int(l_right[1:]) - 1
            l_curr = l_right - 1

            if maze[row][col + 1] == 1:
                rewards[l_curr, l_right] = -1000
            else:
                rewards[l_curr, l_right] = 1

state_to_location = dict((state, location) for location, state in location_to_state.items())

gamma = 0.75 # Discount factor
alpha = 0.9 # Learning rate

class QAgent():
    def __init__(self, alpha, gamma, location_to_state, actions, rewards, state_to_location):
        self.gamma = gamma
        self.alpha = alpha
        self.location_to_state = location_to_state
        self.actions = actions
        self.rewards = rewards
        self.state_to_location = state_to_location

        M = len(location_to_state)
        self.Q = np.zeros((M, M), dtype = None, order = 'C')

    def training(self, start_location, end_location, iterations):
        rewards_new = np.copy(self.rewards)

        ending_state = self.location_to_state[end_location]
        rewards_new[ending_state, ending_state] = 1000
        

        for i in range (iterations):
            current_state = np.random.randint(0, N)
            playable_actions = []

            for j in range (N):
                if rewards_new[current_state, j] != 0:
                    playable_actions.append(j)

            next_state = np.random.choice(playable_actions)
            TD = rewards_new[current_state, next_state] + self.gamma * self.Q[next_state, np.argmax(self.Q[next_state,])] - self.Q[current_state, next_state]
            self.Q[current_state, next_state] += self.alpha * TD
        
        route = [start_location]
        next_location = start_location

        self.get_optimal_route(start_location, end_location, next_location, route, self.Q)
        

    def get_optimal_route(self, start_location, end_location, next_location, route, Q):

        while next_location != end_location:
            starting_state = self.location_to_state[start_location]
            next_state = np.argmax(Q[starting_state,])
            next_location = self.state_to_location[next_state]
            route.append(next_location)
            start_location = next_location
        print (route)

qagent = QAgent(alpha, gamma, location_to_state, actions, rewards, state_to_location)
qagent.training('L1', 'L16', 1000)