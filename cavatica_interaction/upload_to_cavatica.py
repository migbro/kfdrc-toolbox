#!/usr/bin/env python

import sevenbridges as sbg
import sys
config = sbg.Config(profile='cavatica')
api = sbg.Api(config=config)

project = sys.argv[1]
with open(sys.argv[2]) as f:
    flist = f.read().splitlines()
sys.stderr.write('Getting files for project ' + project + '\n')
# files = api.files.query(project=project, names=flist)

for fn in flist:
    sys.stderr.write('Uploading file/dir ' + fn + '\n')
    up = api.files.upload(fn, project, fn)
