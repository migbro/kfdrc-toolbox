#!/usr/bin/env python3

import sys

dx_tbl = open(sys.argv[1])
task_dx_tbl = open(sys.argv[2])

dx_dict = {}
out_fh = {}
next(dx_tbl)
for line in dx_tbl:
    info = line.rstrip('\n').split('\t')
    cbttc_dx = info[0]
    cbio_short = info[1]
    dx_dict[cbttc_dx] = cbio_short
    out_fh[cbio_short] = open(cbio_short + '.predicted_cnv.txt', 'w')
    out_fh[cbio_short].write('Hugo_Symbol\tEntrez_Gene_Id')
dx_tbl.close()

next(task_dx_tbl)

suffix = '.CNVs.Genes.copy_number'
cnv_dict = {}
s_dict = {}
for line in task_dx_tbl:
    info = line.rstrip('\n').split('\t')
    tum_bs_id = info[2]
    task_id = info[11]
    n = 0
    dx_list = {}
    # for all, in any dx, list which files to output to
    for i in range(7, 10, 1):
        if info[i] != '0' and info[i] not in dx_list:
            n += 1
            dx_list[dx_dict[info[i]]] = 0
    # open maf file and iterate through, printing to appropriate mafs
    cur_cnv = open(task_id + suffix)
    for dx in dx_list:
        if dx not in s_dict:
            s_dict[dx] = []
            cnv_dict[dx] = {}
        s_dict[dx].append(tum_bs_id)
    for cnv in cur_cnv:
        data = cnv.rstrip('\n').split('\t')
        gene = data[0] + '\t' + data[1]
        for dx in dx_list:
            if gene not in cnv_dict[dx]:
                cnv_dict[dx][gene] = {}
            cnv_dict[dx][gene][tum_bs_id] = data[2]
    cur_cnv.close()
    sys.stderr.write(tum_bs_id + '\t' + str(n) + '\t' + '\t'.join(dx_list) + '\n')

task_dx_tbl.close()
for dx in cnv_dict:
    out_fh[dx].write('\t' + '\t'.join(s_dict[dx]) + '\n')
    for gene in cnv_dict[dx]:
        out_fh[dx].write(gene)
        for samp in s_dict[dx]:
            if samp in cnv_dict[dx][gene]:
                out_fh[dx].write('\t' + cnv_dict[dx][gene][samp])
            else:
                out_fh[dx].write('\t0')
        out_fh[dx].write('\n')
