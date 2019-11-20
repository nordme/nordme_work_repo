# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import numpy as np

# pre_camp: twa_hp; erp to erp dir, then pskt to pskt dir
# pre_camp: fixed_hp; pskt to pskt dir

# post_camp: twa_hp: erp to erp dir, then pskt to pskt dir
# post_camp: fixed_hp; pskt to pskt dir


pre_or_post = 'post'
fixed_or_twa = 'twa_hp'
erp_or_pskt = 'erp'
raw_subdirs = True  # whether the source directory has date subdirectories or a 'raw_fif' subdirectory

# target_dir = '/mnt/scratch/prek/%s_camp/%s/%s/' % (pre_or_post, fixed_or_twa, erp_or_pskt)
# source_dir = '/mnt/scratch/prek/%s_camp/twa_hp/' % (pre_or_post)
# trans_dir = '/home/nordme/prek/trans/'

target_dir = '/home/nordme/data/prek/post_camp/twa_hp/'

subjects = [d for d in os.listdir(target_dir) if op.isdir(op.join(target_dir, d))
            and 'prek' in d
            and not 'prek_2' in d
            and not 'prek_9' in d]
subjects.sort()

# exclude subjects with split recording sessions -- do those manually
manual_sync = []
brainstudio_path = '/brainstudio/MEG/prek/'
prek_dirs = [x for x in os.listdir(brainstudio_path) if 'prek' in x and not 'prek_2' in x and not 'prek_9' in x]
for prek_dir in prek_dirs:
    date_dirs = os.listdir(op.join(brainstudio_path, prek_dir))
    if len(date_dirs) != 2:
        manual_sync.append(prek_dir)

manual_sync.sort()
print('Please manually sync the following: \n', manual_sync)

erm_dir = '/brainstudio/MEG/prek/empty_room/'

# check to see which subjects already have an empty room

for prek_dir in subjects:
    if not np.in1d(prek_dir, manual_sync):
        path = op.join(target_dir, prek_dir, 'raw_fif', '%s_erm_raw.fif' % prek_dir)
        if op.isfile(path):
            print('Subject %s has a specific erm file under raw_fif.' % prek_dir)
        else:
            pass

# sort empty rooms by date into subject folders

for prek_dir in subjects:
    if not np.in1d(prek_dir, manual_sync):
        sub_dirs = os.listdir(op.join(brainstudio_path, prek_dir))
        sub_dirs.sort()
        if pre_or_post == 'pre':
            sub_dir = sub_dirs[0]
        else:
            sub_dir = sub_dirs[1]
        # locate the empty room file with the same date
        erm_path = op.join(erm_dir, sub_dir, 'prek_%s_erm_raw.fif' % sub_dir)
        if op.isfile(erm_path):
            print('Empty room %s found for subject %s.' % (erm_path, prek_dir))
            erm_source = erm_path
            erm_dest = op.join(target_dir, prek_dir, 'raw_fif', '%s_erm_raw.fif' % prek_dir)
            if op.isfile(erm_dest):
                print('Subject %s already has an erm file.' % prek_dir)
            else:
                shutil.copyfile(erm_source, erm_dest)
        else:
            print('No empty room found for subject %s. A misspelling, perhaps?' % prek_dir)


