# -*- coding: utf-8 -*-

"""This script looks up folders in our anatomy directory,
chooses folders that have the mri naming convention, restructures those directories,
and renames the folders with the appropriate convention."""



import os
import os.path as op
import fnmatch as fm
import shutil


# get and sort all the folders from a directory

# parent_dir = '/mnt/meg/genz/meg/'

parent_dir = '/brainstudio/MEG/genz/anatomy/fix/'


print("Fetching folders from %s" % parent_dir)

folders = os.listdir(parent_dir)
folders.sort()

# choose folders to rename; compile list
genz_folders = []

for folder in folders:
    if 'sub-' in folder:
        # simplify the directory by moving base folders out
        try:
            os.rename(op.join(parent_dir + folder + '/ses-1/' + '%s_ses-1_fsmempr_ti1200_rms_1_freesurf_hires_adult/' % folder),
                  op.join(parent_dir + (folder.replace('sub-genz', 'genz'))))
        except FileNotFoundError:
            print('File %s not found.' % folder)
        genz_folders.append(folder.replace('sub-genz', 'genz'))

print('We are renaming these: %s' % genz_folders)

for folder in genz_folders:
    if fm.fnmatch(folder, 'genz5*'):
        os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '_17a'))
    elif fm.fnmatch(folder, 'genz4*'):
        os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '_15a'))
    elif fm.fnmatch(folder, 'genz3*'):
        os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '_13a'))
    elif fm.fnmatch(folder, 'genz2*'):
        os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '_11a'))
    elif fm.fnmatch(folder, 'genz1*'):
        os.rename(op.join(parent_dir + folder), op.join(parent_dir + folder + '_9a'))
    else:
        raise ValueError('Hey, this folder name is weird. Look at %s' % folder)


for folder in folders:
    if 'sub-' in folder:
        shutil.rmtree(op.join(parent_dir + folder))