#!/usr/bin/env python3

import sys

rn_tbl = open(sys.argv[1])

head = next(rn_tbl)

samp_ind = {}
for line in rn_tbl:
    info = line.rstrip('\n').split('\t')
    tum_bs = info[4].split(',')
    tum_ext = info[5].split(',')
    for i in range(0, len(tum_bs), 1):
        samp_ind[tum_bs[i]] = tum_ext[i]
    norm_bs = info[11].split(',')
    norm_ext = info[12].split(',')
    for i in range(0, len(norm_bs), 1):
        samp_ind[norm_bs[i]] = norm_ext[i]

rn_tbl.close()

maf = open(sys.argv[2])
head = next(maf)

sys.stdout.write(head)
for line in maf:
    data = line.split('\t')
    data[14] = samp_ind[data[14]]
    data[15] = samp_ind[data[15]]
    sys.stdout.write('\t'.join(data))

cnv = open(sys.argv[3])
prefix = sys.argv[4]
head = next(cnv)