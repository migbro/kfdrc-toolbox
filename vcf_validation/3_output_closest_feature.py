#!/usr/bin/env python3
# use a-not-in-b bed files from vcf compare to look for closest features in b for near-matched hits

import sys
import os
import subprocess

bedtools = sys.argv[1]
comp_list = sys.argv[2]
passed_list = sys.argv[3]

# tools = ['VARDICT', 'STRELKA', 'MUTECT2', 'LANCET']

for fn in open(comp_list):
    fn = fn.rstrip('\n')
    fn_half = os.path.basename(fn).split('_vs_')
    # fn_parts_a = fn_half[0].split('_')
    # fn_parts_b = fn_half[1].split('_')
    for fn2 in open(passed_list):
        fn2 = fn2.rstrip('\n')
        fn2_root = os.path.basename(fn2).split('.')
        if fn2_root[0] != fn_half[0]:
            cmd = bedtools + ' closest -a ' + fn + ' -b ' + fn2 + ' -d | sort -nk25 | cut -f 1-7,13-19,25 > ' + fn_half[0] + '_' + fn2_root[0] + '.closest.bed'
            sys.stderr.write(cmd + '\n')
            subprocess.call(cmd, shell=True)


