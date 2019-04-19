#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os.path as op
import mne
import numpy as np

from itertools import product

### SOURCE SPACE GRAND AVERAGES SCRIPT
# set important variables


# raw_dir = '/home/nordme/data/genz/genz_active/'
raw_dir = '/home/nordme/data/genz/genz_active/eLORETA/'
# save_dir = '/home/nordme/data/genz/genz_active/stc_aves/'
save_dir = '/home/nordme/data/genz/genz_active/eLORETA/stc_aves/'
# raw_dir = '/brainstudio/MEG/genz/genz_proc/active/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'


subjects = ['genz111_9a',
            'genz115_9a',
            'genz130_9a',
            'genz131_9a',
            'genz225_11a',
            'genz232_11a',
            'genz334_13a',
            #'genz335_13a',
            'genz429_15a',
            'genz430_15a',
            'genz529_17a',
            'genz530_17a',
            ]

codes = ['al01',
         'al02',
         'al03',
         'fl01',
         'fl02',
         'fl03',
         'el01',
         'el02',
         'el03',
         'tl01',
         'tl02',
         'tl03',
         'ft01',
         'ft02',
         'ft03',
         'et01',
         'et02',
         'et03',
         'tt01',
         'tt02',
         'tt03',
         'ft04',
         'ft05',
         'ft06',
         'et04',
         'et05',
         'et06',
         'tt04',
         'tt05',
         'tt06',
         'ft07',
         'ft08',
         'ft09',
         'et07',
         'et08',
         'et09',
         'tt07',
         'tt08',
         'tt09',
         'ft10',
         'ft11',
         'ft12',
         'et10',
         'et11',
         'et12',
         'tt10',
         'tt11',
         'tt12',
         'at01',
         'at02',
         'at03',
         'at04',
         'at05',
         'at06',
         'at07',
         'at08',
         'at09',
         'at10',
         'at11',
         'at12']

ages = ['all', '9', '11', '13', '15', '17']

feml = [[], [], [], [], [], []]

male = [[], [], [], [], [], []]

both = [[], [], [], [], [], []]

genders = [both, male, feml]

gender_names = ['both', 'male', 'female']

master_list = []

# create subject pools (gender x age) since each grand average will need to draw on a different set of subjects
# index 0 corresponds to subjects of all ages
for i, age in enumerate(ages):
    feml[i] = [sub for sub in subjects if '%sa' % age in sub and int(sub[4:7]) % 2 == 0]
    male[i] = [sub for sub in subjects if '%sa' % age in sub and int(sub[4:7]) % 2 != 0]
    both[i] = [sub for sub in subjects if '%sa' % age in sub]
    feml[0] = [sub for sub in subjects if int(sub[4:7]) % 2 == 0]
    male[0] = [sub for sub in subjects if int(sub[4:7]) % 2 != 0]
    both[0] = [sub for sub in subjects]
    print('Finished creating age pool %s for stc averaging.' % age)

# make a master list of subject pools to average over
# with handy entries that include the list of relevant subjects as well as the gender and age
for gender, gender_name in zip(genders, gender_names):
    for i in np.arange(6):
        master_list.append([gender_name, '%d' % (i*2+7), gender[i]])
        print('Added %s %d to master list of subject pools.' % (gender_name, i))

# create visual grand averages

print('Beginning work on visual stcs.')

epoch = ['FRN', 'SPN']

blocks = ['faces', 'emojis', 'thumbs', 'allblocks']

feedback = ['correct', 'incorrect', 'bothfdbk']

vis_conds = [[e, b, f] for e in epoch for b in blocks for f in feedback]

vcodes = ['%s_%s_%s' % (e, b, f) for e in epoch for b in blocks for f in feedback]

for list in master_list:
    gname, age, subjects = list
    print('Working on visuals for group %s %s.' % (gname, age))
    for vcode in vcodes:
        ave_path = op.join(save_dir, '%s_%s_%s' % (gname, age, vcode))
        stc_ave = 0
        for subject in subjects:
            stc_path = op.join(raw_dir, subject, 'stc', 'visual', '%s_%s_morphed' % (vcode, subject))
            stc = mne.read_source_estimate(stc_path)
            stc_ave += stc
        try:
            stc_ave /= len(subjects)
            assert stc_ave.data.ndim == 2 and stc_ave.data.shape[0] == 20484
            stc_ave.save(ave_path)
            print('Saved stc ave %s.' % ave_path)
        except ZeroDivisionError:
            print('Hmm. Looks like we need subjects for group %s %s.' % (gname, age))


# create auditory grand averages
for list in master_list:
    gname, age, subjects = list
    print('Working on group %s %s.' % (gname, age))
    for code in codes:
        ave_path = op.join(save_dir, '%s_%s_%s' % (gname, age, code))
        stc_ave = 0
        for subject in subjects:
            stc_path = op.join(raw_dir, subject, 'stc', 'auditory', '%s_%s_morphed' % (code, subject))
            stc = mne.read_source_estimate(stc_path)
            stc_ave += stc
        try:
            stc_ave /= len(subjects)
            assert stc_ave.data.ndim == 2 and stc_ave.data.shape[0] == 20484
            stc_ave.save(ave_path)
            print('Saved stc ave %s.' % ave_path)
        except ZeroDivisionError:
            print('Hmm. Looks like we need subjects for group %s %s.' % (gname, age))
