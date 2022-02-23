# -*- coding: utf-8 -*-

import mne
import os.path as op
import numpy as np
import matplotlib.pyplot as plt

# get input to indicate order

m1 = 'Choose visual.\n e = emojis, f = faces'
m2 = 'Indicate feedback order. \n' \
     'p = positive feedback first, n = negative feedback first'

fbk_type = get_keyboard_input()
pos_or_neg = get_keyboard_input()

# visual triggers:
# arrow onset (any block): 2^12 (4096)
# pos, neg vis onset during positive block = 2^10, +2^11 (1024, 3072)
# pos, neg vis onset during negative block = 2^9, +2^11 (512, 2560)

# auditory triggers:
# S1, S2, S3 during positive = 2, 10, 18
# S1, S2, S3 during negative = 1, 9, 17

# key press triggers
# blue = left = 5 (32)
# yellow = right = 6 (64)
# 7 (128)
# 8 (256)

# instantiate the ProPixx and set its attributes
pixx = blah
pixx.attribute()




# set up the visual stream
v_buff =



# set up the auditory stream

a_buff =

# start the vis

# start the aud
