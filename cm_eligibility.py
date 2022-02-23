###### ELIGIBILITY TRACING RL (I.e. when memory matters) #######

import matplotlib.pyplot as plt
import random
import math
import numpy as np
from copy import copy

st_val = {'start':0,
          'opt_a':0,
          'opt_b':0,
          'middle':0,
          'win':1,      # win or loss depends on whether you chose
          'loss':0,     # option a or option b to begin with
          None:0
          }

def st_pf(history):    # state transition probability function (how to move)
    current_state = history[-1]
    next_state = None

    if current_state == 'start':
        choice_val = random.uniform(0, 1)
        if choice_val <= 0.5:
            next_state = 'opt_a'
        else:
            next_state = 'opt_b'

    elif current_state == 'opt_a' or current_state == 'opt_b':
        next_state = 'middle'

    elif current_state == 'middle':
        prev_st = history[-2]
        if prev_st == 'opt_a':
            next_state = 'win'
        elif prev_st == 'opt_b':
            next_state = 'loss'

    elif current_state == 'win' or current_state == 'loss':
        next_state = None

    return (next_state, st_val[current_state])

class EligAgent:
    def __init__(self, states = st_val.keys(), alpha=0.1, gamma=0.9, lam=0.9):
        self.v = {}
        self.e = {}
        for state in states:
            self.v[state] = 0.0
            self.e[state] = 0.0
        self.alpha = alpha
        self.gamma = gamma
        self.lam = lam

    def learn(self, orig_state, new_state, orig_reward):
        a = self.alpha
        g = self.gamma
        l = self.lam
        rpe = orig_reward + g*self.v[new_state] - self.v[orig_state]

        # lambda learning
        for state in self.e.keys():
            self.e[state] *= (l * g)    # let old traces decay over time
            if state == orig_state:
                self.e[state] += 1       # but upgrade the current trace

        for state in self.e.keys():
            self.v[state] += a * rpe * self.e[state]   # weight the learning
                                                    # by how current the trace is

def rl_loop(agent, n=1000):
    for i in range(n):
        history = ['start']

        while st_pf(history)[0] is not None:
            current_st = history[-1]
            next_st, current_rew = st_pf(history)
            history.append(next_st)
            agent.learn(current_st, next_st, current_rew)

        current_st = history[-1]
        next_st, current_rew = st_pf(history)
        history.append(next_st)
        agent.learn(current_st, next_st, current_rew)
        print(f'Trial: {n}')
        print('What Monk knows so far: \n', agent.v)

monk = EligAgent()
rl_loop(monk, 20)
