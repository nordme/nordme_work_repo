# -*- coding: utf-8 -*-

import mne
import numpy as np
import os
import os.path as op
import matplotlib.pyplot as plt

parent_dir = '/home/nordme/data/genz/genz_active/'

skip = ['genz115_9a', 'genz526_17a']
subjects = [x for x in os.listdir(parent_dir) if 'genz' in x and op.isdir(parent_dir + x) and not np.in1d(x, skip)]
subjects.sort()

blocks = ['faces', 'emojis', 'thumbs']

age = 'all'
gender = 'all'

# picks = ['MEG1613', 'MEG1623', 'MEG1633', 'MEG1643', 'MEG0233', 'MEG0243']
# picks = ['MEG1612', 'MEG1622', 'MEG1632', 'MEG1642', 'MEG0232', 'MEG0242', 'MEG1613', 'MEG1623', 'MEG1633', 'MEG1643', 'MEG0233', 'MEG0243']
picks = ['MEG1613']
n = 50  # the sample number. Choose 50 to get N=100 and choose 125 to get N=400

group_data = []
reg_data = []
reg_times = []
times = []

def collapse_data(epochs, blocks):
    # first we create an array with the faces, emojis, and thumbs data
    array = np.array([epochs['%s' % blocks[0]].get_data(), epochs['%s' % blocks[1]].get_data(), epochs['%s' % blocks[2]].get_data()])
    # then we average together the faces, emojis and thumbs data
    mean0 = np.mean(array, axis=0)
    # then we average the sensors into one channel
    mean1 = np.mean(mean0, axis=1)

    return mean1 # array of combined sensor data by epoch with blocks mashed together

def mgtd_data(epochs, blocks):
    # first we create an array with averaged faces, emojis, and thumbs data
    mgtd_array = np.array([abs(epochs['%s' % blocks[0]].get_data()), abs(epochs['%s' % blocks[1]].get_data()), abs(epochs['%s' % blocks[2]].get_data())])
    # then we average together the faces, emojis and thumbs data
    mgtd_mean0 = np.mean(mgtd_array, axis=0)
    # then we average the sensors into one channel
    mgtd_mean1 = np.mean(mgtd_mean0, axis=1)
    return mgtd_mean1

