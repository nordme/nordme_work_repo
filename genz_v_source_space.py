
import mne
import os
import os.path as op
import mayavi.mlab as mm
import matplotlib.pyplot as plt

# set these variables


subjects_dir = '/storage/anat/subjects/'
subjects = [x for x in os.listdir(subjects_dir) if op.isdir('%s%s' % (subjects_dir, x)) and 'genz' in x]
subjects.sort()
# subjects_dir = '/home/nordme/data/genz/anat/'
n_jobs = 16

# variables

spacing = 5.0     # in millimeters
overwrite = True

for subject in subjects:
    base_path = op.join(subjects_dir, subject)

    # run setup_source_space
    src_dir = op.join(base_path, 'bem')
    bem_path = op.join(src_dir, '%s-5120-bem-sol.fif' % subject)
#    brain_path = op.join(base_path, 'bem', 'watershed', '%s_brain_surface' % subject)
#    brain_surf = mne.read_surface(brain_path, return_dict=True)[2]
    aseg_path = op.join(base_path, 'mri', 'aseg.mgz')
    bem = mne.read_bem_solution(bem_path)
    vsurf_name = op.join(src_dir, '%s-%smm-v_aseg-src.h5' % (subject, int(spacing)))
    volume_labels = mne.get_volume_labels_from_aseg(aseg_path)
    assert volume_labels[0] == 'Unknown'
    volume_labels.pop(0)

    print('Working on source space for subject %s.' % subject)

    v_surf = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir,
                                             bem=bem, pos=spacing, mri='aseg.mgz', volume_label=volume_labels,
                                           add_interpolator=True )
    mne.externals.h5io.write_hdf5(vsurf_name, v_surf, overwrite=overwrite)
#    mne.write_source_spaces(vsurf_name, v_surf, overwrite=overwrite)
    # source space plot
    surf_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                       surfaces='white', coord_frame='head', src=v_surf)
    vsurf_save = op.join(src_dir, '%s_v_aseg_plot.png' % subject)
    mm.title('Volumetric Source Space Bounded By BEM Surface')
    mm.savefig(filename=vsurf_save, figure=surf_plot)
    mm.close()
    # bem plot
#    vsurf_plot2 = mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir,
#                                       src=vsurf_name)
#    vsurf2_save = op.join(src_dir, '%s_v_aseg_plot_bem.png' % subject)
#    plt.title('Volumetric Source Space Bounded By BEM Surface')
#    plt.savefig(fname=vsurf2_save, figure=vsurf_plot2)
#    plt.close()
