import sevenbridges as sbg
import argparse
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
from pathlib import Path
import pdb



parser = argparse.ArgumentParser(description='Run a subset of drafted tasks at all times.'
                                             'Use in conjunction with cron tab')
parser.add_argument('-p', '--profile', action='store', dest='profile', help='cavatica profile name')
parser.add_argument('-f', '--folder_id', action='store', dest='folder_id', help='ID of folder to recursively download from')


def recursive_download(api, file_id, path: Path):
    file_obj = api.files.get(id=file_id)
    if file_obj.is_folder():
        path = path / Path(file_obj.name)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Downloading from dir {file_obj.name}")
        for item in api.files.query(parent=file_obj):
            print(f"Recursively downloading {item.name}")
            recursive_download(api, item.id, path)
    else:
        file_obj.download(path=str(path/file_obj.name))


args = parser.parse_args()

config = sbg.Config(profile=args.profile)
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])
recursive_download(api, args.folder_id, Path('./'))

