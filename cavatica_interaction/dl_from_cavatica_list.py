#!/usr/bin/env python

import sevenbridges as sbg
import sys
config = sbg.Config(profile='cavatica')
api = sbg.Api(config=config)

project = sys.argv[1]
flist = []
with open(sys.argv[2]) as f:
    flist = f.read().splitlines()
sys.stderr.write('Getting files for project ' + project + '\n')
files = api.files.query(project=project, names=flist).all()

for fn in files:
    sys.stderr.write('Downloading file ' + fn.name + '\n')
    dl = fn.download(path=fn.name, wait=True)
