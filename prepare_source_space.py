#!/opt/miniconda3/envs/mne_dev/bin/python mne_dev
# -*- coding: utf-8 -*-

import mne
import os.path as op
import numpy as np
import subprocess
import mayavi.mlab as mm
import matplotlib.pyplot as plt

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
sphere = np.array((0.0, -0.02, 0.0, 0.08))    # volumetric source space bounded by sphere
volumetric_bem = True   # for volumetric source space bounded by bem
volumetric_surf = True    # for volumetric source space bounded by surface
warp_surface = False    # for surface source space using warped template surfaces
anat_surface = True   # for individual MRI derived GM/WM surface-only source space

spacing = 'oct6'

for subject in subjects:
    base_path = op.join(subjects_dir, subject)
    warp_subject = subject + '_warp'

    if do_bem:

        # compute BEM
        # ADD warped template BEM option here
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
    vsphere_name = op.join(src_dir, '%s-vsphere-src.fif' % subject)
    vbem_name = op.join(src_dir, '%s-vbem-src.fif' % subject)
    vsurf_name = op.join(src_dir, '%s-%s-vsurf-src.fif' % (subject, spacing))
    wsurf_name = op.join(src_dir, '%s-%s-wsurf-src.fif' % (subject, spacing))
    surf_name = op.join(src_dir, '%s-%s-src.fif' % (subject, spacing))

    print('Working on source space for subject %s.' % subject)

    if sphere is not None:       # volumetric spherical source space
        print('Beginning a spherical source space for subject %s.' % subject)
        v_sphere = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=sphere,
                                                 bem=None, surface=None)
        mne.write_source_spaces(vsphere_name, v_sphere, overwrite=overwrite)
        # source space plot
        print('Plotting spherical source space for subject %s.' % subject)
        sphere_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                             surfaces='white', coord_frame='head', src=v_sphere)
        sph_save = op.join(src_dir, '%s_v_sphere_plot.png' % subject)
        mm.title('Volumetric Source Space Bounded By Sphere')
        mm.savefig(filename=sph_save, figure=sphere_plot)
        mm.close()
        # bem plot
        print('Plotting spherical BEM for subject %s.' % subject)
        sphere_plot2 = mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir, src='%s' % vsphere_name)
        sph2_save = op.join(src_dir, '%s_v_sphere_plot_bem.png' % subject)
        plt.title('Volumetric Source Space Bounded By Sphere')
        plt.savefig(fname=sph2_save, figure=sphere_plot2)
        plt.close()

    if volumetric_bem:         # volumetric source space bounded by BEM
        v_bem = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=None,
                                                 bem=bem, surface=None)
        mne.write_source_spaces(vbem_name, v_bem, overwrite=overwrite)
        # source space plot
        bem_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                          surfaces='white', coord_frame='head', src=v_bem)
        mm.title('Volumetric Source Space Bounded By BEM (Inner Skull)')
        vbem_save = op.join(src_dir, '%s_v_bem_plot.png' % subject)
        mm.savefig(filename=vbem_save, figure=bem_plot)
        mm.close()
        # bem plot
        vbem_plot2 = mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir,
                                          src=v_bem)
        vbem2_save = op.join(src_dir, '%s_vbem_plot_bem.png' % subject)
        plt.title('Volumetric Source Space Bounded By BEM (Inner Skull)')
        plt.savefig(fname=vbem2_save, figure=vbem_plot2)
        plt.close()
    if volumetric_surf:      # volumetric source space bounded by pial surf
        v_surf = mne.setup_volume_source_space(subject=subject, subjects_dir=subjects_dir, sphere=None,
                                                 bem=None, surface=brain_surf)
        mne.write_source_spaces(vsurf_name, v_surf, overwrite=overwrite)
        # source space plot
        surf_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir,
                                           surfaces='white', coord_frame='head', src=v_surf)
        vsurf_save = op.join(src_dir, '%s_v_surf_plot.png' % subject)
        mm.title('Volumetric Source Space Bounded By Brain (Pial) Surface')
        mm.savefig(filename=vsurf_save, figure=surf_plot)
        mm.close()
        # bem plot
        vsurf_plot2 = mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir,
                                           src=v_surf)
        vsurf2_save = op.join(src_dir, '%s_v_surf_plot_bem.png' % subject)
        plt.title('Volumetric Source Space Bounded By Brain (Pial) Surface')
        plt.savefig(fname=vsurf2_save, figure=vsurf_plot2)
        plt.close()
    if warp_surface:      # subject is warped fsaverage, not indv
        warp_surf = mne.setup_source_space(subject=warp_subject, subjects_dir=subjects_dir, n_jobs=n_jobs,
                                           spacing=spacing)
        mne.write_source_spaces(wsurf_name, warp_surf, overwrite=overwrite)
        # source space plot
        ws_plot = mne.viz.plot_alignment(subject=warp_subject, subjects_dir=subjects_dir, surfaces='white',
                                        coord_frame='head', src=warp_surf)
        mm.title('Template-based Surface Source Space (GM/WM Boundary)')
        wsurf_save = op.join(src_dir, '%s_wsurf_plot.png' % subject)
        mm.savefig(filename=wsurf_save, figure=ws_plot)
        mm.close()
        # bem plot
        wsurf_plot2 = mne.viz.plot_bem(subject=warp_subject, subjects_dir=subjects_dir,
                                       src=warp_surf)
        wsurf_save2 = op.join(src_dir, '%s_wsurf_plot_bem.png' % subject)
        plt.title('Template-based Surface Source Space (GM/WM Boundary)')
        plt.savefig(fname=wsurf_save2, figure=wsurf_plot2)
        plt.close()
    if anat_surface:       # WM/GM surface-only source space
        surf = mne.setup_source_space(subject=subject, subjects_dir=subjects_dir, n_jobs=n_jobs, spacing=spacing)
        mne.write_source_spaces(surf_name, surf, overwrite=overwrite)
        # source space plot
        s_plot = mne.viz.plot_alignment(subject=subject, subjects_dir=subjects_dir, surfaces='white',
                               coord_frame='head', src=surf)
        mm.title('MRI-based Surface Source Space (GM/WM Boundary)')
        surf_save = op.join(src_dir, '%s_surf_plot.png' % subject)
        mm.savefig(filename=surf_save, figure=s_plot)
        mm.close()
        # bem plot
        s_plot2 = mne.viz.plot_bem(subject=subject, subjects_dir=subjects_dir,
                                   src=surf)
        surf2_save = op.join(src_dir, '%s_surf_plot_bem.png' % subject)
        plt.title('MRI-based Surface Source Space (GM/WM Boundary)')
        plt.savefig(fname=surf2_save, figure=s_plot2)
        plt.close()
    else:
        print('No source space model selected. Finished with subject %s.' % subject)




