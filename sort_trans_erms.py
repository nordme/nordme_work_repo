# -*- coding: utf-8 -*-
#
import os
import os.path as op
import shutil
import fnmatch as fn


target_dir = '/home/nordme/resting/'
raw_dir = '/brainstudio/MEG/genz/'
trans_dir = '/brainstudio/MEG/genz/genz_proc/active/trans/'

sub_dir = []

all_files = []
rs_list = []
erm_list = []
bads = ['genz102_9a',
        'genz107_9a',
        'genz127_9a',
        'genz204_11a',
        'genz215_11a',
        'genz217_11a',
        'genz301_13a',
        'genz303_13a',
        'genz304_13a',
        'genz306_13a',
        'genz315_13a',
        'genz317_13a',
        'genz405_15a',
        'genz407_15a',
        'genz409_15a']

# Search all the genz subject directories on brainstudio for erms and resting states.
# Eliminate pilot subjects.
# Make lists attaching the subject names to the appropriate sub-directories and files.



subjs = [d for d in os.listdir(raw_dir) if 'genz' in d]
subjs.sort()


for bad in bads:
    try:
        subjs.remove(bad)
        print('Removing bad subject %s' % bad)
    except ValueError:
        pass

rs_subjs = []

for subject in subjs:
    if fn.fnmatch(subject, 'genz9*'):
        print('Pilot subject ignored: %s' %subject)
    elif fn.fnmatch(subject, 'genz_9*'):
        print('Pilot ignored: %s' %subject)
    elif fn.fnmatch(subject, 'genz_proc'):
        print('Ignored: %s' %subject)
    elif fn.fnmatch(subject, 'genz_*'):
        print('Ignored: %s' %subject)
    elif fn.fnmatch(subject, 'genzbuttonbox_test'):
        print('Ignored: %s' % subject)
    else:
        rs_subjs.append(subject)

print(rs_subjs)

for subject in rs_subjs:
    sub =[s for s in os.listdir(raw_dir + subject) if op.isdir(op.join(raw_dir + subject + '/%s' %s))]
    # print(sub)
    for s in sub:
        sub_dir.append(op.join(raw_dir + subject + '/%s' % s))
        files = os.listdir(op.join(raw_dir + subject + '/%s' % s))
        for file in files:
            if 'rest' in file:
                all_files.append(file)
                rs_list.append((subject, s, file))
            if 'erm' in file:
                all_files.append(file)
                erm_list.append((subject, s, file))
            else:
                pass


# See if resting state and erm files exist in the target directory; if non-existent, add

resting_dir = '/home/nordme/resting/'

for s, d, f in rs_list:

    # make subject directory if needed
    if op.isdir(op.join(target_dir + s)):
        pass
    else:
        try:
            os.mkdir(op.join(target_dir + s))
            print('made directory %s' % op.join(target_dir + s))
        except OSError:
            print('Hmm. Check out the folder for subject %s' % s)

    # make raw directory if needed
    if op.isdir(op.join(target_dir + s + '/raw_fif')):
        pass
    else:
        try:
            os.mkdir(op.join(target_dir + s + '/raw_fif'))
            print('made directory %s' % op.join(target_dir + s + '/raw_fif'))
        except OSError:
            print('Hmm. Check out the folder for subject %s' % s)

    rs_source = op.join(raw_dir + s + '/%s/' % d + f)
    # print(rs_source)
    rs_dest = op.join(target_dir + s + '/raw_fif/' + f)
    # print(rs_dest)

    if op.isfile(rs_dest):
        print('Subject %s already has a resting state file.' % s)
    else:
        shutil.copy(rs_source, rs_dest)
        print('added resting state file to subject %s' % s)

for s, d, f in erm_list:

    # make subject directory if needed
    if op.isdir(op.join(target_dir + s)):
        pass
    else:
        try:
            os.mkdir(op.join(target_dir + s))
            print('made directory %s' % op.join(target_dir + s))
        except OSError:
            print('Hmm. Check out the folder for subject %s' % s)

    # make raw directory if needed
    if op.isdir(op.join(target_dir + s + '/raw_fif')):
        pass
    else:
        try:
            os.mkdir(op.join(target_dir + s + '/raw_fif'))
            print('made directory %s' % op.join(target_dir + s + '/raw_fif'))
        except OSError:
            print('Hmm. Check out the folder for subject %s' % s)

    erm_source = op.join(raw_dir + s + '/%s/' %d + f)
    # print(erm_source)
    erm_dest = op.join(target_dir + s + '/raw_fif/' + f)
    # print(erm_dest)
    if op.isfile(erm_dest):
        print('Subject %s already has an erm file.' % s)
    else:
        shutil.copy(erm_source, erm_dest)
        print('added erm file to subject %s' % s)


# Search brainstudio for trans files and sort them into the resting state directory


trans_files = os.listdir(trans_dir)
trans_files.sort()

trans_subjects = [op.join((file.strip('-trans.fif')) + 'a') for file in trans_files if 'genz' in file]


# put trans files into resting state subject folders that don't already have one

resting_dir = '/home/nordme/resting/'

# make resting state subject folders for trans files with no subject folder to match

for t in trans_subjects:
    if op.isdir(op.join(resting_dir + t)):
        pass
    else:
        try:
            os.mkdir(op.join(resting_dir + t))
            print('made directory %s' % op.join(resting_dir + t))
        except OSError:
            print('Hmm. A trans file for % s is having trouble.' % t)


for dir in os.listdir(resting_dir):
    if op.isdir(op.join(resting_dir + dir + '/trans/')):
        # print('Subject %s already has a resting trans folder.' % dir)
        pass
    elif 'genz' in dir:
        try:
            os.mkdir(op.join(resting_dir + dir + '/trans/'))
            print('made directory %s' % op.join(resting_dir + dir + '/trans'))
        except PermissionError:
            print('Need permission for subject %s.' % dir)
        except OSError:
            print('Hmm. A trans folder for % s is having trouble getting made.' % dir)


# sort trans files into trans folders for resting state subjects that don't already have a trans file

for t in trans_subjects:
    rest_dir = op.join(resting_dir + t + '/trans/')
    if op.isfile(op.join(rest_dir + t + '-trans.fif')):
        # print('Subject %s already has a resting trans file.' % t)
        pass
    elif op.isdir(rest_dir):
        shutil.copy(op.join(trans_dir + t + '-trans.fif'), rest_dir)
        print('put trans file in for subject %s' % t)
    else:
        print('Hmm. Check the resting state folder for %s.' % t)
