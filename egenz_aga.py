# -*- coding: utf-8 -*-

import mne
import numpy as np
import os
import os.path as op
import matplotlib.pyplot as plt

# options
t1_or_t2 = 't1'
age = 'all'
gender = 'all'
n = 50  # the sample number. Choose 50 to get N=100 and choose 125 to get N=400
lh_picks = ['MEG1612', 'MEG1622', 'MEG1632', 'MEG1642', 'MEG0232',
         'MEG0242', 'MEG1613', 'MEG1623', 'MEG1633', 'MEG1643', 'MEG0233', 'MEG0243']  # include lh and rh
rh_picks = ['']
lh_picks.sort()
rh_picks.sort()

# setting up

blocks = ['faces', 'emojis', 'thumbs']
parent_dir = '/storage/genz_active/%s/fixed_hp/' % t1_or_t2
skip = ['genz115_9a', 'genz526_17a']
subjects = [x for x in os.listdir(parent_dir) if 'genz' in x and op.isdir(parent_dir + x) and not np.in1d(x, skip)]
subjects.sort()

group_data = []
reg_data = []
reg_times = []
times = []

lh_pairs = np.unique([x[0:6] for x in lh_picks])
rh_pairs = np.unique([x[0:6] for x in rh_picks])

# calculate areal mean signal function
# epochs should be one subject, one block, one syllable,

def calc_ams(epochs, lh_picks, rh_picks):
    lh_picks.sort()
    rh_picks.sort()
    for hemi in ['lh', 'rh']:
        picks = lh_picks if 'lh' in hemi else rh_picks
        # make sure our epochs only have the picks we want
        epochs = epochs.pick_channels(picks)
        data = epochs.get_data()
        # square the gradiometer channels
        data_sq = np.square(data)
        # sum together pairs of gradiometers (picks are sorted numerically, such that grad pairs follow sequentially)
        sum_data = np.zeros(shape=(140, 6, 213))
        for i in np.arange(1, 12, 2):
            num = int((i - 1) / 2)
            sum_data[:, num, :] = np.add(data_sq[:, i, :], data_sq[:, i - 1, :])   # add the first, third, etc elements of axis 1 to the 0th, second, etc elements
        # calculate the square root of the sums
        sqrt_data = np.sqrt(sum_data)
        # average the sums over the temporal area
        mean_data = np.mean(sqrt_data, axis=1)
        if 'lh' in hemi:
            lh_ams = mean_data
        else:
            rh_ams = mean_data

    return lh_ams, rh_ams


for subject in subjects:
    epo_path = op.join(parent_dir, subject, 'epochs', 'All_80-sss_%s-epo.fif' % subject)
    epo = mne.read_epochs(epo_path)

# Overall s01 vs s02 comes first

    # separate out condition epochs
    all_s01 = epo['learn/s01']
    all_s02 = epo['learn/s02']

    # get the ams for each set

    lh_s01, rh_s01 = calc_ams(all_s01, lh_picks, rh_picks)
    lh_s02, rh_s02 = calc_ams(all_so2, lh_picks, rh_picks)

    # get the differences

    lh_diff = lh_s01 - lh_s02
    rh_diff = rh_s01 - rh_s02

    # at this point, data is still in shape (140, 213)

    # return the differences saved in an accessible format for graphing

# block by block s01 vs s02 comes next

    for block in blocks:
        es01 = epo['%s/learn/s01' % block]
        es02 = epo['%/learn/s02' % block]

        lh_es01 = 





