#!/usr/bin/env python

import sys
import os
import subprocess

peddy = sys.argv[1]

for line in open(sys.argv[2]):
    (pre_vcf, fam, post_id) = line.rstrip().split()
    pre_id = pre_vcf.split('.')[0]
    ped = fam + '.ped'
    post_vcf = post_id + '.postCGP.Gfiltered.deNovos.vcf.gz'
    os.mkdir(fam)
    os.chdir(fam)
    cmd = 'python -m ' + peddy + ' -p 4 --sites hg38 --prefix ' + fam + '_pre --plot ../' + pre_vcf + ' ../' + ped \
          + ' && python -m ' + peddy + ' -p 4 --sites hg38 --prefix ' + fam + '_post --plot ../' + post_vcf + ' ../' \
          + ped
    sys.stderr.write('Running peddy ' + cmd + '\n')
    subprocess.call(cmd, shell=True)
    os.chdir('../')
