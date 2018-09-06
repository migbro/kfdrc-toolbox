#!/usr/bin/env python3

import sys

rn_tbl = open(sys.argv[1])

head = next(rn_tbl)
prefix = sys.argv[4]
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
maf_out = open(prefix + '.strelka.vep.filtered.maf', 'w')


maf_out.write(head)
for line in maf:
    data = line.split('\t')
    data[14] = samp_ind[data[14]]
    data[15] = samp_ind[data[15]]
    maf_out.write('\t'.join(data))
maf_out.close()
cnv = open(sys.argv[3])
cnv_out = open(prefix + '.predicted_cnv.txt', 'w')
head = next(cnv)

h_list = head.rstrip('\n').split('\t')
cnv_out.write(h_list[0] + '\t' + h_list[1])
for i in range(2, len(h_list), 1):
    cnv_out.write('\t' + samp_ind[h_list[i]])
cnv_out.write('\n')

for line in cnv:
    cnv_out.write(line)
cnv_out.close()
