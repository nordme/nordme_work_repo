from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mne.viz import Brain
from mne import read_labels_from_annot

def plot_source_power(power, atlas, clim, s_name):
    bplot = Brain(subject=s_name)
    return bplot

subjects = ['erp_1', 'erp_2', 'erp_3']
d_dir = Path('/data/erica/rs')
bands = dict(theta=[4, 7], alpha=[8, 12], beta=[13, 30], gamma=[31, 55])
n_freqs = 52
n_lbls = 68
ba_scale = dict(theta=80, alpha=20, beta=14, gamma=8)
br_scale = dict(theta=0.05, alpha=0.01, beta=0.007, gamma=0.005)

labels = read_labels_from_annot(subject='erp_1', parc='aparc',
                                    subjects_dir='/data/anat_subjects/')
labels = [l for l in labels if not '???' in l.name
          and not l.name.startswith('unknown')]

# load in data
a_data = np.zeros((len(subjects), n_freqs, n_lbls))
r_data = np.zeros((len(subjects), n_freqs, n_lbls))

for si, sub in enumerate(subjects):
    s_path = d_dir / sub / f'{sub}_aparc_nobaseline_dSPM_rs_spower.csv'
    s_data = np.loadtxt(s_path, delimiter=',')
    assert s_data.shape == (58, n_lbls)
    # mean power in cortical label at each frequency
    r_means = s_data.mean(axis=1)
    # total spectral power in the average label
    total_power = r_means.sum()
    # absolute power data
    a_data[si] = s_data[3:55]
    # relative power data
    r_data[si] = s_data[3:55] / total_power

amax, amin = a_data.max(), a_data.min()
rmax, rmin = r_data.max(), r_data.min()

for bi, (band, [low, high]) in enumerate(bands.items()):
    i_dir = d_dir / 'plots'
    f_save = i_dir / f'erp_long_rs_power_plots_{band}.png'
    fig, axes = plt.subplots(nrows=4, ncols=len(subjects), figsize=(16, 16))
    for ci in range(3):
        b_abs = a_data[ci, low-4:high-4, :]
        assert b_abs.shape == (high-low, n_lbls)
        b_rel = r_data[ci, low - 4:high - 4, :]
        assert b_rel.shape == (high - low, n_lbls)
        b_abs, b_rel = b_abs.mean(axis=0), b_rel.mean(axis=0)
        assert b_abs.shape == b_rel.shape == (n_lbls,)
        # some basic stats

        # power brain plots
        a_brain = Brain(subject='erp_1', hemi='split', title=band, background='white', views=['med', 'lat'])
        for lidx, lab in enumerate(labels):
            # label absolute power as percentage of max label for timepoint
            a_val = b_abs[lidx] / b_abs.max()
            a_brain.add_label(lab, color='red', alpha=a_val)
        b_save = i_dir / 'abs' / f'erp_{ci+1}_label_{band}.png'
        a_brain.save_image(b_save)
        a_brain.close()

        # rel brain plots
        r_brain = Brain(subject='erp_1', hemi='split', title=band,
                        background='white', views=['med', 'lat'])
        for lidx, lab in enumerate(labels):
            # label relative power as percentage of max label for timepoint
            r_val = b_rel[lidx] / b_rel.max()
            r_brain.add_label(lab, color='red', alpha=r_val)
        r_save = i_dir / 'rel' / f'erp_{ci + 1}_label_{band}.png'
        r_brain.save_image(r_save)
        r_brain.close()
        # diff plots
        if ci > 0:
            diff = a_data[ci, low - 4:high - 4, :] - a_data[0, low - 4:high - 4, :]
            assert diff.shape == (high - low, n_lbls)
            diff = diff.mean(axis=0)
            d_brain = Brain(subject='erp_1', hemi='split', title=band,
                            background='white', views=['med', 'lat'])
            for lidx, lab in enumerate(labels):
                # label relative power as percentage of max label for timepoint
                d_val = diff[lidx] / ba_scale[band]
                col = 'red' if d_val > 0 else 'blue'
                d_brain.add_label(lab, color=col, alpha=min(1, abs(d_val)))
            d_save = i_dir / 'diff' / f'erp_abs_diff_t{ci + 1}-t1_label_{band}.png'
            d_brain.save_image(d_save)
            d_brain.close()
            # relative diff
            r_diff = r_data[ci, low - 4:high - 4, :] - r_data[0, low - 4:high - 4, :]
            assert r_diff.shape == (high - low, n_lbls)
            r_diff = r_diff.mean(axis=0)
            rd_brain = Brain(subject='erp_1', hemi='split', title=band,
                            background='white', views=['med', 'lat'])
            for lidx, lab in enumerate(labels):
                # label relative power as percentage of max label for timepoint
                rd_val = r_diff[lidx] / br_scale[band]
                col = 'red' if rd_val > 0 else 'blue'
                rd_brain.add_label(lab, color=col, alpha=min(1, abs(rd_val)))
            rd_save = i_dir / 'diff' / f'erp_rel_diff_t{ci + 1}-t1_label_{band}.png'
            rd_brain.save_image(rd_save)
            rd_brain.close()

