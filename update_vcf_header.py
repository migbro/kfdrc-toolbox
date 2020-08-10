#!/usr/bin/env python3

import argparse
from pysam import VariantFile
import os
import sys
import concurrent.futures
import pdb


parser = argparse.ArgumentParser(description='Update errant vcf header using a correct file, and table. Use with xargs')
parser.add_argument('-i', '--input_vcf', action='store', dest='in_vcf', help='Input vcf to fix')
parser.add_argument('-t', '--table', action='store', dest='table', help='Update table with vcf header category and keys to update')
parser.add_argument('-e', '--example', action='store', dest='ex_vcf', help='Example vcf with good headers')
parser.add_argument('-o', '--output-dir', action='store', dest='out_dir', help='Output directory to put updated files')


# def mt_file_process(fname):
#     try:
#         cpath = fname.rstrip('\n')
#         sys.stderr.write("Processing " + cpath + "\n")
#         sys.stderr.flush()
#         cname = os.path.basename(cpath)
#         in_vcf = VariantFile(cpath)
#         # pdb.set_trace()
#         for cat in tbl_dict:
#             for key in tbl_dict[cat]:
#                 getattr(in_vcf.header, cat)[key].remove_header()
#                 in_vcf.header.add_meta(cat_dict[cat], items=[('ID',key), ('Number',getattr(good_boy.header, cat)[key].number),
#                 ('Type',getattr(good_boy.header, cat)[key].type), ('Description',getattr(good_boy.header, cat)[key].description)])
#         # pdb.set_trace()
#         out_fn = args.out_dir + "/" + cname
#         out_vcf = VariantFile(out_fn, 'w', header=in_vcf.header)
#         for rec in in_vcf.fetch():
#             out_vcf.write(rec)
#         out_vcf.close()
#     except Exception as e:
#         sys.stderr.write(str(e) + "\n failed to process " + cpath + "\n")


def file_process(fname):
    try:
        cpath = fname.rstrip('\n')
        sys.stderr.write("Processing " + cpath + "\n")
        sys.stderr.flush()
        in_vcf = VariantFile(cpath)
        # pdb.set_trace()
        for cat in tbl_dict:
            for key in tbl_dict[cat]:
                getattr(in_vcf.header, cat)[key].remove_header()
                in_vcf.header.add_meta(cat_dict[cat], items=[('ID',key), ('Number',getattr(good_boy.header, cat)[key].number),
                ('Type',getattr(good_boy.header, cat)[key].type), ('Description',getattr(good_boy.header, cat)[key].description)])
        # pdb.set_trace()
        out_vcf = VariantFile("-", 'w', header=in_vcf.header)
        for rec in in_vcf.fetch():
            out_vcf.write(rec)
        out_vcf.close()
    except Exception as e:
        sys.stderr.write(str(e) + "\n failed to process " + cpath + "\n")


if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
# pdb.set_trace()

tbl_dict = {}
cat_dict = {'info': 'INFO', 'formats': 'FORMAT'}
for line in open(args.table):
    (cat, key) = line.rstrip('\n').split('\t')
    if cat not in tbl_dict:
        tbl_dict[cat] = []
    tbl_dict[cat].append(key)


good_boy = VariantFile(args.ex_vcf)
file_process(args.in_vcf)
# with open(args.in_vcf) as f:
#     vcf_list = f.read().splitlines()
#     if len(vcf_list[-1]) < 5:
#         vcf_list.pop()

# with concurrent.futures.ThreadPoolExecutor(32) as executor:
#     results = {executor.submit(mt_file_process, fpath): fpath for fpath in vcf_list}
good_boy.close()