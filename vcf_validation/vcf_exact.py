#!/usr/bin/env python

# reads vcf and checks line-by-line to see if content is the same.  quite crude.

import sys
from gzip import gzip


def open_vcf(vcf_fn):
    if vcf_fn[-3:] == '.gz':
        return gzip.open(vcf_fn, 'rb')
    else:
        return open(vcf_fn)


vcf1 = open_vcf(sys.argv[1])
vcf2 = open_vcf(sys.argv[2])

for v1 in vcf1:
    v2 = next(vcf2)
    if v1 != v2:
        sys.stderr.write(v1.rstrip('\n') + '\t' + v2)
vcf1.close()
vcf2.close()
