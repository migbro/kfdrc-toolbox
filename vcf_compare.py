#!/usr/bin/env python

import sys
import os
import subprocess

bedtools = sys.argv[1]
vcf_manifest = sys.argv[2]

vcf_list = []
for line in open(vcf_manifest):
    vcf_list.append(line.rstrip('\n'))
    # print (line)
j = 1

for i in range(len(vcf_list) - 1):
    for k in range(j, len(vcf_list), 1):
        # sys.stdout.write(vcf_list[i] + ' vs ' + vcf_list[k] + '\n')
        vcf1 = vcf_list[i]
        vcf1_root = os.path.basename(os.path.splitext(vcf1)[0])
        vcf2 = vcf_list[k]
        vcf2_root = os.path.basename(os.path.splitext(vcf2)[0])
        cmd = bedtools + ' intersect -a ' + vcf1 + ' -b ' + vcf2 \
              + ' -v -sorted > ' + vcf1_root + '_vs_' + vcf2_root + '.vcf'
        sys.stderr.write(cmd + '\n')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True)

        cmd = bedtools + ' intersect -a ' + vcf2 + ' -b ' + vcf1 \
              + ' -v -sorted > ' + vcf2_root + '_vs_' + vcf1_root + '.vcf'
        sys.stderr.write(cmd + '\n')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True)
    j += 1

