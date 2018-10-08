#!/usr/bin/env python3

import sys
import pdb
sel_list = open(sys.argv[1])
h_flag = sys.argv[2]
tbl = sys.argv[3]

sel_dict = {}

for line in sel_list:
    #pdb.set_trace()
    sel_dict[line.rstrip('\n')] = 0


t_fh = open(tbl)
if h_flag == 1:
    head = next(t_fh)
    sys.stdout.write(head)
for entry in t_fh:
    info = entry.rstrip('\n').split('\t')
    if info[0] in sel_dict:
        sys.stdout.write(entry)
        sel_dict[info[0]] = 1

for lbl in sel_dict:
    if sel_dict[lbl] == 0:
        sys.stderr.write(lbl + ' not in ' + sys.argv[1] + '\n')
