# -*- coding: utf-8 -*-

import os
import mne
import os.path as op
import matplotlib.pyplot as plt

data_dir = '/data/genz'
subjects = ['erica_peterson']
peaks = dict(N100=[80, 120], P250=[230, 270], P550=[530, 570])
# conditions = ['s01', 's02', 's03']
conditions = ['s01', 's03']
lambda2 = 1/(3**2)
atlas = 'HCPMMP1'
target_labels = ['R_STSdp_ROI-rh', 'L_STSdp_ROI-lh']
decim=4

for subject in subjects:
    # load in relevant files
    sub_path = op.join(data_dir, subject)
    epochs_path = op.join(sub_path, 'epochs', 'All_80-sss_%s-epo.fif'
                          % subject)
    inv_path = op.join(sub_path, 'inverse', '%s-80-sss-meg-inv.fif' % subject)
    epochs = mne.read_epochs(epochs_path)
    inv = mne.minimum_norm.read_inverse_operator(inv_path)
    labels =[l for l in mne.read_labels_from_annot(subject=subject, parc=atlas)
            ]
    for condition in conditions:
        c_epochs = epochs['learn/%s' % condition].copy()
        # average faces / emojis / thumbs to get epochs x sensors x samples
        c_ave = c_epochs['faces']
        c_ave._data = (c_epochs['faces'].get_data()
                       + c_epochs['emojis'].get_data()
                       + c_epochs['thumbs'].get_data())/3
        stcs = mne.minimum_norm.apply_inverse_epochs(c_ave, inv, lambda2)
        for label in labels:
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
                plt.savefig('/data/genz/erica_peterson/images/%s_%s_%s_%s.png'
                            % (subject, condition, label.name, peak))
                plt.close()


