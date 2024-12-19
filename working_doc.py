import mne
import numpy as np
from numpy.testing import assert_allclose
from mne import Epochs, find_events, pick_types
from mne.io import read_raw_fif
from mne.label import BiHemiLabel, read_label
from mne.minimum_norm import (
    INVERSE_METHODS,
    apply_inverse_epochs,
    prepare_inverse_operator,
    read_inverse_operator,
)
from mne.minimum_norm.time_frequency import (
    compute_source_psd,
    compute_source_psd_epochs,
    source_band_induced_power,
    source_induced_power,
)

tmin, tmax, event_id = -0.2, 0.5, 1
anat_dir = '/media/erica/data1/anat_subjects'

fname_data = '/media/erica/data1/genz2/twa_hp/genz532_20b/sss_pca_fif/genz532_20b_faces_allclean_fil80_raw_sss.fif'
fname_inv = '/media/erica/data1/genz2/twa_hp/genz532_20b/inverse/genz532_20b-meg-erm-inv.fif'
labels = mne.read_labels_from_annot(subject='fsaverage', parc='aparc', subjects_dir=anat_dir)

# Setup for reading the raw data
raw = mne.io.read_raw_fif(fname_data)
events = find_events(raw, mask=1)
inv = read_inverse_operator(fname_inv)
inv = prepare_inverse_operator(inv, nave=1, lambda2=1.0 / 9.0, method="dSPM")

# picks MEG gradiometers
picks = pick_types(
    raw.info, meg=True, eeg=False, eog=True, stim=False, exclude="bads"
)

# Load condition 1
event_id = 1
events3 = events[:3]  # take 3 events to keep the computation time low
epochs = Epochs(
    raw,
    events3,
    event_id,
    tmin,
    tmax,
    picks=picks,
    baseline=(None, 0),
    reject=dict(grad=2000e-13, mag=6000e-15),
    preload=True,
)

freqs = np.arange(7, 30, 2)

tlen = len(epochs.times)
flen = len(freqs)

# prepare labels
label = labels[60]  # lh Aud
label2 = labels[61]  # rh Aud
bad_lab = label.copy()
bad_lab.vertices = np.hstack((label.vertices, [2121]))  # add 1 unique vert
bad_lbls = [label, bad_lab]
print("label verts:", label.vertices.shape)
vlen_lh = len(np.intersect1d(inv["src"][0]["vertno"], label.vertices))
vlen_rh = len(np.intersect1d(inv["src"][1]["vertno"], label2.vertices))


# prepare instances of BiHemiLabel

lvis = labels[42]
rvis = labels[43]
bihl = BiHemiLabel(lh=label, rh=label2)  # auditory labels
bihl.name = "Aud"
bihl2 = BiHemiLabel(lh=lvis, rh=rvis)  # visual labels
bihl2.name = "Vis"
bihls = [bihl, bihl2]
bad_bihl = BiHemiLabel(lh=bad_lab, rh=rvis)  # 1 unique vert on lh, rh ok
bad_bihls = [bihl, bad_bihl]
print("BiHemi label verts:", bihl.lh.vertices.shape, bihl.rh.vertices.shape)

label_sets = [[labels, bad_lbls], [bihls, bad_bihls]]

# check error handling
sip_kwargs = dict(
    baseline=(-0.1, 0),
    baseline_mode="percent",
    n_cycles=2,
    n_jobs=None,
#    return_plv=False,
    method="dSPM",
    prepared=True,
)

tlen = len(epochs.times)
flen = len(freqs)
vlen = 205

no_list_pow = source_induced_power(
    epochs, inv, freqs, label=label, **sip_kwargs
)
assert no_list_pow.shape == (vlen, flen, tlen)

list_pow = source_induced_power(
    epochs, inv, freqs, label=[label], **sip_kwargs
)
assert list_pow.shape == (1, flen, tlen)

nlp_ave = np.mean(no_list_pow, axis=0)
assert_allclose(nlp_ave, list_pow[0], rtol=1e-1)