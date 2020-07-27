
import mne
import os.path as op
# import mayavi.mlab as mm
import matplotlib.pyplot as plt

# set these variables

subjects = ['genz532_17a']
# subjects_dir = '/storage/anat/subjects/'
subjects_dir = '/home/nordme/data/genz/anat/'
n_jobs = 16

# variables

spacing = 5.0     # in millimeters
overwrite = True

for subject in subjects:
    base_path = op.join(subjects_dir, subject)

    # run setup_source_space
    src_dir = op.join(base_path, 'bem')
    bem_path = op.join(src_dir, '%s-5120-bem-sol.fif' % subject)
    brain_path = op.join(base_path, 'bem', 'watershed', '%s_brain_surface' % subject)
    brain_surf = mne.read_surface(brain_path, return_dict=True)[2]
    bem = mne.read_bem_solution(bem_path)
    vsurf_name = op.join(src_dir, '%s-%smm-vsurf-src.fif' % (subject, int(spacing)))

    print('Working on source space for subject %s.' % subject)

    v_surf = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=None,
                                             bem=bem, surface=None, pos=spacing)
    mne.write_source_spaces(vsurf_name, v_surf, overwrite=overwrite)
#    # source space plot
#    surf_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
#                                       surfaces='white', coord_frame='head', src=v_surf)
#    vsurf_save = op.join(src_dir, '%s_v_surf_plot.png' % subject)
#    mm.title('Volumetric Source Space Bounded By Brain (Pial) Surface')
#    mm.savefig(filename=vsurf_save, figure=surf_plot)
#    mm.close()
    # bem plot
    vsurf_plot2 = mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir,
                                       src=v_surf)
    vsurf2_save = op.join(src_dir, '%s_v_surf_plot_bem.png' % subject)
    plt.title('Volumetric Source Space Bounded By BEM Surface')
    plt.savefig(fname=vsurf2_save, figure=vsurf_plot2)
    plt.close()
