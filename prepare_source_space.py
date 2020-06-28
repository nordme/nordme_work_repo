#!/opt/miniconda3/envs/mne_dev/bin/python mne_dev
# -*- coding: utf-8 -*-

import mne
import os.path as op
import numpy as np
import subprocess
import mayavi.mlab as mm

# set these variables

subjects = ['genz532_17a']
# subjects_dir = '/storage/anat/subjects/'
subjects_dir = '/home/nordme/data/genz/anat/'
n_jobs = 16

# BEM variables
do_bem = False
layers = 1     # how many layers of the BEM you wish to compute (3 for EEG, 1 for MEG)
preflood = 12
overwrite = True

# source space variables
# script is set up to produce one source space of each variety
# Turn off the ones you don't want generated, otherwise they'll all get made
sphere = np.array((0.0, -0.02, 0.0, 0.08))
radius = None  # for sphere-constrained volumetric models; None will skip that step
# radius = None
volumetric_bem = False   # for volumetric source space bounded by bem
volumetric_surf = False    # for volumetric source space bounded by surface
warp_surface = True    # for warping of template source space to generate BEM
anat_surface = False   # for individual MRI dervied GM/WM surface-only source space

spacing = 'oct6'

for subject in subjects:
    base_path = op.join(subjects_dir, subject)
    warp_subject = subject + '_warp'

    if do_bem:

        # compute BEM
        print('Working on BEM for subject %s.' % subject)

        bsurf_name = op.join(base_path, 'bem', '%s-5120-bem.fif' % subject)
        bem_name = op.join(base_path, 'bem', '%s-5120-bem-sol.fif' % subject)

        ws = subprocess.run(['mne', 'watershed_bem', '--subject', '%s' % subject,
                        '--preflood', '%s' % preflood, '--overwrite', '%s' % overwrite])

        print('Finished watershed algorithm. Starting to create the BEM model.')

        model = subprocess.run(['mne_setup_forward_model', '--homog', '--surf', '--ico',
                        '4', '--subject', '%s' % subject])

    # run setup_source_space
    src_dir = op.join(base_path, 'bem')
    bem_path = op.join(src_dir, '%s-5120-bem-sol.fif' % subject)
    brain_path = op.join(base_path, 'bem', 'watershed', '%s_brain_surface' % subject)
    brain_surf = mne.read_surface(brain_path, return_dict=True)[2]
    bem = mne.read_bem_solution(bem_path)
    vsphere_name = op.join(src_dir, '%s-%s-vsphere-src.fif' % (subject, str(radius)))
    vbem_name = op.join(src_dir, '%s-vbem-src.fif' % (subject))
    vsurf_name = op.join(src_dir, '%s-%s-vsurf-src.fif' % (subject, spacing))
    wsurf_name = op.join(src_dir, '%s-%s-wsurf-src.fif' % (subject, spacing))
    surf_name = op.join(src_dir, '%s-%s-src.fif' % (subject, spacing))

    print('Working on source space for subject %s.' % subject)

    if radius:
        v_sphere = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=sphere,
                                                 bem=None, surface=None)   # volumetric spherical source space
        mne.write_source_spaces(vsphere_name, v_sphere, overwrite=overwrite)
        sphere_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                             surfaces='white', coord_frame='head', src=v_sphere)
        sph_save = op.join(src_dir, '%s_v_sphere_plot.png' % subject)
        mm.title('Volumetric Source Space Bounded By Sphere')
        mm.savefig(filename=sph_save, figure=sphere_plot)
        mm.close()
    if volumetric_bem:
        v_bem = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=None,
                                                 bem=bem, surface=None)      # volumetric source space bounded by BEM
        mne.write_source_spaces(vbem_name, v_bem, overwrite=overwrite)
        bem_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                          surfaces='white', coord_frame='head', src=v_bem)
        mm.title('Volumetric Source Space Bounded By BEM (Inner Skull)')
        vbem_save = op.join(src_dir, '%s_v_bem_plot.png' % subject)
        mm.savefig(filename=vbem_save, figure=bem_plot)
        mm.close()
    if volumetric_surf:
        v_surf = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=None,
                                                 bem=None, surface=brain_surf)    # volumetric source space bounded by brain surf
        mne.write_source_spaces(vsurf_name, v_surf, overwrite=overwrite)
        surf_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                           surfaces='white', coord_frame='head', src=v_surf)
        vsurf_save = op.join(src_dir, '%s_v_surf_plot.png' % subject)
        mm.title('Volumetric Source Space Bounded By Brain (Pial) Surface')
        mm.savefig(filename=vsurf_save, figure=surf_plot)
        mm.close()
    if warp_surface:
        warp_surf = mne.setup_source_space(subject=warp_subject, subjects_dir=subjects_dir, n_jobs=n_jobs,
                                           spacing=spacing)       # subject is warped fsaverage, not indv
        mne.write_source_spaces(wsurf_name, warp_surf, overwrite=overwrite)
        ws_plot = mne.viz.plot_alignment(subject=warp_subject, subjects_dir=subjects_dir, surfaces='white',
                                        coord_frame='head', src=warp_surf)
        mm.title('Template-based Surface Source Space (GM/WM Boundary)')
        wsurf_save = op.join(src_dir, '%s_wsurf_plot.png' % subject)
        mm.savefig(filename=wsurf_save, figure=ws_plot)
        mm.close()
    if anat_surface:
        surf = mne.setup_source_space(subject=subject, subjects_dir=subjects_dir, n_jobs=n_jobs, spacing=spacing
                                      )   # WM/GM surface-only source space
        mne.write_source_spaces(surf_name, surf, overwrite=overwrite)
        s_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir, surfaces='white',
                               coord_frame='head', src=surf)
        mm.title('MRI-based Surface Source Space (GM/WM Boundary)')
        surf_save = op.join(src_dir, '%s_surf_plot.png' % subject)
        mm.savefig(filename=surf_save, figure=s_plot)
        mm.close()
    else:
        print('No source space model selected. Finished with subject %s.' % subject)




