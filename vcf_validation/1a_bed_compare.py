#!/usr/bin/env python
# same as vcf compare, except for bed input

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
        bed1 = file_list[i]
        bed1_root = os.path.basename(os.path.splitext(bed1)[0])[:-4]
        bed2 = file_list[k]
        bed2_root = os.path.basename(os.path.splitext(bed2)[0])[:-4]
        super_root = bed1_root + '_vs_' + bed2_root
        cmd = bedtools + ' intersect -a ' + bed1 + ' -b ' + bed2 \
              + ' -v -header 2> ' + super_root + '.errs > ' + super_root + '.bed'
        sys.stderr.write(cmd + '\n')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True)
        super_root = bed2_root + '_vs_' + bed1_root
        cmd = bedtools + ' intersect -a ' + bed2 + ' -b ' + bed1 \
              + ' -v -header 2> ' + super_root + '.errs > ' + super_root + '.bed'
        sys.stderr.write(cmd + '\n')
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=None,
                         stderr=None, close_fds=True)
    j += 1

