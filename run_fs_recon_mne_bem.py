# -*- coding: utf-8 -*-

"""Run FreeSurfer reconstruction. Compute MNE BEM. Create skin surface and
  MNE source space."""

# Authors: Kambiz Tavabi <ktavabi@gmail.com>
# License: MIT

import os
import os.path as op
import copy
from shutil import copyfile
import time
import mne
from mne.utils import run_subprocess
import fnmatch

# from nbwr.picks import subjects
# from meeg_processing.utils import find_files

# subjects_dir = get_subjects_dir(None, raise_error=True)
subjects_dir = '/brainstudio/MEG/genz/anatomy'
environ = copy.copy(os.environ)
environ['SUBJECTS_DIR'] = subjects_dir
run_recon = False
do_rms = False
do_flash = False
n_jobs = 6


def find_files(pattern, path):
   """Return list of names for filename pattern search."""
   result = []
   for root, dirs, files in os.walk(path):
       for name in files:
           if fnmatch.fnmatch(name, pattern):
               result.append(op.join(root, name))
   return result


subjects = ['530_17a',
            '532_17a']

for subject in subjects:
    t0 = time.time()
    subject = 'genz%s' % subject
    print('     Processing static for %s...' % subject)
    mri_dir = op.join(subjects_dir, subject, 'mri')
    # mk nii & orig dirs
    nii_dir = op.join(subjects_dir, subject, 'nii')
    orig_dir = op.join(mri_dir, 'orig')
    if not op.exists(nii_dir):
        os.makedirs(nii_dir)
    if not op.exists(orig_dir):
        os.makedirs(orig_dir)
    bem_dir = op.join(subjects_dir, subject, 'bem')
    # link T1.nii to mprage in mri dir
    T1_ = find_files('*MEMP*.nii.gz',
                     op.join(subjects_dir, subject))
    try:
        if len(T1_) < 1:
            raise RuntimeWarning('T1 volume not found')
        os.symlink(op.join(nii_dir, op.basename(T1_[0])[:-3]),
                   op.join(nii_dir, 'T1.nii'))
        mprage = op.join(nii_dir, 'T1.nii')
    except RuntimeWarning:
        pass

    # FS recon
    if run_recon:
        print('     Starting FreeSurfer reconstruction process...')
        if do_rms:
            run_subprocess(['mri_concat', '--rms', '--i', mprage,
                            '--o', op.join(subjects_dir,
                                           subject, 'mri/orig/001.mgz')],
                           env=environ)
        else:
            run_subprocess(['mri_convert', mprage,
                            op.join(subjects_dir, subject, 'mri/orig/001.mgz')])
        run_subprocess(['recon-all', '-subject', subject, '-all'],
                       env=environ)
    # BEM
    run_subprocess(['mne_setup_mri', '--mri', 'T1', '--subject', subject,
                    '--overwrite'], env=environ)
    if do_flash:
        print('     Starting flash BEM  process...')
        fa_param_dir = op.join(mri_dir, 'flash', 'parameter_maps')
        if not op.exists(fa_param_dir):
            os.makedirs(fa_param_dir)
        # link spgr nii vols to flash5 and flash30 in parameter_maps dir
        for fa, ln in zip(('5', '30'), ('flash5', 'flash30')):
            fl_vol = find_files(
                subject + '_ses-1_spgr_fa-%s-tr-12p0_1.nii' % fa,
                bs_path + subject)
            if len(fl_vol) < 1:
                raise RuntimeError('%s volume not found' % fl_vol[0])
            copyfile(fl_vol[0], op.join(nii_dir, op.basename(fl_vol[0])))
            os.symlink(op.join(nii_dir, op.basename(fl_vol[0])),
                       op.join(fa_param_dir, ln))
        for ii, fa in enumerate(('5', '30')):
            print('     Processing flash%s...' % fa)
            nii_file = op.join(nii_dir, 'flash%s.nii' % fa)
            mgz_file = op.join(fa_param_dir, 'flash%s.mgz' % fa)
            run_subprocess(['mri_convert', nii_file, mgz_file],
                           env=environ)
            run_subprocess(['fsl_rigid_register',
                            '-r', op.join(mri_dir, 'rawavg.mgz'),
                            '-i', op.join(mri_dir, 'flash', 'flash%s.mgz' % fa),
                            '-o', op.join(mri_dir, 'flash',
                                          'flash%s_reg.mgz' % fa)],
                           env=environ)
            os.mkdir(op.join(mri_dir, 'flash%s' % fa))
            run_subprocess(['mri_convert', '-ot', 'cor',
                            op.join(mri_dir, 'flash', 'flash%s_reg.mgz' % fa),
                            op.join(mri_dir, 'flash%s' % fa)], env=environ)
        run_subprocess(['mri_convert', '-ot', 'cor',
                        op.join(mri_dir, 'brainmask.mgz'),
                        op.join(mri_dir, 'brain')])
        run_subprocess(['mri_convert', '-ot', 'cor',
                        op.join(mri_dir, 'T1.mgz'),
                        op.join(mri_dir, 'T1')])
        run_subprocess(['mri_make_bem_surfaces', subject], env=environ)
        run_subprocess(['mne', 'watershed_bem', '--subject', subject,
                        '--overwrite'], env=environ)
        for srf in ('inner', 'outer'):
            run_subprocess(['mne_convert_surface', '--tri',
                            op.join(bem_dir, '%s_skull.tri' % srf),
                            '--swap', '--surfout',
                            op.join(bem_dir, '%s_skull.surf' % srf)],
                           env=environ)
        # copyfile(op.join(bem_dir, 'watershed',
        #                  '%s_outer_skin_surface' % subject),
        #          op.join(bem_dir, 'outer_skin.surf'))
    else:
        print('     Starting Watershed BEM  process...')
        run_subprocess(['mne', 'watershed_bem', '--subject', subject,
                        '--preflood', '12', '--overwrite'],
                       env=environ)

    # Create dense head surface and symbolic link to head.fif file
    print('     Creating high resolution skin surface...')
    run_subprocess(['mne', 'make_scalp_surfaces',
                    '--overwrite', '--subject', subject, '--force'], env=environ)
    if op.isfile(op.join(subjects_dir, subject, 'bem/%s-head.fif' % subject)):
        os.rename(op.join(subjects_dir, subject, 'bem/%s-head.fif' % subject),
                  op.join(subjects_dir, subject,
                          'bem/%s-head-sparse.fif' % subject))
    os.symlink(
        (op.join(subjects_dir, subject, 'bem/%s-head-dense.fif' % subject)),
        (op.join(subjects_dir, subject, 'bem/%s-head.fif' % subject)))

    # Create source space
    print('        Creating mne forward model...')
    if do_flash:
        run_subprocess(['mne_setup_forward_model', '--surf', '--ico',
                        '4', '--subject', subject, '--scalpshift 3'], env=environ)
    else:
        # Can try '--outershift'  & '--scalpshift' for problematic cases
        run_subprocess(['mne_setup_forward_model', '--homog', '--surf', '--ico',
                        '4', '--subject', subject], env=environ)
    print('     Creating mne  source space...')
    src = mne.setup_source_space(subject, spacing='oct6', n_jobs=n_jobs)
    src.save(op.join(subjects_dir, subject, 'bem',
                     '%s-oct-6-src.fif' % subject),
             overwrite=True)
    run_subprocess(['mne_make_morph_maps', '--from', subject,
                    '--to', 'fsaverage', '--redo'], env=environ)
    # f = plot_bem(subject=subject, subjects_dir=subjects_dir,
    #              brain_surfaces='white', orientation='coronal', show=False)
    # f.savefig(op.join(subjects_dir, subject, '%s_bem.png' % subject), dpi=200,
    #           format='png')
    # plt.close(plt.gcf())
    print('    Time: %s mns' % round((time.time() - t0) / 60., 2))
