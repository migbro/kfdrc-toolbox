#!/usr/bin/env python3

import sys
n = int(sys.argv[2])
for fn in open(sys.argv[1]):
    fn = fn.rstrip('\n')
    cur = open(fn)
    for line in cur:
        info = line.rstrip('\n').split('\t')
        if int(info[-1]) > n:
            cur.close()
            break
        else:
            sys.stdout.write(line)
