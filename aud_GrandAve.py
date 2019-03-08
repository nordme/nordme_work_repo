#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 11:03:42 2018

@author: mdclarke

script to create auditory grand averages for genZ data. 

"""
# 124 no faces learn 

import mne
from os import path as op

age = '17a' ## CHANGE TO APPROPRIATE AGE GROUP [9a, 11a, 13a, 15a, or 17a]

# data_path = '/mnt/brainstudio/genz/genz_proc/active/'
data_path = '/brainstudio/MEG/genz/genz_proc/active/'
avg_path = op.join(data_path, 'group_averages')
analysis = 'Split'
lpf = 80

nine = ['genz105_9a', 'genz106_9a', 'genz108_9a', 'genz111_9a',
        'genz110_9a', 'genz112_9a', 'genz113_9a', 'genz114_9a', 'genz115_9a',
        'genz116_9a', 'genz118_9a', 'genz119_9a',
        'genz120_9a', 'genz121_9a', 'genz122_9a', 'genz123_9a',
        'genz124_9a', 'genz125_9a', 'genz126_9a', 'genz128_9a',
        'genz130_9a', 'genz131_9a', 'genz133_9a']

eleven = [ 'genz205_11a', 'genz206_11a', 'genz207_11a',
           'genz208_11a', 'genz209_11a', 'genz210_11a', 'genz212_11a',
           'genz216_11a', 'genz218_11a', 'genz219_11a', 'genz223_11a',
           'genz224_11a', 'genz225_11a', 'genz226_11a', 'genz227_11a',
           'genz228_11a', 'genz229_11a', 'genz230_11a', 'genz231_11a',
           'genz232_11a', 'genz233_11a', 'genz235_11a']

thirteen = ['genz309_13a', 'genz311_13a', 'genz313_13a', 'genz314_13a',
            'genz318_13a', 'genz319_13a', 'genz320_13a', 'genz322_13a',
            'genz323_13a', 'genz324_13a', 'genz325_13a', 'genz326_13a', 'genz327_13a', 'genz328_13a', 'genz329_13a',
            'genz330_13a', 'genz331_13a', 'genz332_13a', 'genz333_13a', 'genz334_13a',
            'genz335_13a', 'genz337_13a']

fifteen = ['genz401_15a', 'genz403_15a', 'genz406_15a',
           'genz409_15a', 'genz411_15a', 'genz412_15a', 'genz413_15a',
           'genz414_15a', 'genz415_15a', 'genz417_15a',
           'genz418_15a', 'genz419_15a', 'genz420_15a', 'genz421_15a',
           'genz422_15a', 'genz423_15a', 'genz424_15a', 'genz425_15a',
           'genz426_15a', 'genz427_15a', 'genz428_15a', 'genz429_15a',
           'genz430_15a', 'genz431_15a', 'genz432_15a']

seventeen = ['genz507_17a', 'genz512_17a', 'genz513_17a',
             'genz514_17a', 'genz515_17a', 'genz516_17a', 'genz517_17a',
             'genz518_17a', 'genz519_17a', 'genz520_17a', 'genz521_17a',
             'genz522_17a', 'genz523_17a', 'genz526_17a', 'genz527_17a',
             'genz528_17a', 'genz529_17a', 'genz530_17a', 'genz531_17a', 'genz532_17a']


if age == '9a':
    subjs = nine
if age == '11a':
    subjs = eleven
if age == '13a':
    subjs = thirteen
if age == '15a':
    subjs = fifteen
if age == '17a':
    subjs = seventeen
      
conditions = ['aud/faces/learn/s01',
              'aud/faces/learn/s02',
              'aud/faces/learn/s03',
              'aud/thumbs/learn/s01',
              'aud/thumbs/learn/s02',
              'aud/thumbs/learn/s03',
              'aud/emojis/learn/s01',
              'aud/emojis/learn/s02',
              'aud/emojis/learn/s03',              
              'aud/faces/test/s01',
              'aud/faces/test/s02',
              'aud/faces/test/s03',
              'aud/faces/test/s04',
              'aud/faces/test/s05',
              'aud/faces/test/s06',
              'aud/faces/test/s07',
              'aud/faces/test/s08',
              'aud/faces/test/s09',
              'aud/faces/test/s10',
              'aud/faces/test/s11',
              'aud/faces/test/s12',              
              'aud/thumbs/test/s01',
              'aud/thumbs/test/s02',
              'aud/thumbs/test/s03',
              'aud/thumbs/test/s04',
              'aud/thumbs/test/s05',
              'aud/thumbs/test/s06',
              'aud/thumbs/test/s07',
              'aud/thumbs/test/s08',
              'aud/thumbs/test/s09',
              'aud/thumbs/test/s10',
              'aud/thumbs/test/s11',
              'aud/thumbs/test/s12',
              'aud/emojis/test/s01',
              'aud/emojis/test/s02',
              'aud/emojis/test/s03',
              'aud/emojis/test/s04',
              'aud/emojis/test/s05',
              'aud/emojis/test/s06',
              'aud/emojis/test/s07',
              'aud/emojis/test/s08',
              'aud/emojis/test/s09',
              'aud/emojis/test/s10',
              'aud/emojis/test/s11',
              'aud/emojis/test/s12']
names = ['aud_faces_learn_s01',
         'aud_faces_learn_s02',
         'aud_faces_learn_s03',
         'aud_thumbs_learn_s01',
         'aud_thumbs_learn_s02',
         'aud_thumbs_learn_s03',
         'aud_emojis_learn_s01',
         'aud_emojis_learn_s02',
         'aud_emojis_learn_s03',  
         'aud_faces_test_s01',
         'aud_faces_test_s02',
         'aud_faces_test_s03',
         'aud_faces_test_s04',
         'aud_faces_test_s05',
         'aud_faces_test_s06',
         'aud_faces_test_s07',
         'aud_faces_test_s08',
         'aud_faces_test_s09',
         'aud_faces_test_s10',
         'aud_faces_test_s11',
         'aud_faces_test_s12',              
         'aud_thumbs_test_s01',
         'aud_thumbs_test_s02',
         'aud_thumbs_test_s03',
         'aud_thumbs_test_s04',
         'aud_thumbs_test_s05',
         'aud_thumbs_test_s06',
         'aud_thumbs_test_s07',
         'aud_thumbs_test_s08',
         'aud_thumbs_test_s09',
         'aud_thumbs_test_s10',
         'aud_thumbs_test_s11',
         'aud_thumbs_test_s12',
         'aud_emojis_test_s01',
         'aud_emojis_test_s02',
         'aud_emojis_test_s03',
         'aud_emojis_test_s04',
         'aud_emojis_test_s05',
         'aud_emojis_test_s06',
         'aud_emojis_test_s07',
         'aud_emojis_test_s08',
         'aud_emojis_test_s09',
         'aud_emojis_test_s10',
         'aud_emojis_test_s11',
         'aud_emojis_test_s12']

by_all = True

by_gender = True

gaves = []

f_gaves = []

m_gaves = []

if by_gender:
    for j, (cond, name) in enumerate(zip(conditions, names)):
        m_evokeds = []
        f_evokeds = []
        for subj in subjs:
            if int(subj[4:7]) % 2 == 0:  # if the subject number is even, the subject is a girl
                gender = 'f'
            else:
                gender = 'm'
            evoked_file = op.join(data_path, '%s' % subj, 'inverse',
                                  '%s_%d-sss_eq_%s-ave.fif'
                                  % (analysis, lpf, subj))
            evoked = mne.read_evokeds(evoked_file, condition=cond,
                                      baseline=(None, 0))
            assert evoked.comment == cond
            if gender == 'f':
                f_evokeds.append(evoked)
            else:
                m_evokeds.append(evoked)
        print('f_evokeds: %s' % len(f_evokeds))
        print('m_evokeds: %s' % len(m_evokeds))
        f_gaves.append(mne.grand_average(f_evokeds))
        f_gaves[j].comment = 'f_%s' % cond
        m_gaves.append(mne.grand_average(m_evokeds))
        m_gaves[j].comment = 'm_%s' % cond
    mne.write_evokeds(op.join(avg_path, 'f' + 'AUD_%s_%s_N%d-ave.fif'
                              % (age, analysis, len(f_evokeds))), f_gaves)
    mne.write_evokeds(op.join(avg_path, 'm' + 'AUD_%s_%s_N%d-ave.fif'
                              % (age, analysis, len(m_evokeds))), m_gaves)


if by_all:
    for j, (cond, name) in enumerate(zip(conditions, names)):
        evokeds = []
        for subj in subjs:
            evoked_file = op.join(data_path, '%s' %subj, 'inverse',
                                  '%s_%d-sss_eq_%s-ave.fif'
                                  % (analysis, lpf, subj))
            evoked = mne.read_evokeds(evoked_file, condition=cond,
                                      baseline=(None,0))
            assert evoked.comment == cond
            evokeds.append(evoked)
        gaves.append(mne.grand_average(evokeds))
        gaves[j].comment = cond
        mne.write_evokeds(op.join(avg_path, 'AUD_%s_%s_N%d-ave.fif'
                                  % (age, analysis, len(subjs))), gaves)

