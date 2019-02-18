#!/usr/bin/env python3

import sevenbridges as sbg
import argparse
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import sys
import concurrent.futures


parser = argparse.ArgumentParser(description='Script to summarize peddy outputs.')
parser.add_argument('-i', '--id_list', action='store', dest='id_list', help='cavatica file id list')
parser.add_argument('-p', '--profile', action='store', dest='profile', help='cavatica profile name')
parser.add_argument('-t', '--threads', action='store', dest='threads', help='num threads')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

config = sbg.Config(profile=args.profile)
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])


def get_files(api, file_id):
    try:
        file_obj = api.files.get(id=file_id)
        file_obj.download(path=file_obj.name, wait=True)
    except Exception as e:
        print(e)
        print ('Could not download file with id ' + file_id + '\n')
        sys.exit()


with open(args.id_list) as f:
    id_list = f.read().splitlines()

for id_value in id_list:
    sys.stderr.write('Downloading file ' + id_value + '\n')
    get_files(api, id_value)

with concurrent.futures.ProcessPoolExecutor(int(args.threads)) as executor:
    results = {executor.submit(get_files, api, id_value): id_value for id_value in id_list}
