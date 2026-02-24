from pathlib import Path
import mne
import numpy as np
from quaternion import quaternion
import csv

data_dir = Path('/media/erica/data1/m2m')
#subjects = [dir for dir in list(data_dir.walk())[0][1]]
subjects = ['acc_test',]


# frame_trigger_delay = 150
frame_trigger_delay = 0
# transformation matrix: optitrack coordinates to room coordinates
o_r_transform = np.array([[-0.3861917,  -0.7097543,   0.58915548, -1.28498289],
                          [-0.07634419,  0.66111041,  0.74639429,  1.61672498],
                          [-0.91925345,  0.24327291, -0.30950088, -0.36701521],
                          [ 0.,          0.,          0.,          1.        ]])

q_inv = quaternion(-0.491278328975763,
                   0.256026712140394,
                   -0.767594046531035,
                   -0.322327597157024)


def find_start_end(t_list):
    # a series of four 4 triggers marks start of recording
    # a series of six 4 triggers marks the end
    # sometimes channels start high, so we have to check we're finding
    # the right series
    fours = np.where(t_list[:, 2] == 4)[0]
    first_four, last_four = fours[0], fours[-1]
    #print(f'first, last: {first_four}, {last_four}')
    assert all(t_list[first_four:first_four+4, 2]==4)
    assert all(t_list[last_four-5:last_four, 2]==4)
    start = first_four+4
    end = last_four-5
    #print(start, end)
    return start, end


def clean_trigs(events):
    clean_events = events.copy()
    remove_idxs = []
    mid_digits = [e for e in events if e[1] > 0]
    md_idxs = np.where(events[:, 1]>0)[0]
    for mdi, md in zip(md_idxs, mid_digits):
        prior_ev = events[mdi-1]
        if prior_ev[0] == md[0]-1:
            remove_idxs.append(mdi-1)
    print(f'Removing {len(remove_idxs)} triggers with 1 ms dur')
    first_pass = np.delete(clean_events, remove_idxs, axis=0)
    also_remove = np.where(first_pass[:, 2]>10)[0]  # condition markers
    all_clean = np.delete(first_pass, also_remove, axis=0)
    return all_clean


def reconstruct_pos(frames, positions):
    pidx = 0
    skipped_rows = 0
    fixed_pos = np.zeros(len(fids, 7))
    for fidx in range(len(frames)):
        if frames[fidx, 1] == 1:
            fixed_pos[fidx] == positions[pidx]
            pidx += 1
        else:
            assert frames[fidx, 1] == 0
            skipped_rows += 1
    assert pidx == len(positions)
    assert skipped_rows == (len(frames)-pidx)
    return fixed_pos


def convert_to_room_coords(p_data, t_matrix, q_inv):
    out_pos = np.zeros(shape=(p_data.shape))
    for pidx, prow in enumerate(p_data):
        # preserve zero coordinates
        # zeros indicate where optitrack lost track of the helmet
        # we'll add position interpolation, if desired, during position
        # compensation; for now, keep zeros intact
        if all(prow)==0:
            out_pos[pidx] = prow
        else:
            pos_vector = [prow[0], prow[1], prow[2], 1]
            [posx, posy, posz, _] = t_matrix @ pos_vector
            # natnetsdk outputs quats with scalar, w, last
            q_cam = quaternion(prow[6], prow[3], prow[4], prow[5])
            q_out = q_inv * q_cam
            out_pos[pidx] = [posx, posy, posz, q_out.x, q_out.y, q_out.z, q_out.w]
    return out_pos


def samps_to_fids(pos_df, tts, raw):
    raw_diff = False
    nonzero = np.where(pos_df[:, 0] > 0)[0]
    assert len(nonzero) == len(tts)
    print(f'Filling in the blanks in between {len(nonzero)} sample pins')
    # fill in the sample blanks
    for nii, nonz in enumerate(nonzero[0:-1]):
        next = nonzero[nii + 1]
        samp1, id1 = pos_df[nonz, 0], pos_df[nonz, 1]
        samp2, id2 = pos_df[next, 0], pos_df[next, 1]
        samp_diff = samp2 - samp1
        id_diff = id2 - id1
        # print(nii, samp_diff, id_diff)
        try:
            assert np.allclose((samp_diff / id_diff), 8.3, atol=0.1), (
            (samp_diff / id_diff))
        except AssertionError:
            print(samp_diff / id_diff)
        n_fill = next-nonz
        fill_samps = np.linspace(samp1, samp2, n_fill)
        fill_samps = np.round(fill_samps)
        assert fill_samps[0] == samp1
        assert len(pos_df[nonz+1:next]) == len(fill_samps[1:])
        pos_df[nonz+1:next, 0] = fill_samps[1:]

    # beginning samples
    assert all(pos_df[0:nonzero[0], 0] == 0)
    n_bsamps = 8.3*(nonzero[0])
    start_f, start_s = sp_out[nonzero[0], 1], sp_out[nonzero[0], 0]
    first_bsamp = start_s-n_bsamps
    #begins = np.arange(first_bsamp, start_s, 8.3)
    begins = np.round(np.linspace(first_bsamp, start_s, nonzero[0]+1))
    if first_bsamp < raw.first_samp:
        print(f'*** Warning: Record raw started after stim script!')
        begins[begins<0] = 0
        raw_diff = True
    assert pos_df[nonzero[0], 0] == begins[-1]
    pos_df[0:nonzero[0], 0] = begins[0:-1]
    # end samples
    assert all(pos_df[nonzero[-1]+1:, 0] == 0)
    n_esamps = 8.3*((len(pos_df)-1)-nonzero[-1])
    end_f, end_s = sp_out[nonzero[-1], 1], sp_out[nonzero[-1], 0]
    last_esamp = end_s + n_esamps
    n_ends = len(pos_df) - nonzero[-1]
    ends = np.round(np.linspace(end_s, last_esamp+1, n_ends, endpoint=False))
    if last_esamp > raw.last_samp:
        print(f'*** Warning: Record raw ended before stim script end!')
        ends[ends>raw.last_samp] = 0
        raw_diff = True
    #ends = np.arange(end_s, last_esamp+1, 8.3)
    pos_df[nonzero[-1]+1:, 0] = ends[1:]
    return pos_df, raw_diff



