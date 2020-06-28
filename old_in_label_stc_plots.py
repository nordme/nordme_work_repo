#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 13:59:41 2020

@author: erica
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 11:44:16 2020

@author: nordme
"""

import mne
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import os.path as op
import numpy as np
from surfer import Brain

# set these variables

# target_names = list of str: names of labels to select from atlas
target_names = ['Anterior Cingulate and Medial Prefrontal Cortex-lh',
                'Anterior Cingulate and Medial Prefrontal Cortex-rh',
                'Auditory Association Cortex-lh',
                'Auditory Association Cortex-rh',
                'DorsoLateral Prefrontal Cortex-lh',
                'DorsoLateral Prefrontal Cortex-rh',
                'Early Auditory Cortex-lh',
                'Early Auditory Cortex-rh',
                'Inferior Frontal Cortex-lh',
                'Inferior Frontal Cortex-rh',
                'Insular and Frontal Opercular Cortex-lh',
                'Insular and Frontal Opercular Cortex-rh',
                'Orbital and Polar Frontal Cortex-lh',
                'Orbital and Polar Frontal Cortex-rh',
                'Medial Temporal Cortex-lh',
                'Medial Temporal Cortex-rh',
                'Temporo-Parieto-Occipital Junction-lh',
                'Temporo-Parieto-Occipital Junction-rh',
                'Lateral Temporal Cortex-lh',
                'Lateral Temporal Cortex-rh',
                'Inferior Parietal Cortex-lh',
                'Inferior Parietal Cortex-rh'
                ]

label_type = 'HCPMMP1_combined'       # str: options are 'HCPMMP1_combined', 'HCPMMP1', 'aparc.a2009s', 'aparc'
timepoints = {'50': [30, 70], '100': [80, 120], '400': [380, 420]}
stc_type = 'dSPM'           # str: indicates method for stcs, e.g. 'dSPM' or 'eLORETA'
aud_or_vis = 'auditory'     # str: 'auditory' or 'visual'

# paths
base_dir = '/storage/genz_active/t1/twa_hp/'
save_dir = op.join(base_dir, 'labels', 'anat_labels')
src_path = '/storage/anat/subjects/fsaverage/bem/fsaverage-ico-5-src.fif'
stc_names = ['al01',
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
             ]

subjects = [x for x in os.listdir(base_dir) if 'genz' in x and op.isdir(op.join(base_dir, x))]
subjects.sort()

# get the constraining anatomical labels read in
all_labels = mne.read_labels_from_annot(subject='fsaverage', parc=label_type)
target_labels = [x for x in all_labels if np.in1d(x.name, target_names)]

# read in source space
src = mne.read_source_spaces(src_path)

# begin
for subject in subjects:
    stcs_path = op.join(base_dir, subject, '%s_stc' % stc_type, '%s' % aud_or_vis)
    for name in stc_names:
        stcs = [x for x in os.listdir(stcs_path) if name in x and 'morphed' in x]
        for s in stcs:
            code, _, _, _ = s.split('_')
            csv_name = 'genz_anat_label_activation_values_%s' % (code)
#            csv_save_path = op.join(save_dir, csv_name)
            csv_save_path = op.join(save_dir, csv_name)

            # read in the stc
            s_path = op.join(stcs_path, '%s' % s)
            stc = mne.read_source_estimate(s_path)
            stc.data = np.abs(stc.data)
            print('Working on stc %s for subject %s.' % (s, subject))

            # constrain by the anatomical labels
            for label in target_labels:
                label_name = label.name.replace(' ', '_')
                hemi = label_name.split('-')[-1]
                stc_inl = stc.in_label(label)
                
                # plot in-label activation
                print('Working on plots.')
                ln = label.name
                xvals = stc_inl.times
                yvals = stc_inl.data
                plt.figure()
                plot = plt.plot(xvals, yvals)
                plt.title('Activation in label %s.' % (ln))
                plt.savefig(op.join(save_dir, '%s_activation.eps' % ln))
                plt.close()
                
                # create the timepoint averages (collapse time dimension)
                for timepoint, [t_start, t_stop] in zip(timepoints.keys(), timepoints.values()):
                    time = int((t_stop+t_start)/2)
                    print('Timepoint: %d ms' % time)
                    stc_ave = stc_inl.copy().crop(t_start/1000, t_stop/1000)
                    stc_ave = stc_ave.mean()
                    stc_inl_mean = stc_ave.mean()

                    # output results
                    with open(csv_save_path, 'ab') as fid:
                        fid.write(('%s, %s, %s, %s, %s, %s\n' %
                                   (subject, hemi, label_name, s, time, stc_inl_mean)).encode())
