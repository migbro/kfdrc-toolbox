import argparse
import gzip
import os

parser = argparse.ArgumentParser()
parser.add_argument('--example_vcf',
                    help='VCF file with desired contig headers')
parser.add_argument('--input_vcf',
                    help='VCF with contig headers to replace')

args = parser.parse_args()

e_vcf = gzip.open(args.example_vcf, "rb")
in_vcf = gzip.open(args.input_vcf, "rb")
out_fn = os.path.splitext(os.path.basename(args.input_vcf))[0]
out_vcf = open(out_fn, 'w')

contigs = []
for line in e_vcf:
    line = line.decode()
    if line.startswith("#CHROM"):
        break
    elif line.startswith("##contig"):
        contigs.append(line)
new_head = []
flag = 0
for line in in_vcf:
    line = line.decode()
    if line.startswith("##contig"):
        if flag == 0:
            new_head.extend(contigs)
            flag = 1
    else:
        new_head.append(line)
        if line.startswith("#CHROM"):
            break
out_vcf.write("".join(new_head))
for line in in_vcf:
    line = line.decode()
    out_vcf.write(line)
out_vcf.close()
