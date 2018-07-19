#!/usr/bin/env python
# check output from closest feature after running vcf compare without -v flag for mismatched variant calls

import sys

for fn in open(sys.argv[1]):
    fn = fn.rstrip('\n')
    for line in open(fn):
        data = line.split('\t')
        if data[5] != data[12] or data[6] != data[13]:
            line = line.rstrip('\n')
            sys.stdout.write(line + '\t' + fn + '\n')
