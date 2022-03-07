"""
Quick script from Bo Zhang and modifed by Miguel Brown to get files and their sizes from
cavatica projects that are not in external buckets. Useful for estimating
cost of storage hits against billing group for a project
"""
import sevenbridges as sbg
from sevenbridges.errors import SbgError
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import argparse
import sys
import pdb


parser = argparse.ArgumentParser()
parser.add_argument("--project", required=True)
parser.add_argument("--profile", required=True)
args = parser.parse_args()

c = sbg.Config(profile=args.profile)
api = sbg.Api(config=c, error_handlers=[rate_limit_sleeper, maintenance_sleeper])


def iterate_folder(folder_obj):
    """
    Folders are funky in this api - there is no .all(). Need to iterate if more than 50 files in folder
    """
    # Need this array as a proper bookmark of sorts to ensure you make it to the next page
    sys.stderr.write('Found dir ' + folder_obj.name + ', drilling down\n')
    folder_list = []
    j = 0
    folder_list.append(folder_obj.list_files())
    total = folder_obj.list_files().total
    i = len(folder_list[j])
    for obj in folder_list[j]:
        if obj.is_folder():
            iterate_folder(obj)
        else:
            check_file(obj)
    while i < (total - 1):
        folder_list.append(folder_list[j].next_page())
        j += 1
        for obj in folder_list[j]:
            if obj.is_folder():
                iterate_folder(obj)
            else:
                check_file(obj)
        i += len(folder_list[j])

    for obj in folder_obj.list_files():
        i += 1
        if obj.is_folder():
            iterate_folder(obj)
        else:
            check_file(obj)


def check_file(file_obj):
    print(file_obj.id + "\t" + file_obj.name + "\t" + str(file_obj.size) + "\t" + str(file_obj.size/1073741824) + "\t" + file_obj.storage.type)
    # if file_obj.storage.volume is None:
    #     print(file_obj.id + "\t" + file_obj.name + "\t" + str(file_obj.size) + "\t" + str(file_obj.size/1073741824))
    # else:
    #     pdb.set_trace()
    #     hold=1


files = api.files.query(project=args.project).all()
print("File ID\tFile Name\tFile Size bytes\tFile Size GB\tStorage type")
for f in files:
    try:
        if f.is_folder():
            iterate_folder(f)
        else:
            check_file(f)
    except Exception as e:
        sys.stderr.write("Ran into error processing " + f.name + " with error: " + str(e) + "\n")
        exit(1)
