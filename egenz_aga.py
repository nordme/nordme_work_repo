# -*- coding: utf-8 -*-
# author: nordme

import mne
import numpy as np
import os
import os.path as op
import matplotlib.pyplot as plt

# options
area = 'temporal' # options are: frontal, temporal, parietal, occipital
t1_or_t2 = 't1'
age = 'all'
gender = 'all'

if area == 'frontal':
    lh_picks = ['MEG0522', 'MEG0532', 'MEG0612', 'MEG0512', 'MEG0542', 'MEG0312',
                'MEG0523', 'MEG0533', 'MEG0613', 'MEG0513', 'MEG0543', 'MEG0313']
    rh_picks = ['MEG0912', 'MEG0942', 'MEG1022', 'MEG0922', 'MEG0932', 'MEG1212',
                'MEG0913', 'MEG0943', 'MEG1023', 'MEG0923', 'MEG0933', 'MEG1213']
elif area == 'temporal':
    lh_picks = ['MEG1612', 'MEG1622', 'MEG1632', 'MEG1642', 'MEG0232',
                'MEG0242', 'MEG1613', 'MEG1623', 'MEG1633', 'MEG1643', 'MEG0233', 'MEG0243']
    rh_picks = ['MEG2412', 'MEG2413', 'MEG2422', 'MEG2423', 'MEG2432',
                'MEG2433', 'MEG2442', 'MEG2443', 'MEG1332', 'MEG1333', 'MEG1342', 'MEG1343']
elif area == 'parietal':
    lh_picks = ['MEG0442', 'MEG0432', 'MEG0712', 'MEG1812', 'MEG1822', 'MEG0742',
                'MEG0443', 'MEG0423', 'MEG0713', 'MEG1813', 'MEG1823', 'MEG0743']
    rh_picks = ['MEG0722', 'MEG1142', 'MEG1132', 'MEG0732', 'MEG2212', 'MEG2222',
                'MEG0723', 'MEG1143', 'MEG1133', 'MEG0733', 'MEG2213', 'MEG2223']
else:           # occipital
    lh_picks = ['MEG1942', 'MEG1922', 'MEG1632', 'MEG1642', 'MEG0232',
                'MEG0242', 'MEG1613', 'MEG1623', 'MEG1633', 'MEG1643', 'MEG0233', 'MEG0243']
    rh_picks = ['MEG2412', 'MEG2413', 'MEG2422', 'MEG2423', 'MEG2432',
                'MEG2433', 'MEG2442', 'MEG2443', 'MEG1332', 'MEG1333', 'MEG1342', 'MEG1343']

lh_picks.sort()
rh_picks.sort()

# setting up

blocks = ['faces', 'emojis', 'thumbs', 'all']
parent_dir = '/storage/genz_active/%s/fixed_hp/' % t1_or_t2
save_dir = '/storage/genz_learners/t1/fixed_hp/%s' % area
skip = ['genz115_9a', 'genz526_17a', 'genz131_9a', 'genz214_11a', 'genz409_15a']
subjects = [x for x in os.listdir(parent_dir) if 'genz' in x and op.isdir(parent_dir + x) and not np.in1d(x, skip)]
# subjects = ['genz532_17a']
subjects.sort()
# subjects = subjects[0:5]

work_dir = parent_dir
group_data = []
reg_data = []
reg_times = []
times = []

# function to calculate areal mean signal
# epochs should be one subject, one block, one syllable

