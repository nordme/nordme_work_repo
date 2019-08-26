# -*- coding: utf-8 -*-

import mne
import mnefun
import numpy as np
import os
import os.path as op
import matplotlib.pyplot as plt

parent_dir = ''

subjects = [x for x in os.listdir(parent_dir) if '' in x and op.isdir(parent_dir + x)]
subjects.sort()

age = 'all'
gender = 'all'

fnames = ['%s_faces_learn_01_raw.fif', '%s_emojis_learn_01_raw.fif', '%s_thumbs_learn_01_raw.fif']
epochs = []

picks = []
time = 0.100

group_data = []

for subject in subjects:
    epo_path = op.join(parent_dir, subject, 'epochs', 'All_80-sss_%s-epo.fif' % subject)
    epo = mne.read_epochs(epo_path, picks)
    s01 = epo['s01']
    s03 = epo['s03']

    # average data to get good waveforms
    s01 = collapse_sensors(subject, s01, picks)
    s03 = collapse_sensors(subject, s03, picks)
    s01 = collapse_blocks(subject, s01, blocks)
    s03 = collapse_blocks(subject, s03, blocks)

    # calculate the differences between conditions
    dC = delta_c(subject, s01, s03, time)

    # put together array of differences at N=100
    n100 = delta_peak(subject, dC, time=0.1)
    peak = n100.max()

    # plot the difference values at N=100
    plot = plot_delta(subject, n100, time=0.1)
    save_name = op.join(parent_dir, subject, '%s_N100_delta_S01_S03.png' % subject)
    plot.savefig(save_name)
    plt.close()

    # save the subject data to the group data
    group_data.append([subject, peak])


# calculate group statistics

high_learners = []
mid_learners = []
low_learners = []

group_data = group_data[group_data[:,1].argsort()]  # sort the group data by epoch number so we can see who peaked earliest and latest
times = group_data[:, 1]
group_max = times.max
group_min = times.min
group_range = group_max - group_min
q1, q2, q3 = np.percentile(times, [25, 50, 75])
iqr = q3-q1
group_upperf = q3 + 1.5*iqr
group_lowerf = q1 - 1.5*iqr

for data in group_data:
    if data[1] >= group_upperf:
        high_learners.append(data)
    if data[1] <= group_lowerf:
        low_learners.append(data)
    else:
        mid_learners.append(data)

print('Upper fence: %s' % group_upperf)
print('Lower fence: %s' % group_lowerf)
print('Our high learners are: \n', high_learners)
print('Our low learners are: \n', low_learners)


def pick_subs(subjects, age, gender):



def collapse_sensors(subject, epochs, picks):

    return # array of sensor data by epoch as if from one single sensor

def collapse_blocks(subject, epochs, blocks):

    return # array of sensor data by epoch with trials from each block zipped then averaged

def delta_c(subject, c1_epochs, c2_epochs):
    # input: two sets of epochs from different conditions
    return # array of delta values by epoch number

def delta_peak(subject, delta_c, time):

    return # delta values sorted by epoch; can return peak values with no time specified or delta value at spec time

def plot_delta(subject, delta, time):

    return fig # return a plot with epoch number on the x-axis and delta_c values on the y-axis

def plot_dpeak(subject, delta_peak):

    return fig # return a plot with peak value, peak time noted; epochs by number on x-axis


    # separating f / e / t
#    for cond in ['faces', 'emojis', 'thumbs']:
#        sep_epo = mne.Epochs(epochs['learn/%s' % cond])
#        epochs = collapse_sensors(subject, fnames, sep_epo, picks)