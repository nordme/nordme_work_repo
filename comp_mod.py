
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from copy import copy

#### SIMPLE RL #####

class Environment:
    st_seq = {'cue': 'wait',
              'wait': 'juice',
              'juice': None}
    st_vals = {'cue':0,
               'wait': 0,
               'juice':1,
               None: 0}

    def __init__(self):
        self.state = 'cue'

    def transition(self):
        state = self.state
        new_state = Environment.st_seq[state]   # returns new state
        new_reward = Environment.st_vals[new_state]   # retrieves val
        self.state = new_state
        return (new_state, new_reward)


class TDAgent:
    def __init__(self, gamma=0.9, alpha=0.1):
        self.v = {'cue':0,
                  'wait':0,
                  'juice':0,
                  None:0}

        self.gamma = gamma
        self.alpha = alpha

    def learn(self, orig_state, orig_reward, new_state):
        v_orig = self.v[orig_state]
        v_new = self.v[new_state]
        g = self.gamma
        a = self.alpha

        rpe = orig_reward + g*v_new - v_orig
        v_orig_update = v_orig + a*rpe

        self.v[orig_state] = v_orig_update

        # How accurate is my table showing state values?
        # Let's compare what I think of my new state to what I think of my old state
        # If the new state is more valuable, then the old state gets a boost in value
        # We're lending value backwards
        # If the new state is less valuable, then the old state value gets dinged
        # This sort of RL is designed to give a cue (prev state) valuable
        # by making it accept the value of the following state

def rl_loop(env, agent):
    while env.state is not None:
        state = env.state
        reward = env.st_vals[state]
        transition = env.transition() # returns new state and new st_val
        new_state = None
        if transition is not None:
            new_state = transition[0]
        agent.learn(state, reward, new_state)

def run_trials(environment, agent, n):
    for i in range(n):
        environment.state = 'cue'
        rl_loop(environment, agent)
        print(f'Trial: {n}')
        print('What James Bond knows so far: \n', agent.v)


e = Environment()
james_bond = TDAgent(gamma=0.5)

t1 = run_trials(e, james_bond, 10)