def calc_ams(epochs, block, lh_picks, rh_picks):
    lh_picks.sort()
    rh_picks.sort()
    for hemi in ['lh', 'rh']:
        picks = lh_picks if 'lh' in hemi else rh_picks
        if block == 'all':
            picked_eps = epochs['learn'].pick_channels(picks)
            array1 = np.array([picked_eps['faces'].get_data(), picked_eps['emojis'].get_data(),
                               picked_eps['thumbs'].get_data()])
            data = np.mean(array1, axis=0)
        else:
            picked_eps = epochs['%s/learn' % block].pick_channels(picks)
            data = picked_eps.get_data()
        # square the gradiometer channels
        data_sq = np.square(data)
        # sum together pairs of gradiometers (picks are sorted numerically, such that grad pairs follow sequentially)
        sum_data = np.zeros(shape=(140, 6, 213))
        for i in np.arange(1, 12, 2):
            num = int((i - 1) / 2)
            # add the first, third, etc elements of axis 1 to the 0th, second, etc elements
            sum_data[:, num, :] = np.add(data_sq[:, i, :], data_sq[:, i - 1, :])
        # calculate the square root of the sums
        sqrt_data = np.sqrt(sum_data)
        # average the temporal channels together
        mean_data = np.mean(sqrt_data, axis=1)
        if 'lh' in hemi:
            lh_ams = mean_data
        else:
            rh_ams = mean_data

    return lh_ams, rh_ams


# diffs should be from one subject, one block, one peak (N100 or N400); shape (140)

def plot_ams_epochs(diffs, save_name, block, hemi, peak):

    # plot the difference values at the given sample; x-axis is epoch number
    diffs_n = np.array(diffs)
    fig = plt.plot(diffs)
    plt.title('%s %s %s %s' % (subject, block, hemi, peak))
    plt.ylim(-2.55e-11, 2.5e-11)
    plt.ylabel('S01 - S02 areal mean signal')
    plt.xlabel('Epoch number')

    # add a regression curve to the plot
    x = np.arange(len(diffs_n))
    y = diffs_n
    regression_coeffs = np.polyfit(x, y, deg=5)
    curve = np.poly1d(regression_coeffs)
    plt.plot(x, curve(x), color='k', lw=8)

    plt.savefig(save_name)

    return fig


def plot_ams_bars(diffs, save_name, block, hemi, peak):
    blue = '#397489'
    red = '#894739'

    early = diffs[0:46].mean()
    mid = diffs[46:92].mean()
    late = diffs[92:138].mean()
    early, mid, late = early*1e13, mid*1e13, late*1e13
    colors = [[], [], []]
    for i, t in enumerate((early, mid, late)):
        if t > 0:
            colors[i] = blue
        else:
            colors[i] = red

    plt.figure()
    fig = plt.bar(x=np.arange(3), height=[early, mid, late], color=colors)
    plt.title('%s %s %s %s' % (subject, block, hemi, peak))
    plt.ylim(-50, 50)
    plt.ylabel('S01 - S02 areal mean signal averaged over trial blocks')
    plt.xticks(np.arange(3), labels=['Early trials', 'Mid trials', 'Late trials'])
    plt.savefig(save_name)

    return fig, early, mid, late


def bothhems_ams_bars(subject, heights, save_name, block):
    blue = '#397489'
    red = '#894739'

    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
    fig.suptitle('%s: Areal mean signal for subject %s' % (block, subject))
    plt.xticks(ticks=np.arange(3), labels=['Early', 'Mid', 'Late'])
    plt.ylim(ymin=-15, ymax=25)
    ax0, ax1, ax2, ax3 = axes.flatten()
    ax0.set_title("LH")
    ax1.set_title('RH')
    ax0.set_ylabel('N100')
    ax2.set_ylabel('N400')

    for i, ax in enumerate((ax0, ax1, ax2, ax3)):
        ydata = heights[i]
        colors = [[],[],[]]
        for r in range(3):
            colors[r] = red if ydata[r] < 0 else blue
        ax.bar(x=np.arange(3), height=ydata, color=colors)

    plt.savefig(save_name)
    
