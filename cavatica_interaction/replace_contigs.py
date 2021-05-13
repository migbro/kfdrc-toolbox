import argparse
import pysam

parser = argparse.ArgumentParser()
parser.add_argument('--example_vcf',
                    help='VCF file with desired contig headers')
parser.add_argument('--input_vcf',
                    help='VCF with contig headers to replace')

args = parser.parse_args()

e_vcf = pysam.VariantFile(args.example_vcf, 'r')
in_vcf = pysam.VariantFile(args.input_vcf, 'r')
