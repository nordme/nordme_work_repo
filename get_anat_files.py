# -*- coding: utf-8 -*-

"""This script copies mri files to our MEG anat directory,
chooses folders in anat that have the mri naming convention,
and renames the folders with the appropriate convention."""



import os
import os.path as op
import fnmatch as fm
import shutil



# copy files from MRI to MEG

mri_dir ='/brainstudio/MRI/data/genz/'
parent_dir = '/brainstudio/MEG/genz/anatomy/fix/'

subjects = ['sub-genz527',
            'sub-genz528',
            'sub-genz529',
            'sub-genz531']

print('Pulling files to %s for specified subjects.' % parent_dir)

for sub in subjects:
    source = op.join(mri_dir + sub + '/ses-1/' + '%s_ses-1_fsmempr_ti1200_rms_1_freesurf_hires_adult' % sub)
    shutil.copytree(source, op.join(parent_dir + sub))
    print('Added %s' % sub)


# get and sort all the folders to rename from a directory

print("Renaming folders from %s" % parent_dir)

folders = os.listdir(parent_dir)
folders.sort()

# choose folders to rename; compile list
genz_folders = []

for folder in folders:
    if 'sub-' in folder:
        try:
            os.rename(op.join(parent_dir + folder),
                  op.join(parent_dir + (folder.replace('sub-genz', 'genz'))))
            print('Renaming %s' % folder)
        except FileNotFoundError:
            print('File %s not found.' % folder)
        genz_folders.append(folder.replace('sub-genz', 'genz'))
#

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
