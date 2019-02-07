# -*- coding: utf-8 -*-
"""
GenZ pilot analysis script.

"""
import mne

from functools import partial

import numpy as np
from scipy import linalg
import itertools

from .io.pick import pick_types, pick_channels, pick_channels_regexp
from .io.constants import FIFF
from .io.ctf.trans import _make_ctf_coord_trans_set
from .forward import (_magnetic_dipole_field_vec, _create_meg_coils,
                      _concatenate_coils)
from .cov import make_ad_hoc_cov, compute_whitener
from .transforms import (apply_trans, invert_transform, _angle_between_quats,
                         quat_to_rot, rot_to_quat)
from .utils import verbose, logger, use_log_level, _check_fname, warn

from mne.chpi import (_get_hpi_info, _get_hpi_initial_fit, _magnetic_dipole_objective, _fit_magnetic_dipole,
_chpi_objective, _unit_quat_constraint, _fit_chpi_quat, _setup_hpi_struct, _fit_cHPI_amplitudes, _fit_device_hpi_positions)



# coil 1 = 83 hz
# coil 2 = 143 hz
# coil 3 = 203 hz
# coil 4 = 263 hz
# coil 5 = 323 hz


# define variables we need

coil_choices = ['one', 'two', 'three', 'four', 'five']

coil_placement = ['back', 'front']

positions = ['control', 'down', 'fardown', 'forward']

s_freq = [1000, 2000]

lowpass = [330, 660]

dir_path = '/home/nordme/data/cHPI_test'

files = []


# read in the raw file

raw = mne.io.read_raw_fif('path')

info = mne.io.read_info(raw)

# report Elekta's measurements from digitizing
# use the results from _get_hpi_initial_fit and raw_info to make sure they match

hpi_dig_locations = mne.chpi._get_hpi_initial_fit(info)
print('File: %s Initial coil locations: %s' % (file, hpi_dig_locations))
print('raw_info: %s' % raw.info['hpi_meas'])


# report mne-python calculations for coil location and coil distances
# use the results from _fit_device_hpi_positions





# report discrepencies between original and measured, plus measured fit quality





