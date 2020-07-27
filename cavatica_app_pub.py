import argparse
from ruamel import yaml
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input-cwl', action='store', dest='cwl', help='Input cwl file', required=True)
parser.add_argument('-o', '--output-cwl', action='store', dest='out', help='Output cwl file name', required=True)
parser.add_argument('-r', '--readme', action='store', dest='readme', help='Readme file to insert into workflow/tool doc, if applicable', required=False)
parser.add_argument('-l', '--label', action='store', dest='label', help='User-friendly label to add to tool/workflow cwl, if needed', required=False)
parser.add_argument('-t', '--tags', action='store', dest='tags', help='Seven bridges tags file, in yaml format', required=False)
parser.add_argument('-f', '--files', action='store', dest='files', help='Cavatica-style tsv manifest with file ID, file name, and associated cwl input key', required=False)
args = parser.parse_args()


yaml.preserve_quotes = True  # not necessary for your current input

data = yaml.load(open(args.cwl), yaml.RoundTripLoader)

pdb.set_trace()
hold=1