from pathlib import Path
import mne
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mne.viz import plot_evoked_topo


ga_c = mne.read_evokeds('/data/genz/fixedhp/correct_aud_15-17_44-ave.fif')
ga_i = mne.read_evokeds('/data/genz/fixedhp/incorrect_aud_15-17_44-ave.fif')

cdiff_data = ga_c[0].data - ((ga_c[1].data + ga_c[2].data) / 2)
idiff_data = ga_i[0].data - ((ga_i[1].data + ga_i[2].data) / 2)

cdiff = ga_c[0].copy()
idiff = ga_i[0].copy()
cdiff.data = cdiff_data
idiff.data = idiff_data

c_ic = [cdiff, idiff]

topo = plot_evoked_topo(c_ic)

t_save = Path('/data/genz/fixedhp/c_ic_topo_plot.png')
topo.savefig(t_save)
topo.close()
print(f'saved picture to {t_save}')

