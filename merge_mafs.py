#!/usr/bin/env python3

import sys

with open(sys.argv[1]) as f:
    header = f.read()
dx_tbl = open(sys.argv[2])
task_dx_tbl = open(sys.argv[3])

dx_dict = {}
out_fh = {}
next(dx_tbl)
for line in dx_tbl:
    info = line.rstrip('\n').split('\t')
    cbttc_dx = info[0]
    cbio_short = info[1]
    dx_dict[cbttc_dx] = cbio_short
    out_fh[cbio_short] = open(cbio_short + '.strelka.vep.maf', 'w')
    out_fh[cbio_short].write(header)
dx_tbl.close()

next(task_dx_tbl)

suffix = '.strelka.vep.maf'

for line in task_dx_tbl:
    info = line.rstrip('\n').split('\t')
    task_name = info[10]
    task_id = info[11]
    n = 0
    dx_list = []
    # for all, in any dx, list which files to output to
    for i in range(7, 10, 1):
        if info[i] != '0':
            n += 1
            dx_list.append(dx_dict[info[i]])
    # open maf file and iterate through, printing to appropriate mafs
    cur_maf = open(task_id + suffix)
    next(cur_maf)
    next(cur_maf)
    for line in cur_maf:
        for dx in dx_list:
            out_fh[dx].write(line)
    cur_maf.close()
    sys.stderr.write(task_name + '\t' + str(n) + '\n')

task_dx_tbl.close()
