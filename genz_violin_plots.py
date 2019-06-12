#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import os.path as op
import mne
import numpy as np
import matplotlib.pyplot as plt

# change these variable based on what you want

stcs = ['both_17_SPN_faces_correct', 'both_17_SPN_emojis_correct', 'both_17_SPN_thumbs_correct']
# stcs.sort()

title = '17 yr olds block comparison of SPN (correct)'

ticks = [1,2,3]

labels = ['faces', 'emojis', 'thumbs']

vis_or_aud = 'visual' # 'visual' or 'auditory'

prefix = 'SPN_allblocks_correct' # code to indicate condition

gender = 'both'

age = '17'

signed = False

dSPM = True

# other things

save_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/plots/'

if signed:
    tag = '/signed/'
else:
   tag = '/'

if dSPM:
    aves_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/dSPM_ave/%s%s' % (vis_or_aud, tag)
    method = 'dSPM'
else:
    aves_dir = '/brainstudio/MEG/genz/genz_proc/active/twa_hp/eLORETA_ave/%s%s' % (vis_or_aud, tag)
    method = 'eLORETA'

# stcs = [s[0:-7] for s in os.listdir(aves_dir) if '-lh' in s and 'both' in s]



# read in the stc and plot it

plot = []

for s in stcs:
    stc_path = op.join(aves_dir, s)
    stc = mne.read_source_estimate(stc_path)
    print('Reading in data for stc %s' % s)
    data = stc.data
    flat = data.flatten()
    plot.append(flat)

print('Working on the plot. Hang on a minute.')
fig = plt.violinplot(plot, showmedians=True)
plt.title(title)
plt.xticks(ticks=ticks, labels=labels)
save_name = op.join(save_dir, '%s_%s_%s_%s.png' % (prefix, gender, age, method))
plt.savefig(save_name)
print('Saved image %s' % save_name)


