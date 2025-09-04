"""Recursively download a directory from Cavatica to a local path."""
import argparse
import sys
from pathlib import Path
from time import sleep

import sevenbridges as sbg
from sevenbridges.http.error_handlers import maintenance_sleeper, rate_limit_sleeper


def recursive_download(api: sbg.Api, file_id: str, path: Path) -> None:
    """Recursively download a directory from Cavatica to a local path.

    Will make local directories as needed, and download files to match the tree structure

    Args:
        api (sbg.Api): An authenticated Cavatica API object
        file_id (str): The ID of the file or folder to download
        path (Path): The local path to download to, based on the remote structure

    """
    file_obj = api.files.get(id=file_id)
    if file_obj.is_folder():
        path = path / Path(file_obj.name)
        path.mkdir(parents=True, exist_ok=True)
        print(f"Downloading from dir {path}", file=sys.stderr)
        for item in api.files.query(parent=file_obj).all():
            recursive_download(api, item.id, path)
    else:
        print(f"Downloading {file_obj.name}", file=sys.stderr)
        dl = file_obj.download(path=str(path / file_obj.name), wait=False)
        dl.start()
        while dl.status != "COMPLETED":
            print(f"  {dl.status}, {dl.progress} completed, {dl.duration} elapsed", file=sys.stderr)
            sleep(1)
        print(f"{dl.status}", file=sys.stderr)

parser = argparse.ArgumentParser(
    description="Run a subset of drafted tasks at all times.Use in conjunction with cron tab"
)
parser.add_argument("-p", "--profile", action="store", dest="profile", help="cavatica profile name")
parser.add_argument(
    "-f", "--folder_id", action="store", dest="folder_id",
    help="ID of folder to recursively download from",
)

args = parser.parse_args()

config = sbg.Config(profile=args.profile)
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])
recursive_download(api, args.folder_id, Path("./"))
