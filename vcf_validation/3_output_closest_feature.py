#!/usr/bin/env python3
# use a-not-in-b bed files from vcf compare to look for closest features in b for near-matched hits

import sys
import os
import subprocess

bedtools = sys.argv[1]
comp_list = sys.argv[2]
passed_list = sys.argv[3]

# tools = ['VARDICT', 'STRELKA', 'MUTECT2', 'LANCET']
passed_attr = {}
for fn in open(passed_list):
    fn = fn.rstrip('\n')
    fn_parts = os.path.basename(fn).split('.')
    fn_parts2 = fn_parts[0].split('_')
    tool = fn_parts2[1]
    passed_attr[tool] = {}
    passed_attr[tool]['fn_root'] = fn_parts[0]
    passed_attr[tool]['path'] = fn


for fn in open(comp_list):
    fn = fn.rstrip('\n')
    fn_half = os.path.basename(fn).split('_vs_')
    fn_parts_a = fn_half[0].split('_')
    fn_parts_b = fn_half[1].split('_')
    tool = fn_parts_b[1]
    tool = tool.replace('.bed', '')
    cmd = bedtools + ' closest -a ' + fn + ' -b ' + passed_attr[tool]['path'] \
          + ' -d | sort -nk25 | cut -f 1-7,13-19,25 > ' + fn_half[0] + '_' + passed_attr[tool]['fn_root'] \
          + '.closest.bed'
    sys.stderr.write(cmd + '\n')
    subprocess.call(cmd, shell=True)


