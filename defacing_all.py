from pathlib import Path
import numpy as np
import nibabel as nb
import mne
from mne.bem import make_watershed_bem
from mne.io.constants import FIFF
import mne_bids
from mne_bids.write import _deface
from mne.transforms import apply_trans



s_dir = Path('/media/erica/data2/anat_subjects')

subjects = ['sample', 'genz532_17a']
d_dirs = [Path('/home/erica/mne_data/MNE-sample-data/MEG'),
          Path('/media/erica/data2/genz/t1/twa_hp')]
raw_fns = ['sample_audvis_raw.fif',
           'raw_fif/genz532_17a_faces_learn_01_raw.fif']
trans_fns = ['sample_audvis_raw-trans.fif', 'trans/genz532_17a-trans.fif']

prefloods = [5, 18]

for si, sub in enumerate(subjects):
    print(f'Working on defacing subject {sub}')
    df_save = s_dir / sub / 'mri' / 'df_T1.mgz'
    check_dir = s_dir / sub / 'bem' / 'orig'
    assert check_dir.exists()
    # load trans
    t_path = d_dirs[si] / sub / trans_fns[si]
    trans = mne.read_trans(t_path)
    # get dig points
    r_path = d_dirs[si] / sub / raw_fns[si]
    raw = mne.io.read_raw_fif(r_path, allow_maxshield=True)
    fids = [p["r"] for p in raw.info["dig"] if
            p["kind"] == FIFF.FIFFV_POINT_CARDINAL]
    assert raw.info["dig"][0]["coord_frame"] == FIFF.FIFFV_COORD_HEAD

    # get T1
    t1_path = s_dir / sub / 'mri' / 'T1.mgz'
    t1 = nb.load(t1_path)

    # get transform to MRI coordinate space
    vox_to_ras = t1.header.get_vox2ras_tkr()
    ras_to_vox = np.linalg.inv(vox_to_ras)


    df_fids = np.zeros((3, 3))
    # put dig points into MRI coordinate space
    for fi, fid in enumerate(fids):
        trans_t1 = apply_trans(trans, fid, move=True)
        df_fids[fi] = apply_trans(ras_to_vox, trans_t1 * 1e3, move=True)

    # deface MRI
    print(f'Starting defacing')
    df_t1 = _deface(t1, df_fids, True)
    nb.save(df_t1, df_save)

    # generate defaced surfs
    print(f'Generating defaced surfaces for sub {sub}')
    df_surfs = make_watershed_bem(sub, subjects_dir=s_dir, volume=df_save,
                                  preflood=prefloods[si], overwrite=True)

    plot = mne.viz.plot_alignment(raw.info, trans, sub, s_dir,
                                  surfaces=dict(outer_skull=0.4,
                                                inner_skull=0.4, head=0.2),
                                  meg=False)
    p_save = s_dir / sub / 'bem' / f'{sub}_deface_surfaces.png'
    plot.plotter.screenshot(p_save)
    
    # BEM model + sol
    print(f'Starting BEM for sub {sub}')
    bsurf_name = s_dir / sub / 'bem' / f'{sub}-5120-5120-5120-bem.fif'
    bsol_name = s_dir / sub / 'bem' / f'{sub}-5120-5120-5120-bem-sol.fif'

    b_model = mne.make_bem_model(sub, ico=4, subjects_dir=s_dir, )
    b_sol = mne.make_bem_solution(b_model)