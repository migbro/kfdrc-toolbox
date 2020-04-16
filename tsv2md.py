import sys
import argparse
import pdb

parser = argparse.ArgumentParser(description='Script to summarize peddy outputs.')
parser.add_argument('-f', '--file', action='store', dest='tsv', help='tsv file')
parser.add_argument('-m', '--max-col', action='store', dest='max', help='max column width')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

data = []
max_len = []
max_w = int(args.max)

for line in open(args.tsv):
    info = line.rstrip('\n').split('\t')
    data.append(info)
    if len(max_len) == 0:
        for item in info:
            max_len.append(len(item))
    else:
        for i in range(len(max_len)):
            if len(info[i]) > max_w:
                max_len[i] = max_w
            elif len(info[i]) > max_len[i]:
                max_len[i] = len(info[i])
# print header first
d_ct = []
for i in range(len(data[0])):
    d_ct.append(len(data[0][i]))
    sys.stdout.write(" | " + data[0][i] + "".join([" "] * max_len[i]))
    d_ct[i] += max_len[i]
sys.stdout.write(" |\n")
for i in range(len(data[0])):
    sys.stdout.write(" | " + "".join(["-"] * d_ct[i]))
sys.stdout.write(" |\n")
# pdb.set_trace()
for i in range(1, len(data), 1):
    for j in range(len(data[i])):
        d_ct = len(data[i][j]) + 2
        sys.stdout.write(" | " + data[i][j] + "".join([" "] * max_len[j]))
        d_ct += max_len[j]
    sys.stdout.write(" |\n")


