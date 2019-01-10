# -*- coding: utf-8 -*-

"""This script is a template for processing data using mnefun."""

# imports

import mne
import mnefun

# paths to important places

raw_dir =

# subjects

subjects = []

# parameters needed by mnefun functions

study_params = mnefun.Params()

# multiple functions need the following parameters

study_params.
study_params.
study_params.
study_params.
study_params.
study_params.
study_params.
study_params.

# for fetch_raw
study_params.
study_params.
study_params.

# for do_score
study_params.
study_params.
study_params.

# for push_raw
study_params.
study_params.
study_params.

# for do_sss
study_params.
study_params.
study_params.

# for fetch_sss
study_params.
study_params.
study_params.

# for channel fixing
study_params.
study_params.
study_params.

# for do_ssp
study_params.
study_params.
study_params.

# for apply_ssp
study_params.
study_params.
study_params.

# for write_epochs
study_params.
study_params.
study_params.


# specify what jobs to do

mnefun.do_processing(
    study_params,
    fetch_raw = False,
    do_score = False,
    push_raw = False,
    do_sss = False,
    fetch_sss = False,
    do_ch_fix = False,
    do_ssp = False,
    apply_ssp = False,
    write_epochs = False
)



