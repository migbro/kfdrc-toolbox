#!/usr/bin/env python3

import sys
import os

blacklist = {}
for entry in open(sys.argv[1]):
    blacklist[entry.rstrip('\n')] = 0

maf_list = open(sys.argv[2])
fcol = int(sys.argv[3])
for maf in maf_list:
    maf = maf.rstrip('\n')
    cur = open(maf)
    new_fn = os.path.basename(maf)[-4:] + 'filtered.maf'
    new = open(new_fn, 'w')
    head = next(cur)
    new.write(head)
    head = next(cur)
    new.write(head)
    head = head.rstrip('\n').split('\t')
    sys.stderr.write('Filtering file ' + maf + ' on field ' + head[fcol] + ' to file ' + new_fn + '\n')
    for entry in cur:
        info = entry.rstrip('\n').split('\t')
        if info[fcol] not in blacklist:
            new.write(entry)
    cur.close()
    new.close()

maf_list.close()
