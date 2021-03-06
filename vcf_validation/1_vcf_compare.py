#!/usr/bin/env python

import sys
import os
import subprocess

bedtools = sys.argv[1]
file_manifest = sys.argv[2]

file_list = []
for line in open(file_manifest):
    file_list.append(line.rstrip('\n'))
    # print (line)
j = 1

for i in range(len(file_list) - 1):
    for k in range(j, len(file_list), 1):
        # sys.stdout.write(vcf_list[i] + ' vs ' + vcf_list[k] + '\n')
        vcf1 = file_list[i]
        vcf1_root = os.path.basename(os.path.splitext(vcf1)[0])[:-4]
        vcf2 = file_list[k]
        vcf2_root = os.path.basename(os.path.splitext(vcf2)[0])[:-4]
        super_root = vcf1_root + '_vs_' + vcf2_root
        cmd = bedtools + ' intersect -a ' + vcf1 + ' -b ' + vcf2 \
              + ' -v -header 2> ' + super_root + '.errs | gzip -c > ' + super_root + '.vcf.gz'
        sys.stderr.write(cmd + '\n')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True)
        super_root = vcf2_root + '_vs_' + vcf1_root
        cmd = bedtools + ' intersect -a ' + vcf2 + ' -b ' + vcf1 \
              + ' -v -header 2> ' + super_root + '.errs | gzip -c > ' + super_root + '.vcf.gz'
        sys.stderr.write(cmd + '\n')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True)
    j += 1