def plot_waveforms(subject, lh_s01, lh_s02, rh_s01, rh_s02, block, save_name):

    blue = '#397489'
    dkblue = '#175267'
    lmean1 = lh_s01.mean(axis=0)
    lmean2 = lh_s02.mean(axis=0)
    rmean1 = rh_s01.mean(axis=0)
    rmean2 = rh_s02.mean(axis=0)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharey=True)
    plt.suptitle('%s %s S01 and S02' % (subject, block))
    plt.ylabel('S01 and S02 areal mean signal')
    plt.xlabel('Time (samples)')
    ax1.plot(lmean1, color=blue)
    ax1.plot(lmean2, color=dkblue)
    ax2.plot(rmean1, color=blue)
    ax2.plot(rmean2, color=dkblue)

#    plt.ylim(0, 1e-12)
#    plt.xlim(xmin=-100, xmax=750)

    plt.savefig(save_name)

    return fig

for subject in subjects:
    epo_path = op.join(parent_dir, subject, 'epochs', 'All_80-sss_%s-epo.fif' % subject)
    epo = mne.read_epochs(epo_path)
    es01 = epo['s01']
    es02 = epo['s02']
    save_path = op.join(save_dir, subject)
    if op.isdir(save_path):
        print('Subject %s has an images directory.' % subject)
    else: 
        os.mkdir(save_path)

    # Calculate the ams data by block

    block_data = []

    for block in blocks:
        # get the ams for each set
        lh_s01, rh_s01 = calc_ams(es01, block, lh_picks, rh_picks)
        lh_s02, rh_s02 = calc_ams(es02, block, lh_picks, rh_picks)
        # get the differences (shape (140, 213))
        lh_diff = lh_s01 - lh_s02
        rh_diff = rh_s01 - rh_s02
        # average difference values over a 40 ms window surrounding the target peak time
        lh100 = lh_diff[:, 45:55].mean(axis=1)           # 50th sample = 200 ms after baseline starts, or 100 ms past 0
        rh100 = rh_diff[:, 45:55].mean(axis=1)
        lh400 = lh_diff[:, 120:130].mean(axis=1)         # 125th sample = 500 ms past baseline
        rh400 = rh_diff[:, 120:130].mean(axis=1)
        # Now data should be in shape (140)
        

        # Given the returned block data, spit out some graphs
        # GRAPH 1: Amp differences (S01-S02) at sample n over epochs
        # GRAPH 2: Bar graph showing averaged amp differences for early, mid and late epochs.

        for hemi, peak in [['lh', '100'], ['lh', '400'], ['rh', '100'], ['rh', '400']]:
            A = op.join(save_path, '%s_%s_%s_%s_%s_ams_epochs.png' % (subject, area, block, hemi, peak))
            B = op.join(save_path, '%s_%s_%s_%s_%s_ams_bars.png' % (subject, area, block, hemi, peak))

            if '400' in peak and 'lh' in hemi:
                plotA = plot_ams_epochs(diffs=lh400, save_name=A, block=block, hemi=hemi, peak=peak)
                plt.close()
                plotB, le400, lm400, ll400 = plot_ams_bars(diffs=lh400, save_name=B, block=block, hemi=hemi, peak=peak)
                plt.close()
            elif '100' in peak and 'lh' in hemi:
                plotA = plot_ams_epochs(diffs=lh100, save_name=A, block=block, hemi=hemi, peak=peak)
                plt.close()
                plotB, le100, lm100, ll100 = plot_ams_bars(diffs=lh100, save_name=B, block=block, hemi=hemi, peak=peak)
                plt.close()
            elif '400' in peak:
                plotA = plot_ams_epochs(diffs=rh400, save_name=A, block=block, hemi=hemi, peak=peak)
                plt.close()
                plotB, re400, rm400, rl400 = plot_ams_bars(diffs=rh400, save_name=B, block=block, hemi=hemi, peak=peak)
                plt.close()
            else:
                plotA = plot_ams_epochs(diffs=rh100, save_name=A, block=block, hemi=hemi, peak=peak)
                plt.close()
                plotB, re100, rm100, rl100 = plot_ams_bars(diffs=rh100, save_name=B, block=block, hemi=hemi, peak=peak)
                plt.close()

        # Add the block data to a text file
        if block == 'all':
            heights = [[le100, lm100, ll100], [re100, rm100, rl100], [le400, lm400, ll400], [re400, rm400, rl400]]
            hems_save = op.join(save_path, '%s_%s_all_both_hems.png' % (subject, area))
            plotC = bothhems_ams_bars(subject=subject, heights=heights, save_name=hems_save, block=block)
            plt.close()
            waves_save = op.join(save_path, '%s_%s_all_waveforms.png' % (subject, area))
            plotD = plot_waveforms(subject, lh_s01, lh_s02, rh_s01, rh_s02, block, waves_save)
            plt.close()
            if rl400 >= ll400 and rl100>=ll100:
                learner = 'rh_learner'
            elif rl400 <= ll400 and rl100 <= ll100:
                learner = 'lh_learner'
            else:
                learner = 'mixed'

            with open(op.join(save_dir, 'global_all_ams.txt'), 'ab') as fid:
                print('Adding a line to the global all ams file.')
                fid.write((('%s, %s, %s, %s, %s, %s \n' %
                            (subject, learner, ll100, ll400, rl100, rl400)).encode()))

            with open(op.join(save_dir, subject, '%s_%s_all_ams.txt' % (subject, learner)), 'ab') as fid:
                print('writing ams data to a csv at %s' % op.join(subject, '%s_all_ams.txt' % subject))
                fid.write(('%s: S01 - S02 areal mean signal \n' % block).encode())
                fid.write((('%s, %s, %s, %s \n' %
                            ('left 100:', le100, lm100, ll100)).encode()))
                fid.write((('%s, %s, %s, %s \n' %
                            ('left 400:', le400, lm400, ll400)).encode()))
                fid.write((('%s, %s, %s, %s \n' %
                            ('right 100:', re100, rm100, rl100)).encode()))
                fid.write((('%s, %s, %s, %s \n' %
                            ('right 400:', re400, rm400, rl400)).encode()))
        else:
            if rl400 >= ll400 and rl100>=ll100:
                learner = 'rh_learner'
            elif rl400 <= ll400 and rl100 <= ll100:
                learner = 'lh_learner'
            else:
                learner = 'mixed'
            waves_save = op.join(save_path, '%s_%s_%s_waveforms.png' % (subject, block, area))
            plotD = plot_waveforms(subject, lh_s01, lh_s02, rh_s01, rh_s02, block, waves_save)
            plt.close()
            with open(op.join(save_dir, 'global_all_ams.txt'), 'ab') as fid:
                print('Adding a line to the global all ams file.')
                fid.write((('%s, %s, %s, %s, %s, %s, %s \n' %
                            (subject, learner, block, ll100, ll400, rl100, rl400)).encode()))
            with open(op.join(save_dir, subject, '%s_%s_ams.txt' % (subject, block)), 'ab') as fid:
                print('writing ams data to a csv at %s' % op.join(subject, '%s_%s_ams.txt' % (subject, block)))
                fid.write(('%s: S01 - S02 areal mean signal \n' % block).encode())
                fid.write((('%s, %s, %s, %s \n' %
                            ('left 100:', le100, lm100, ll100)).encode()))
                fid.write((('%s, %s, %s, %s \n' %
                            ('left 400:', le400, lm400, ll400)).encode()))
                fid.write((('%s, %s, %s, %s \n' %
                            ('right 100:', re100, rm100, rl100)).encode()))
                fid.write((('%s, %s, %s, %s \n' %
                            ('right 400:', re400, rm400, rl400)).encode()))


# lh_pairs = np.unique([x[0:6] for x in lh_picks])
# rh_pairs = np.unique([x[0:6] for x in rh_picks])

#    diffs_n = []
#    for i in range(140):
#        diffs_n.append([i, dC[i][n]])

