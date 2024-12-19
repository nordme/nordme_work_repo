
import os
import os.path as op
import mne
from utils import _short_label


anat_dir = '/media/erica/data1/anat_subjects'
atlas = 'HCPMMP1_combined'
out_dir = f'/media/erica/data1/anat_subjects/atlas/gmix/{atlas}'

if not op.isdir(out_dir):
    os.mkdir(out_dir)

fs_labels = [x for x in mne.read_labels_from_annot('fsaverage', atlas)
             if not '???' in x.name and not 'unknown' in x.name]
left_labels = [x for x in fs_labels if x.name.endswith('lh')]


brain = mne.viz.Brain('fsaverage', 'split', views=['med', 'lat', 'ven'],
              subjects_dir=anat_dir, background='white')


for li, label in enumerate(left_labels):
    lname = _short_label(label.name)
    rh_idx = li + 180 if atlas=='HCPMMP1' else li*2 + 1
    label2 = fs_labels[rh_idx]
    plot_path = op.join(out_dir, '%s.png' % lname)
    brain.add_label(label, borders=False, color='r')
    brain.add_label(label2, borders=False, color='r')
    brain.add_text(x=0.8, y=0.8, text=lname)
    brain.save_image(plot_path)
    print(f'label {li}: {label.name}')
    brain.remove_labels()
    brain.remove_text()