for sub in subjects:
    print(f'Starting subject {sub} position file creation.')
    sub_dir = data_dir / sub
    _, _, f_names = list(sub_dir.walk())[0]
    # raw_name = sub_dir / f'{sub}_4m_01_raw.fif'
    try:
        raw_name = sub_dir / [rn for rn in f_names if 'raw.fif' in rn][0]
        fid_name = sub_dir / [fn for fn in f_names if 'fids' in fn][0]
        pos_name = sub_dir / [pn for pn in f_names if 'pos' in pn][0]
        tab_name = sub_dir / [tn for tn in f_names if 'tab' in tn][0]
    except IndexError:
        #raise RuntimeWarning(f'Subject {sub} is missing files.')
        print(f'Subject {sub} is missing files.')
        continue
    except Exception as e:
        print(e)
        continue
    t_trigs = []
    fids = []
    posd = []
    sp_out = []
    # load fids and pos
    with open(fid_name, 'r') as f_file:
        fids = np.loadtxt(f_file, converters=float, dtype=int)
    with open(pos_name, 'r') as p_file:
        posd = np.loadtxt(p_file, dtype=float)
    with open(tab_name, 'r') as f:
        reader = csv.reader(f, delimiter="\t")
        for ri, row in enumerate(reader):
            if ri>=2:
                if row[1]=='frame_id':
                    frow = row
                    trg, fid = row[2].split(',')
                    trg = int(trg.strip('['))
                    fid = int(fid.strip(']').strip(' ').strip("'").strip("'"))
                    t_trigs.append([trg, fid])

    # load raw
    raw = mne.io.read_raw_fif(raw_name, allow_maxshield=True)
    # find raw events
    orig_trigs = mne.find_events(raw, mask=15, shortest_event=1)
    # remove start and end series
    orig_start, orig_end = find_start_end(orig_trigs)
    r_trigs = orig_trigs[orig_start+1:orig_end]
    r_trigs = np.array(r_trigs)
    r_trigs = clean_trigs(r_trigs)

    # match pos to fids
    if len(fids) > len(posd):
        raise RuntimeWarning(f'******** Warning: missing rigid body data!!')
        rb_missing = np.where(fids[:, 1] < 1)[0]
        print(
            f'n fids={len(fids)}, n pos={len(pos)}, fids no pos={rb_missing}')
        posd = reconstruct_pos(fids, posd)
        assert len(fids) == len(posd)
    else:
        assert len(fids) == len(posd)
        assert all(fids[:, 1] == 1)
        fids = np.array(fids)
        pos = np.array(posd)

    pos = convert_to_room_coords(pos, o_r_transform, q_inv)

    # ensure that raw triggers match tab file triggers
    if len(t_trigs) != len(r_trigs):
        raise RuntimeError(f'******* Error: mismatched triggers! Tab file:'
                           f' {len(t_trigs)} trigs; raw file: {len(r_trigs)}')
    else:
        assert len(t_trigs) == len(r_trigs)
        t_trigs = np.array(t_trigs)
        assert np.allclose(t_trigs[:, 0], r_trigs[:, 2])

    # Construct sample-position matching file
    sp_out = np.zeros(shape=(len(fids), 9))
    # match fids to MEG samples
    for ffi, fd in enumerate(fids):
        sp_out[ffi][1] = fd[0]
        sp_out[ffi][2:] = posd[ffi]

        # check for frame id in tab trig list
        if fd[0] in t_trigs[:, 1]:
            rt_idx = list(t_trigs[:,1]).index(fd[0])
            # add the meg sample to out list, correcting for delay
            sp_out[ffi][0] = r_trigs[rt_idx][0] - frame_trigger_delay

    assert len(np.where(sp_out[:, 0] > 0)[0]) == len(t_trigs)
    sp_out, raw_diff = samps_to_fids(sp_out, t_trigs, raw)

    nz_check = np.where(sp_out[:, 0] == 0)[0]
    if nz_check.size > 0:
        assert raw_diff
    else:
        assert nz_check.size==0
        assert not raw_diff

    # output in txt
    out_name = sub_dir / f'{raw_name.stem}_samplesxframes.csv'
    with open(out_name, 'w') as out_f:
        writer = csv.writer(out_f)
        for row in sp_out:
            writer.writerow(row)
    print(f'Saving position file to {out_name}')
