import matplotlib.pyplot as plt
import random
import math
import numpy as np
from copy import copy

def distance(p1, p2):
    if p1 is None or p2 is None:
        return 0.0
    else:
        x1, y1 = p1
        x2, y2 = p2
        dist = math.sqrt((x1-x2)**2 + (y1-y2)**2)
    return dist

reward_pos = (0.75, 0.75)       # reward position - where the cheese is

class Maze:
    initial_state = (0.1, 0.1)
    reward_rad = 0.1                # reward radius - how close you have to be

    def __init__(self, reward_pos=reward_pos):
        self.state = self.initial_state
        self.end = False
        self.reward_pos = reward_pos

    def close_enough(self, state):
        a = np.array(state)
        b = np.array(self.reward_pos)
        d = np.sqrt(np.sum((a-b)**2))  # Euclidean distance to cheese
        if d < Maze.reward_rad:
            return True
        else:
            return False

    def reward(self, state):
        if state is None or not self.close_enough(state):
            return 0
        else:
            return 10

    def state_trans(self, state1, action1):
        if self.close_enough(state1):
            return None

        x1, y1 = state1
        dx, dy = action1

        x2 = min(max(0, x1+dx), 1)      # makes sure we can't go outside walls
        y2 = min(max(0, y1+dy), 1)

        return (x2, y2)

    def reward_trans(self, state1, action1, state2):
        if state2==None:
            return 0
        else:
            if self.close_enough(state2):
                return 10
            else:
                return 0


    def transition(self, action1):
        state1 = self.state
        state2 = self.state_trans(state1, action1)
        reward2 = self.reward_trans(state1, action1, state2)

        self.state = state2
        return (state2, reward2)

class ContAgent:
    def __init__(self, alpha=0.1, gamma=0.9, step=0.1, res=10):
        self.step = step
        self.alpha = alpha
        self.gamma = gamma
        self.res = res                              # res = resolution
        self.values = np.zeros((res, res))

    def policy(self, state):
        angle = random.uniform(0, math.pi*2)
        s = self.step
        (move_x, move_y) = (math.sin(angle*s), math.cos(angle*s))
        return move_x, move_y

    def featurize(self, state):         # divide space into grid-like areas
        x, y = state                    # for assigning value
        n = self.res-1
        vx = min(math.floor(self.res * x), n)
        vy = min(math.floor(self.res * y), n)
        return (vx, vy)

    def v_function(self, state):
        vx, vy = self.featurize(state)
        return self.values[vx, vy]

    def learn(self, state1, reward1, state2):
        g = self.gamma
        a = self.alpha
        vx1, vy1 = self.featurize(state1)
        v1 = self.v_function(state1)
        v2 = 0

        if state2 is not None:
            v2 = self.v_function(state2)
        rpe = reward1 + g*v2 - v1
        self.values[vx1, vy1] += a*rpe

