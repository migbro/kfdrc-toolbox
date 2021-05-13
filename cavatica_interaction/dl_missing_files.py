"""
Download missing files using a cavativa manifest and a dir of existing file
"""
import sevenbridges as sbg
from sevenbridges.errors import SbgError
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import sys
import re
import concurrent.futures
import os
import pdb
config = sbg.Config(profile='turbo')
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])

def check_dl_file(entry):
    try:
        info = entry.rstrip('\n').split(',')
        path = dir + info[1]
        if not os.path.isfile(path):
            getme = api.files.get(info[0])
            getme.download(path)
    except Exception as e:
        sys.stderr.write(str(e) + "\n")
        sys.stderr.write("Got an error downloading " + info[1] + "\n")

dir = sys.argv[1] + "/"
manifest = open(sys.argv[2])
head = next(manifest)
i = 1
n = 100

with concurrent.futures.ThreadPoolExecutor(8) as executor:
    results = {executor.submit(check_dl_file, line): line for line in manifest}
    for result in concurrent.futures.as_completed(results):
        if i % n == 0:
            sys.stderr.write(str(i) + ' Files downloaded\n')
        i += 1

# for line in manifest:
#     check_dl_file(line)