for subject in subjects:
    epo_path = op.join(parent_dir, subject, 'epochs', 'All_80-sss_%s-epo.fif' % subject)
    epo = mne.read_epochs(epo_path)
    epo = epo.pick_channels(picks)
    es01 = epo['learn/s01']
    es03 = epo['learn/s03']

    # average data to get good waveforms

    s01 = collapse_data(es01, blocks)
    s03 = collapse_data(es03, blocks)

    # calculate the differences between conditions
    dC = s01 - s03

    # put together array of condition difference values
    diffs_n = []
    for i in range(140):
        diffs_n.append([i, dC[i][n]]) # returns an array of S01 to S03 differences just at N=100 or N=400

    # plot the difference values at the given sample; x-axis is epoch number
    diffs_n = np.array(diffs_n)
    plt.plot(diffs_n[:, 1])
    plt.title('%s' % subject)
    plt.ylim(-2.55e-11, 2.5e-11)
    plt.ylabel('N100 amplitude difference between S01 and S03')
    plt.xlabel('Epoch number')

    # add a regression curve to the plot
    x = diffs_n[:, 0]
    y = diffs_n[:, 1]
    regression_coeffs = np.polyfit(x, y, deg=5)
    curve = np.poly1d(regression_coeffs)
    plt.plot(x, curve(x), color='k', lw=8)

    save_name = op.join(parent_dir, subject, '%s_%s_S01_S03_1613_reg.png' % (subject, n))
    plt.savefig(save_name)
    plt.close()

    # save the subject data to the group data

    peak_epoch = np.argmax(diffs_n[:, 1])
    peak = diffs_n[peak_epoch][1]
    group_data.append([subject, peak_epoch, peak])
    times.append(peak_epoch)

    reg_epoch = np.argmax(curve(x))
    reg_peak = curve(reg_epoch)
    reg_data.append([subject, reg_epoch, reg_peak])
    reg_times.append(reg_epoch)


    # create a bar chart of the early, mid, and late epoch mean differences at the given sample
    early1 = s01[0:46]
    mid1 = s01[46:92]
    late1 = s01[92:138]

    early3 = s03[0:46]
    mid3 = s03[46:92]
    late3 = s03[92:138]

    d_early = early1 - early3
    evk_early = np.mean(d_early, axis=0)
    d_mid = mid1 - mid3
    evk_mid = np.mean(d_mid, axis=0)
    d_late = late1 - late3
    evk_late = np.mean(d_late, axis=0)

    early = evk_early[n]
    mid = evk_mid[n]
    late = evk_late[n]

    plt.figure()
    plt.bar(x=np.arange(3), height=[early, mid, late])
    plt.ylim(-0.5e-11, 0.5e-11)
    save2 = op.join(parent_dir, subject, '%s_%s_S01_S03_1613_bar.png' % (subject, n))
    plt.savefig(save2)
    plt.close()

    # magnitude data bar chart
    ms01 = mgtd_data(es01, blocks)
    ms03 = mgtd_data(es03, blocks)

    mearly1 = ms01[0:46]
    mmid1 = ms01[46:92]
    mlate1 = ms01[92:138]

    mearly3 = ms03[0:46]
    mmid3 = ms03[46:92]
    mlate3 = ms03[92:138]

    md_early = mearly1 - mearly3
    mevk_early = np.mean(md_early, axis=0)
    md_mid = mmid1 - mmid3
    mevk_mid = np.mean(md_mid, axis=0)
    md_late = mlate1 - mlate3
    mevk_late = np.mean(md_late, axis=0)

    mearly = mevk_early[n]
    mmid = mevk_mid[n]
    mlate = mevk_late[n]

    plt.figure()
    plt.bar(x=np.arange(3), height=[mearly, mmid, mlate])
    plt.ylim(-4e-12, 4e-12)
    save3 = op.join(parent_dir, subject, '%s_%s_S01_S03_1613_bar_mgtd.png' % (subject, n))
    plt.savefig(save3)
    plt.close()


# calculate group statistics

high_learners = []
mid_learners = []
low_learners = []

print(group_data)
times.sort()
print('Times:', times)
# group_max = np.amax(times, axis=0)
# group_min = np.amin(times, axis=0)
# group_range = group_max - group_min
q1, q2, q3 = np.percentile(times, q=[25, 50, 75], axis=0)
iqr = q3-q1
group_upperf = q3 + 1.5*iqr
group_lowerf = q1 - 1.5*iqr

for data in group_data:
    if data[1] >= q3:
        low_learners.append(data)
    if data[1] <= q1:
        high_learners.append(data)
    else:
        mid_learners.append(data)

# regression based learning calculations
reg_high = []
reg_low = []
reg_mid = []

reg_times.sort()
rq1, rq2, rq3 = np.percentile(reg_times, q=[25, 50, 75], axis=0)

for rdata in reg_data:
    if rdata[1] >= rq3:                # rdata[1] being the peak epoch number for a given subject; here, a late peak
        reg_low.append(rdata)
    if rdata[1] <= rq1:                 # here, an early peak
        reg_high.append(rdata)
    else:
        reg_mid.append(rdata)


print('Upper fence: %s' % group_upperf)
print('Lower fence: %s' % group_lowerf)
print('Q3:', q3)
print('Q1:', q1)
print('Our high learners are: \n', high_learners)
print('Our low learners are: \n', low_learners)

print('RQ3:', rq3)
print('RQ1:', rq1)
print('Our regression-based high learners are: \n', reg_high)
print('Our regression-based low learners are: \n', reg_low)
