import mne
from pathlib import Path

sdir = Path('/media/erica/data2/anat_subjects')
ddir = Path('/media/erica/data2/genz/t1/twa_hp/genz105_9a')
trans = mne.read_trans(ddir / 'trans/genz105_9a-trans.fif')
src = mne.read_source_spaces(sdir / 'genz105_9a/bem/genz105_9a-oct-6-src.fif')
raw = mne.io.read_raw_fif(ddir / f'sss_pca_fif/genz105_9a_faces_learn_01_allclean_fil80_raw_sss.fif')
info = raw.info
sub = 'genz105_9a'

def plot_align(subj):
    plot = mne.viz.plot_alignment(subject=subj, subjects_dir=sdir,
                                  coord_frame='head', src=src, trans=trans,
                                  info=info, surfaces=dict(head=0.4, pial=0.4),
                                  meg='sensors')
    return plot

p = plot_align(sub)
