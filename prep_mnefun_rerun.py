'''
mnefun doesn't automatically allow overwriting. This script prepares a
directory of processed data for mnefun reruns by deleting all the old files
that would otherwise cause an mnefun crash.

****** THIS SCRIPT DELETES FILES. USE WITH CAUTION ******
'''

import os
import os.path as op
import re
from mne.utils import logger

#s_dir = '/media/erica/data1/genz/control/twa_hp'
#s_dir = '/media/erica/data1/genz/t2/twa_hp/rs_only'
s_dir = '/media/erica/data1/genz/t1/twa_hp'
#subjects = sorted([x for x in os.listdir(s_dir) if x.startswith('genz')])
#subjects = ['erica_peterson']
subjects = ['genz131_9a', 'genz226_11a', 'genz331_13a',  # fix 1842
            'genz421_15a', # fix 1421, 1431, 2611
            'genz527_17a', # fix 1743
            'genz115_9a',]

erm = True
lists = False
pca = True
epochs = True
#conds = ['faces', 'emojis', 'rest']
#conds = ['rest_01']
#conds = ['1', '2', '3', 'rest']
conds = ['faces_learn_01', 'emojis_learn_01', 'thumbs_learn_01', 'rest_01',
         'faces_test_01', 'emojis_test_01', 'thumbs_test_01']
raws = ['.pos', '-chpi_locs.h5', '-counts.h5', '_maxbad.txt']
#raws = False
cov_runs = ['aud-80-sss', 'erm_allclean_fil']
inv_runs = ['_aud-80-sss-meg', '-meg-erm']
inv_suffs = ['fixed-', 'free-', '']

def del_files(path_list):
    for path in path_list:
        if op.exists(path):
            os.remove(path)
            logger.info('Deleted %s' % path.split('/')[-1])

for s in subjects:
    sub_dir = op.join(s_dir, s)
    if lists:
        l_paths = [op.join(sub_dir, 'lists', f'ALL_{s}_{c}-eve.lst')
                 for c in conds]
        del_files(l_paths)
    if raws:
        r_paths = [op.join(sub_dir, 'raw_fif', f'{s}_{c}_raw{r}')
                   for c in conds
                   for r in raws]
        r_paths.append(op.join(sub_dir, 'raw_fif', f'{s}_twa_pos.fif'))
        if erm:
            r_paths.append(op.join(sub_dir, 'raw_fif',
                                   f'{s}_erm_raw_maxbad.txt'))
        del_files(r_paths)
    if pca and op.exists(op.join(sub_dir, 'sss_pca_fif')):
        p_paths = [op.join(sub_dir, 'sss_pca_fif', x)
                   for x in os.listdir(op.join(sub_dir, 'sss_pca_fif'))
                   if re.match('preproc_', x)]
        del_files(p_paths)
    if epochs and op.exists(op.join(sub_dir, 'epochs')):
        e_paths = [op.join(sub_dir, 'epochs', f'All_80-sss_{s}-epo.fif')]
        del_files(e_paths)
    if cov_runs and op.exists(op.join(sub_dir, 'covariance')):
        c_paths = [op.join(sub_dir, 'covariance', f'{s}_{cv}-cov.fif')
                   for cv in cov_runs]
        if erm:
            c_paths.append(op.join(sub_dir, 'covariance',
                                   f'{s}_erm_allclean_fil80-sss-cov.fif'))
        del_files(c_paths)
    if inv_runs and op.exists(op.join(sub_dir, 'inverse')):
        i_paths = [op.join(sub_dir, 'inverse', f'{s}{ir}-{isf}inv.fif')
                   for ir in inv_runs
                   for isf in inv_suffs]
        i_paths.append(op.join(sub_dir, 'inverse',
                               f'All_80-sss_eq_{s}-ave.fif'))
        del_files(i_paths)
