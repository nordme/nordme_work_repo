# -*- coding: utf-8 -*-


for si, subj in enumerate(params.subjects):
    if op.exists(op.join(params.work_dir, subj, 'raw_fif')):
        prebad_file = op.join(params.work_dir, subj,
                              'raw_fif', '%s_prebad.txt' % subj)
        if not op.exists(prebad_file):
            assert len(bad_channels) == len(params.subjects)
            if bad_channels[si] is None:
                with open(prebad_file, 'w') as f:
                    f.write("")
            else:
                with open(prebad_file, 'w') as output:
                    for ch_name in bad_channels[si]:
                        output.write("%s\n" % ch_name)