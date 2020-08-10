import argparse
import sys
import sevenbridges as sbg
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--files', action='store', dest='files', help='Cavatica-style tsv manifest with file ID, file name, and associated cwl input key', required=False)
parser.add_argument('-p', '--project', action='store', dest='project', help='Project to copy to', required=True, default="cavatica/apps-publisher")
parser.add_argument('-n', '--profile', action='store', dest='profile', help='Cavatica profile name', required=True, default="cavatica")

args = parser.parse_args()

config = sbg.Config(profile=args.profile)
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])

manifest = open(args.files)
head = next(manifest)
sys.stdout.write(head)

for line in manifest:
    # field one should be file ID, field two file name
    info = line.split('\t')
    # first check if file already exists in destination project
    files = api.files.query(project=args.project, names=[info[1]])
    if len(files) == 0:
        sys.stderr.write('File ' + info[1] + ' not in destination, copying\n')
        orig = api.files.get(info[0])
        cp_file = orig.copy(project=args.project)
        info[0] = cp_file.id
        sys.stdout.write("\t".join(info))
    else:
        sys.stderr.write('File ' + info[1] + ' already exists. Updating file ID using destination copy\n')
        info[0] = files[0].id
        sys.stdout.write("\t".join(info))