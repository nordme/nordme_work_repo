# -*- coding: utf-8 -*-

import os.path as op
import mne
import matplotlib.pyplot as plt
import numpy as np
import scipy

save_dir = '/home/nordme/data/genz/'
anat_dir = '/brainstudio/MEG/genz/anatomy/'
subject = 'genz219_11a'
fixed_subject = 'genz219_11a_fixed'
bad_path = op.join(anat_dir, subject, 'bem', '%s-oct-6-src.fif' % subject)
good_path = op.join(anat_dir, fixed_subject, 'bem', '%s-oct-6-src.fif' % fixed_subject)

bad_src = mne.read_source_spaces(bad_path)
good_src = mne.read_source_spaces(good_path)

bad_verts = np.concatenate((bad_src[0]['rr'][bad_src[0]['vertno']], bad_src[1]['rr'][bad_src[1]['vertno']]), axis=0)
good_verts = np.concatenate((good_src[0]['rr'][good_src[0]['vertno']], good_src[1]['rr'][good_src[1]['vertno']]), axis=0)


# bad to good using compute nearest
bad_to_good = mne.surface._compute_nearest(bad_verts, good_verts, return_dists=True)
bad_to_good_mm = 1000 * bad_to_good[1]
bad_to_good_mm.sort()

# bad to good using scipy.spatial.distance.cdist
bad_to_good1 = scipy.spatial.distance.cdist(bad_verts, good_verts)
bad_to_good_min1 = np.min(bad_to_good1, axis=-1)
bad_to_good_mm1 = bad_to_good_min1*1000
bad_to_good_mm1.sort()


bad_to_bad = scipy.spatial.distance.cdist(bad_verts, bad_verts)
np.fill_diagonal(bad_to_bad, np.inf)
bad_to_bad_min = np.min(bad_to_bad, axis=-1)
bad_to_bad_mm = bad_to_bad_min*1000
bad_to_bad_mm.sort()


good_to_good = scipy.spatial.distance.cdist(good_verts, good_verts)
np.fill_diagonal(good_to_good, np.inf)
good_to_good_min = np.min(good_to_good, axis=-1)
good_to_good_mm = good_to_good_min*1000
good_to_good_mm.sort()


# histograms

btg_plot = plt.hist(bad_to_good_mm, bins=np.arange(0, 8, 0.5))
plt.title('Bad vertices to good vertices: mne.surface._compute_nearest')
plt.savefig(op.join(save_dir, 'bad_to_good_hist.png'))
plt.close()

btg_plot1 = plt.hist(bad_to_good_mm1, bins=np.arange(0, 8, 0.5))
plt.title('Bad vertices to good vertices: scipy.spatial.distance.cdist')
plt.savefig(op.join(save_dir, 'bad_to_good_hist1.png'))
plt.close()


btb_plot = plt.hist(bad_to_bad_mm, bins=np.arange(0, 8, 0.5))
plt.title('Bad vertices to bad vertices: scipy.spatial.distance.cdist')
plt.savefig(op.join(save_dir, 'bad_to_bad_hist.png'))
plt.close()


gtg_plot = plt.hist(good_to_good_mm, bins=np.arange(0, 8, 0.5))
plt.title('Good vertices to good vertices: scipy.spatial.distance.cdist')
plt.savefig(op.join(save_dir, 'good_to_good_hist.png'))
plt.close()