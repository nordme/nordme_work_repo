# -*- coding: utf-8 -*-

import mne
import os
import os.path as op
import numpy as np

prek_dir = '/storage/prek/'
subjects = [x for x in os.listdir(prek_dir) if 'prek' in x and op.isdir(prek_dir + x)]
subjects.sort()
fmin=0
fmax=20
tmin=0
tmax=180

pcas = []

#
# for subject in subjects:
#    sub_path = op.join(prek_dir, '%s' % subject)
#    pca_path = op.join(sub_path, 'sss_pca_fif', '%s_erp_pre_allclean_fil80_raw_sss.fif' % subject)
#    pca = mne.io.read_raw_fif(pca_path)
#    crop = pca.copy().crop(tmin=tmin, tmax=tmax)
#    for_app = np.array(crop.get_data())
#    for_app = for_app.mean(axis=0)
#    pcas.append(for_app)

aves = []

for subject in subjects:
    sub_path = op.join(prek_dir, '%s' % subject)
    ave_path = op.join(sub_path, 'inverse', 'All_80-sss_eq_%s-ave.fif' % subject)
    ave = mne.read_evokeds(ave_path)
    aves.append(ave[0])

grand_ave = pcas.mean(axis=0)

sample_pca = mne.io.read_raw_fif('/storage/prek/prek_1103/sss_pca_fif/prek_1103_erp_pre_allclean_fil80_raw_sss.fif')
sample_pca.get_data() = grand_ave

ga_plot = sample_pca.plot_psd(fmin=fmin, fmax=fmax)

ga_plot.savefig(op.join(prek_dir, 'prek_pre_%s_%s_psd.png' % (int(round(fmin)), fmax)))
