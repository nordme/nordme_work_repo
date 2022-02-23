# -*- coding: utf-8 -*-

import os
import mne
import os.path as op
import matplotlib.pyplot as plt
import numpy as np

data_dir = '/data/egenz'
subjects = ['erica_peterson']
# peaks = dict(N100=[80, 120], P250=[230, 270],  P550=[530, 570])
peaks = dict(N100=[80, 120], P250=[230, 270],  P400=[400, 500])
# conditions = ['s01', 's02', 's03']
# conditions = ['s01', 's02']
conditions = ['s02']
lambda2 = 1/(3**2)
atlas = 'HCPMMP1'
#target_labels = ['R_STSdp_ROI-rh', 'L_STSdp_ROI-lh']
decim=4
os.environ['SUBJECTS_DIR']='/data/anat_subjects'

target_labels=['R_TPOJ1_ROI-rh']

for subject in subjects:
    # load in relevant files
    sub_path = op.join(data_dir, subject)
    epochs_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-epo.fif'
                          % subject)
#    inv_path = op.join(sub_path, 'inverse', '%s-80-sss-meg-inv.fif' % subject)
    inv_path = op.join(sub_path, 'inverse', '%s_aud-80-sss-meg-inv.fif' % subject)
    epochs = mne.read_epochs(epochs_path)
    inv = mne.minimum_norm.read_inverse_operator(inv_path)
    labels =[l for l in mne.read_labels_from_annot(subject=subject, parc=atlas)
            ]
    for condition in conditions:
#        c_epochs = epochs['learn/%s' % condition].copy()
        c_epochs = epochs['%s' % condition].copy()
        # average faces / emojis / thumbs to get epochs x sensors x samples
        c_ave = c_epochs['faces/pos_block'][0:122] if condition == 's02' else \
            c_epochs['faces/pos_block']
#        c_ave._data = (c_epochs['faces/pos_block'].get_data()[0:122]
#        c_ave._data = (c_epochs['faces/pos_block'].get_data()
#                       + c_epochs['emojis/pos_block'].get_data())/2
        c_ave._data = (c_epochs['faces/pos_block'].get_data()[0:122]
                       + c_epochs['emojis/pos_block'].get_data()[0:122]
                       + c_epochs['faces/neg_block'].get_data()[0:122]
                       + c_epochs['emojis/neg_block'].get_data()[0:122])/4
#                       + c_epochs['thumbs'].get_data())/3
        stcs = mne.minimum_norm.apply_inverse_epochs(c_ave, inv, lambda2)
        ls = [l for l in labels if l.name in target_labels]
        for label in labels:
#        for label in ls:
            in_label_stcs = [s.in_label(label) for s in stcs]
            in_label_stcs = [s.data.mean(axis=0) for s in in_label_stcs]
            # in_label_stcs has shape n_epochs x n_samples
            for peak, [start, stop] in zip(peaks.keys(), peaks.values()):
                start = int(start/decim)
                stop = int(stop/decim)
                ptc = [p[start:stop].mean() for p in in_label_stcs]
                assert len(ptc) == len(c_ave.get_data())
                fig = plt.figure()
                plot = plt.plot(ptc)
                x = np.arange(len(ptc))
                m, b = np.polyfit(x, ptc, 1)
                print(m)
                plt.plot(x, m * x + b, 'k--' )
                fig.text(0.7, 0.8, 'slope = %.04f' % m)
                plt.savefig('/data/egenz/erica_peterson/images/%s/%s_%s_%s_%s.png'
                            % (condition, subject, condition, label.name, peak))
                print(f'Fig for label {label.name}')
                plt.close()







