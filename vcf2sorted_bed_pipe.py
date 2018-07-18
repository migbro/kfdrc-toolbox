#!/usr/bin/env python3
# written by mbrown 2018-Jul-18
# convert vcfs to sorted bed for use with bedtools

import sys
import os
import subprocess

bedops_vcf2bed = sys.argv[1]
flist = sys.argv[2]

export_path = 'export PATH=$PATH:' + os.path.dirname(bedops_vcf2bed)
subprocess.call(export_path, shell=True)

for fn in open(flist):
    fn = fn.rstrip('\n')
    fn_parts = os.path.basename(fn).split('.')
    cmd = 'cat ' + fn + ' | ' + bedops_vcf2bed + ' > ' + fn_parts[0] + '.sorted.bed'
    if fn_parts[-1] == 'gz':
        cmd = 'zcat ' + fn + ' | ' + bedops_vcf2bed + ' > ' + fn_parts[0] + '.sorted.bed'
    subprocess.call(cmd, shell=True)
