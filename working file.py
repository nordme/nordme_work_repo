# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.

"""

import os.path as op
import mnefun
import numpy as np
from score import (score, aud_in_names, aud_in_numbers,
                   pick_aud_cov_events, pick_vis_cov_events)


# coil 1 = 83 hz
# coil 2 = 143 hz
# coil 3 = 203 hz
# coil 4 = 263 hz
# coil 5 = 323 hz


# define variables we need

coil_choices = ['one', 'two', 'three', 'four', 'five']

coil_placement = ['back', 'front']

positions = ['control', 'down', 'fardown', 'forward']

s_freq = [1000, 2000]

lowpass = [330, 660]

dir_path = '/home/nordme/data/cHPI_test'

files = []


# report Elekta's measurements from digitizing





# report mne-python calculations for coil location and coil distances





# report discrepencies between original and measured, plus measured fit quality





