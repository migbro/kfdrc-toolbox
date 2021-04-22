import argparse
import sys
import concurrent.futures
import re


parser = argparse.ArgumentParser(description='Run a subset of drafted tasks at all times.'
                                             'Use in conjunction with cron tab')
parser.add_argument('-i', '--header', action='store', dest='header', help='maf header')
parser.add_argument('-d', '--dir', action='store', dest='dir', help='file input dir')
parser.add_argument('-m', '--manifest', action='store', dest='manifest', help='cavatica manifest')
# parser.add_argument('-f', '--flag', action='store_true', dest='flag', help='flag to edit sample names to shorter style for TCGA')
parser.add_argument('-c', '--caller', action='store', dest='caller', help='Set as ALL to process all, or enter caller name')
parser.add_argument('-o', '--out', action='store', dest='flag', help='output file name')


# def process_rename(file_handle, t_idx, n_idx):
#     entry = next(file_handle)
#     data = entry.rstrip('\n').split('\t')
#     data[t_idx] = "data[t_idx].split("_")

def process_norm(file_handle):
    entry = next(file_handle)
    return entry


def process_maf(file_name):
    file_handle = open(file_name)
    sys.stderr.write("Processing " + file_name + "\n")
    skip = next(file_handle)
    skip = next(file_handle)
    # if args.flag:
    with concurrent.futures.ThreadPoolExecutor(40) as executor:
        results = {executor.submit(process_norm, data): data for data in file_handle}
        for result in concurrent.futures.as_completed(results):
            if result.result() is not None:
                out.write(result.result())
    sys.stderr.write("Completed processing file\n")



if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

head = open(args.header)
header = []
out = open(args.out, "w")
for line in head:
    header.append(line)

out.write("".join(header))
manifest = open(args.manifest)
mhead = next(manifest)
# only needed if flag set, for TCGA processing
# if args.flag:
#     cols = header[1].rstrip('\n').split('\t')
#     t_idx = cols.index("Tumor_Sample_Barcode")
#     n_idx = cols.idx("Matched_Norm_Sample_Barcode")
for line in manifest:
    info = line.rstrip('\n').split(',')
    if args.caller == "ALL" or re.search(args.caller, info[1]):
        current = args.dir + "/" + info[1]
        process_maf(current)
out.close()