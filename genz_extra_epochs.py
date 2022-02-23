# -*- coding: utf-8 -*-
import os
import mne
import os.path as op
import matplotlib.pyplot as plt
import numpy as np

data_dir = '/data/egenz'
subjects = ['erica_peterson']
# peaks = dict(N100=[80, 120], P250=[230, 270],  P550=[530, 570])
peaks = dict(N100=[80, 120], P250=[230, 270],  P400=[400, 500])
# conditions = ['s01', 's02', 's03']
# conditions = ['s01', 's02']
conditions = ['s02']
lambda2 = 1/(3**2)
atlas = 'HCPMMP1'
target_labels = ['R_STSdp_ROI-rh', 'L_STSdp_ROI-lh']
decim=4

syls = ['s01', 's02', 's03']
times = [100, 200, 400]
windows = ['f20', 'l20', 'whole']

# plot epoch topo plots by syl

for subject in subjects:
    sub_path = op.join(data_dir, subject)
    inv_path = op.join(sub_path, 'inverse',
                       '%s_aud-80-sss-meg-inv.fif' % subject)
    faces = op.join(sub_path, 'sss_pca_fif',
                    '%s_faces_allclean_fil80_raw_sss.fif' % subject)
    emojis = op.join(sub_path, 'sss_pca_fif',
                     '%s_emojis_allclean_fil80_raw_sss.fif' % subject)
    faces = mne.io.read_raw_fif(faces)
    emojis = mne.io.read_raw_fif(emojis)
    ep_dir = op.join(sub_path, 'epochs')

    f_ev = mne.read_events(op.join(sub_path, 'lists',
                                   'ALL_%s_faces-eve.lst' % subject))
    e_ev = mne.read_events(op.join(sub_path, 'lists',
                                   'ALL_%s_emojis-eve.lst' % subject))

    pic_dir = op.join(sub_path, 'images')

    ### s01

    fn1_evs = [x for x in f_ev if x[2] - 1121 == 0]
    fp1_evs = [x for x in f_ev if x[2] - 1111 == 0]
    en1_evs = [x for x in e_ev if x[2] - 1211 == 0]
    ep1_evs = [x for x in e_ev if x[2] - 1221 == 0]

    ep1 = mne.Epochs(emojis, ep1_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    en1 = mne.Epochs(emojis, en1_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    fp1 = mne.Epochs(faces, fp1_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    fn1 = mne.Epochs(faces, fn1_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')

    ep1_100 = mne.Epochs(emojis, ep1_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    en1_100 = mne.Epochs(emojis, en1_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    fp1_100 = mne.Epochs(faces, fp1_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    fn1_100 = mne.Epochs(faces, fn1_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')

    ep1_200 = mne.Epochs(emojis, ep1_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    en1_200 = mne.Epochs(emojis, en1_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    fp1_200 = mne.Epochs(faces, fp1_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    fn1_200 = mne.Epochs(faces, fn1_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')

    ep1_400 = mne.Epochs(emojis, ep1_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    en1_400 = mne.Epochs(emojis, en1_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    fp1_400 = mne.Epochs(faces, fp1_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    fn1_400 = mne.Epochs(faces, fn1_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')

    s1_data = ((ep1.get_data() +
                    en1.get_data() +
                    fp1.get_data() +
                    fn1.get_data()) / 4)

    s1 = mne.Epochs(emojis, ep1_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    s1._data = s1_data
    s1.save(op.join(ep_dir, 's1_entire-epo.fif'), overwrite=True)

    f20_s1_data = ((ep1.get_data()[0:20] +
                        en1.get_data()[0:20] +
                        fp1.get_data()[0:20] +
                        fn1.get_data()[0:20]) / 4)

    f20_s1 = mne.Epochs(emojis, ep1_evs[0:20], tmin=-0.1, tmax=0.75,
                            baseline=None, picks='meg')
    f20_s1._data = f20_s1_data
    f20_s1.save(op.join(ep_dir, 'f20_s1_entire-epo.fif'),
                    overwrite=True)

    l20_s1_data = ((ep1.get_data()[-20:] +
                        en1.get_data()[-20:] +
                        fp1.get_data()[-20:] +
                        fn1.get_data()[-20:]) / 4)

    l20_s1 = mne.Epochs(emojis, ep1_evs[-20:], tmin=-0.1, tmax=0.75,
                            baseline=None, picks='meg')
    l20_s1._data = l20_s1_data
    l20_s1.save(op.join(ep_dir, 'l20_s1_entire-epo.fif'),
                    overwrite=True)


    s1_100_data = ((ep1_100.get_data() +
                        en1_100.get_data() +
                        fp1_100.get_data() +
                        fn1_100.get_data()) / 4)

    s1_100 = mne.Epochs(emojis, ep1_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    s1_100._data = s1_100_data
    s1_100.save(op.join(ep_dir, 's1_100_whole-epo.fif'), overwrite=True)

    f20_s1_100_data = ((ep1_100.get_data()[0:20] +
                        en1_100.get_data()[0:20] +
                        fp1_100.get_data()[0:20] +
                        fn1_100.get_data()[0:20]) / 4)

    f20_s1_100 = mne.Epochs(emojis, ep1_evs[0:20], tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    f20_s1_100._data = f20_s1_100_data
    f20_s1_100.save(op.join(ep_dir, 'f20_s1_100_whole-epo.fif'), overwrite=True)

    l20_s1_100_data = ((ep1_100.get_data()[-20:] +
                        en1_100.get_data()[-20:] +
                        fp1_100.get_data()[-20:] +
                        fn1_100.get_data()[-20:]) / 4)

    l20_s1_100 = mne.Epochs(emojis, ep1_evs[-20:], tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    l20_s1_100._data = l20_s1_100_data
    l20_s1_100.save(op.join(ep_dir, 'l20_s1_100_whole-epo.fif'), overwrite=True)

    s1_200_data = ((ep1_200.get_data() +
                        en1_200.get_data() +
                        fp1_200.get_data() +
                        fn1_200.get_data()) / 4)

    s1_200 = mne.Epochs(emojis, ep1_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    s1_200._data = s1_200_data
    s1_200.save(op.join(ep_dir, 's1_200_whole-epo.fif'), overwrite=True)

    f20_s1_200_data = ((ep1_200.get_data()[0:20] +
                        en1_200.get_data()[0:20] +
                        fp1_200.get_data()[0:20] +
                        fn1_200.get_data()[0:20]) / 4)

    f20_s1_200 = mne.Epochs(emojis, ep1_evs[0:20], tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    f20_s1_200._data = f20_s1_200_data
    f20_s1_200.save(op.join(ep_dir, 'f20_s1_200-epo.fif'), overwrite=True)

    l20_s1_200_data = ((ep1_200.get_data()[-20:] +
                        en1_200.get_data()[-20:] +
                        fp1_200.get_data()[-20:] +
                        fn1_200.get_data()[-20:]) / 4)

    l20_s1_200 = mne.Epochs(emojis, ep1_evs[-20:], tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    l20_s1_200._data = l20_s1_200_data
    l20_s1_200.save(op.join(ep_dir, 'l20_s1_200-epo.fif'), overwrite=True)

    s1_400_data = ((ep1_400.get_data() +
                        en1_400.get_data() +
                        fp1_400.get_data() +
                        fn1_400.get_data()) / 4)

    s1_400 = mne.Epochs(emojis, ep1_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    s1_400._data = s1_400_data
    s1_400.save(op.join(ep_dir, 's1_400_whole-epo.fif'), overwrite=True)

    f20_s1_400_data = ((ep1_400.get_data()[0:20] +
                        en1_400.get_data()[0:20] +
                        fp1_400.get_data()[0:20] +
                        fn1_400.get_data()[0:20]) / 4)

    f20_s1_400 = mne.Epochs(emojis, ep1_evs[0:20], tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    f20_s1_400._data = f20_s1_400_data
    f20_s1_400.save(op.join(ep_dir, 'f20_s1_400-epo.fif'), overwrite=True)

    l20_s1_400_data = ((ep1_400.get_data()[-20:] +
                        en1_400.get_data()[-20:] +
                        fp1_400.get_data()[-20:] +
                        fn1_400.get_data()[-20:]) / 4)

    l20_s1_400 = mne.Epochs(emojis, ep1_evs[-20:], tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    l20_s1_400._data = l20_s1_400_data
    l20_s1_400.save(op.join(ep_dir, 'l20_s1_400-epo.fif'), overwrite=True)

    ### s02

    fn2_evs = [x for x in f_ev if x[2] - 1122 == 0]
    fp2_evs = [x for x in f_ev if x[2] - 1112 == 0]
    en2_evs = [x for x in e_ev if x[2] - 1212 == 0]
    ep2_evs = [x for x in e_ev if x[2] - 1222 == 0]

    ep2 = mne.Epochs(emojis, ep2_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    en2 = mne.Epochs(emojis, en2_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    fp2 = mne.Epochs(faces, fp2_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    fn2 = mne.Epochs(faces, fn2_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')

    ep2_100 = mne.Epochs(emojis, ep2_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    en2_100 = mne.Epochs(emojis, en2_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    fp2_100 = mne.Epochs(faces, fp2_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    fn2_100 = mne.Epochs(faces, fn2_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')

    ep2_200 = mne.Epochs(emojis, ep2_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    en2_200 = mne.Epochs(emojis, en2_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    fp2_200 = mne.Epochs(faces, fp2_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    fn2_200 = mne.Epochs(faces, fn2_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')

    ep2_400 = mne.Epochs(emojis, ep2_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    en2_400 = mne.Epochs(emojis, en2_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    fp2_400 = mne.Epochs(faces, fp2_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    fn2_400 = mne.Epochs(faces, fn2_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')

    s2_data = ((ep2.get_data() +
                en2.get_data() +
                fp2.get_data() +
                fn2.get_data()) / 4)

    s2 = mne.Epochs(emojis, ep2_evs, tmin=-0.1, tmax=0.75, baseline=None, picks='meg')
    s2._data = s2_data
    s2.save(op.join(ep_dir, 's2_entire-epo.fif'), overwrite=True)

    f20_s2_data = ((ep2.get_data()[0:20] +
                    en2.get_data()[0:20] +
                    fp2.get_data()[0:20] +
                    fn2.get_data()[0:20]) / 4)

    f20_s2 = mne.Epochs(emojis, ep2_evs[0:20], tmin=-0.1, tmax=0.75,
                        baseline=None, picks='meg')
    f20_s2._data = f20_s2_data
    f20_s2.save(op.join(ep_dir, 'f20_s2_entire-epo.fif'),
                overwrite=True)

    l20_s2_data = ((ep2.get_data()[-20:] +
                    en2.get_data()[-20:] +
                    fp2.get_data()[-20:] +
                    fn2.get_data()[-20:]) / 4)

    l20_s2 = mne.Epochs(emojis, ep2_evs[-20:], tmin=-0.1, tmax=0.75,
                        baseline=None, picks='meg')
    l20_s2._data = l20_s2_data
    l20_s2.save(op.join(ep_dir, 'l20_s2_entire-epo.fif'),
                overwrite=True)

    s2_100_data = ((ep2_100.get_data() +
                        en2_100.get_data() +
                        fp2_100.get_data() +
                        fn2_100.get_data()) / 4)

    s2_100 = mne.Epochs(emojis, ep2_evs, tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    s2_100._data = s2_100_data
    s2_100.save(op.join(ep_dir, 's2_100_whole-epo.fif'), overwrite=True)

    f20_s2_100_data = ((ep2_100.get_data()[0:20] +
                        en2_100.get_data()[0:20] +
                        fp2_100.get_data()[0:20] +
                        fn2_100.get_data()[0:20]) / 4)

    f20_s2_100 = mne.Epochs(emojis, ep2_evs[0:20], tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    f20_s2_100._data = f20_s2_100_data
    f20_s2_100.save(op.join(ep_dir, 'f20_s2_100_whole-epo.fif'), overwrite=True)

    l20_s2_100_data = ((ep2_100.get_data()[-20:] +
                        en2_100.get_data()[-20:] +
                        fp2_100.get_data()[-20:] +
                        fn2_100.get_data()[-20:]) / 4)

    l20_s2_100 = mne.Epochs(emojis, ep2_evs[-20:], tmin=0.05, tmax=0.15, baseline=None, picks='meg')
    l20_s2_100._data = l20_s2_100_data
    l20_s2_100.save(op.join(ep_dir, 'l20_s2_100_whole-epo.fif'), overwrite=True)

    s2_200_data = ((ep2_200.get_data() +
                        en2_200.get_data() +
                        fp2_200.get_data() +
                        fn2_200.get_data()) / 4)

    s2_200 = mne.Epochs(emojis, ep2_evs, tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    s2_200._data = s2_200_data
    s2_200.save(op.join(ep_dir, 's2_200_whole-epo.fif'), overwrite=True)

    f20_s2_200_data = ((ep2_200.get_data()[0:20] +
                        en2_200.get_data()[0:20] +
                        fp2_200.get_data()[0:20] +
                        fn2_200.get_data()[0:20]) / 4)

    f20_s2_200 = mne.Epochs(emojis, ep2_evs[0:20], tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    f20_s2_200._data = f20_s2_200_data
    f20_s2_200.save(op.join(ep_dir, 'f20_s2_200-epo.fif'), overwrite=True)

    l20_s2_200_data = ((ep2_200.get_data()[-20:] +
                        en2_200.get_data()[-20:] +
                        fp2_200.get_data()[-20:] +
                        fn2_200.get_data()[-20:]) / 4)

    l20_s2_200 = mne.Epochs(emojis, ep2_evs[-20:], tmin=0.15, tmax=0.3, baseline=None, picks='meg')
    l20_s2_200._data = l20_s2_200_data
    l20_s2_200.save(op.join(ep_dir, 'l20_s2_200-epo.fif'), overwrite=True)

    s2_400_data = ((ep2_400.get_data() +
                        en2_400.get_data() +
                        fp2_400.get_data() +
                        fn2_400.get_data()) / 4)

    s2_400 = mne.Epochs(emojis, ep2_evs, tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    s2_400._data = s2_400_data
    s2_400.save(op.join(ep_dir, 's2_400_whole-epo.fif'), overwrite=True)

    f20_s2_400_data = ((ep2_400.get_data()[0:20] +
                        en2_400.get_data()[0:20] +
                        fp2_400.get_data()[0:20] +
                        fn2_400.get_data()[0:20]) / 4)

    f20_s2_400 = mne.Epochs(emojis, ep2_evs[0:20], tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    f20_s2_400._data = f20_s2_400_data
    f20_s2_400.save(op.join(ep_dir, 'f20_s2_400-epo.fif'), overwrite=True)

    l20_s2_400_data = ((ep2_400.get_data()[-20:] +
                        en2_400.get_data()[-20:] +
                        fp2_400.get_data()[-20:] +
                        fn2_400.get_data()[-20:]) / 4)

    l20_s2_400 = mne.Epochs(emojis, ep2_evs[-20:], tmin=0.4, tmax=0.5, baseline=None, picks='meg')
    l20_s2_400._data = l20_s2_400_data
    l20_s2_400.save(op.join(ep_dir, 'l20_s2_400-epo.fif'), overwrite=True)

    ### gfp plots

    s1_ave_gfps = []
    for s in s1_100_data:
        gfps = []
        tnps = s.T
        for t in tnps:
            gfp = t.std()
            gfps.append(gfp)
        gfps = np.array(gfps)
        final1 = gfps.mean()
        s1_ave_gfps.append(final1)

    s2_ave_gfps = []
    for s in s2_100_data:
        gfps2 = []
        tnps2 = s.T
        for t in tnps2:
            gfp = t.std()
            gfps2.append(gfp)
        gfps2 = np.array(gfps2)
        final2 = gfps2.mean()
        s2_ave_gfps.append(final2)

    fig, axes = plt.subplots()
    s01, = axes.plot(s1_ave_gfps, color='dodgerblue', label='Syl 1 GFP')
    s02, = axes.plot(s2_ave_gfps, color='limegreen', label='Syl 2 GFP')
    axes.legend(handles=[s01, s02])
    axes.set_xlabel('Epochs')
    axes.set_ylabel('Average GFP from 50 - 150 ms')
    fig.savefig(op.join(pic_dir, 's01_s02_avg_gfp_over_epochs.png'))
    plt.close()

    s1_400_ave_gfps = []
    for s in s1_400_data:
        gfps = []
        tnps = s.T
        for t in tnps:
            gfp = t.std()
            gfps.append(gfp)
        gfps = np.array(gfps)
        final1 = gfps.mean()
        s1_400_ave_gfps.append(final1)

    s2_400_ave_gfps = []
    for s in s2_400_data:
        gfps2 = []
        tnps2 = s.T
        for t in tnps2:
            gfp = t.std()
            gfps2.append(gfp)
        gfps2 = np.array(gfps2)
        final2 = gfps2.mean()
        s2_400_ave_gfps.append(final2)

    fig, axes = plt.subplots()
    s01, = axes.plot(s1_400_ave_gfps, color='dodgerblue', label='Syl 1 GFP')
    s02, = axes.plot(s2_400_ave_gfps, color='limegreen', label='Syl 2 GFP')
    axes.legend(handles=[s01, s02])
    axes.set_xlabel('Epochs')
    axes.set_ylabel('Average GFP from 400 - 400 ms')
    fig.savefig(op.join(pic_dir, 's01_s02_400ms_avg_gfp_over_epochs.eps'))
    fig.savefig(op.join(pic_dir, 's01_s02_400ms_avg_gfp_over_epochs.png'))
    plt.close()

    ### plot topos

    for syl, time, win in zip(syls, times, windows):
        topo_dir = op.join(pic_dir, 'topo')
        plot_save = op.join(topo_dir, f'{syl}_{time}_{win}_topo.png')

        ep_name = f'{win}_{syl}_{time}'


