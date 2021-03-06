#!/usr/bin/env python3

import sys
import os


def process_maf(maf_file, maf_exc, out_fh, samp_id, norm_id):
    maf_read = open(maf_file)
    next(maf_read)
    next(maf_read)
    fcol = 8
    for var in maf_read:
        var_data = var.rstrip('\n').split('\t')
        if var_data[fcol] not in maf_exc:
            var_data[15] = samp_id
            var_data[16] = norm_id
            var_data.pop(3)
            out_fh.write('\t'.join(var_data) + '\n')
    maf_read.close()


def process_cnv(cbio_short, cnv_dict, s_dict, samp_id, cnv_file):
    if cbio_short not in s_dict:
        s_dict[cbio_short] = []
        cnv_dict[cbio_short] = {}
    s_dict[cbio_short].append(samp_id)
    for cnv in open(cnv_file):
        cnv_data = cnv.rstrip('\n').split('\t')
        gene = cnv_data[0] + '\t' + cnv_data[1]
        if gene not in cnv_dict[cbio_short]:
            cnv_dict[cbio_short][gene] = {}
        cnv_dict[cbio_short][gene][samp_id] = cnv_data[2]
    return cnv_dict, s_dict


dx_fh = open(sys.argv[1])
exc_file = open(sys.argv[2])
dna_sheet = open(sys.argv[3])
cnv_dir = sys.argv[4]
maf_dir = sys.argv[5]
mega_sample_sheet = open(sys.argv[6])
mega_patient_sheet = open(sys.argv[7])
skip_data = sys.argv[8]

with open(sys.argv[9]) as f:
    header = f.read()

dx_dict = {}
maf_fh = {}
cnv_fh = {}
sample_fh = {}
samp_head = '#Patient Identifier\tSample Identifier\tSPECIMEN_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED' \
            '\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tMATCHED_NORMAL_SAMPLE_ID\tMATCHED_NORMAL_SPECIMEN_ID' \
            '\n#Patient identifier\tSample Identifier using external_sample_id\tkfdrc tumor biopsecimen ID' \
            '\tStudy-defined cancer type\tStudy-defined cancer type detail\ttumor tissue location' \
            '\tprimary v metastatic tumor designation\tmatched normal external_sample_id' \
            '\tkfdrc matched normal biospecimen ID\n#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING' \
            '\tSTRING\n#1\t1\t1\t1\t1\t1\t1\t1\t1\nPATIENT_ID\tSAMPLE_ID\tSPECIMEN_ID\tCANCER_TYPE' \
            '\tCANCER_TYPE_DETAILED\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tMATCHED_NORMAL_SAMPLE_ID' \
            '\tMATCHED_NORMAL_SPECIMEN_ID\n'
patient_fh = {}
pt_head = '#Patient Identifier\tGENDER\tAGE\tTUMOR_SITE\tRACE\tETHNICITY\n#Patient identifier' \
          '\tGender or sex of the patient\tAge at which the condition or disease was first diagnosed, in years' \
          '\tTumor location\tracial demographic\tethnic demographic\n#STRING\tSTRING\tNUMBER\tSTRING\tSTRING' \
          '\tSTRING\n#1\t1\t1\t1\t1\t1\nPATIENT_ID\tGENDER\tAGE\tTUMOR_SITE\tRACE\tETHNICITY\n'


blacklist = {}
next(dx_fh)
temp = {}
if skip_data == 'y':
    sys.stderr.write('Skip data flag given, will only output sample sheets\n')
for line in dx_fh:
    info = line.rstrip('\n').split('\t')
    cbttc_dx = info[0]
    cbio_short = info[1]
    dx_dict[cbttc_dx] = cbio_short
    if cbio_short not in temp:
        temp[cbio_short] = 1
        os.mkdir(cbio_short)
        if skip_data != 'y':
            maf_fh[cbio_short] = open(cbio_short + '.strelka.vep.filtered.maf', 'w')
            cnv_fh[cbio_short] = open(cbio_short + '.predicted_cnv.txt', 'w')
            maf_fh[cbio_short].write(header)
            cnv_fh[cbio_short].write('Hugo_Symbol\tEntrez_Gene_Id')

        sample_fh[cbio_short] = open(cbio_short + '/data_clinical_sample.txt', 'w')
        sample_fh[cbio_short].write(samp_head)
        patient_fh[cbio_short] = open(cbio_short + '/data_clinical_patient.txt', 'w')
        patient_fh[cbio_short].write(pt_head)


dx_fh.close()

for line in exc_file:
    blacklist[line.rstrip('\n')] = 0

maf_exc = {"Silent": 0, "Intron": 0, "IGR": 0, "3'UTR": 0, "5'UTR": 0, "3'Flank": 0, "5'Flank": 0}

dna_task_dict = {}
next(dna_sheet)
for line in dna_sheet:
    info = line.rstrip('\n').split('\t')
    if info[2] not in blacklist:
        dna_task_dict[info[2]] = info[-2]

maf_suffix = '.strelka.vep.maf'
cnv_suffix = '.CNVs.Genes.copy_number'

pt_dict = {}
for i in range(0, 5, 1):
    next(mega_sample_sheet)

cnv_dict = {}
s_dict = {}


for line in mega_sample_sheet:
    data = line.rstrip('\n').split('\t')
    dx = data[3]
    pt_id = data[0]
    bs_ids = data[2].split(';')
    samp_id = data[1]
    norm_id = data[-2]
    if data[3] != '':
        if pt_id not in pt_dict:
            pt_dict[pt_id] = {}
        dx_list = dx.split(';')
        temp = {}
        for cbttc_dx in dx_list:
            cbio_short = dx_dict[cbttc_dx]
            if cbio_short not in temp:
                pt_dict[pt_id][cbio_short] = 1
                sample_fh[cbio_short].write(line)
                temp[cbio_short] = 1
                if skip_data != 'y':
                    for bs_id in bs_ids:
                        if bs_id in dna_task_dict:
                            sys.stderr.write('DNA data found for ' + bs_id + '\n')
                            cur_maf = maf_dir + '/' + dna_task_dict[bs_id] + maf_suffix
                            sys.stderr.write('Processing maf ' + cur_maf + '\n')
                            sys.stderr.flush()
                            process_maf(cur_maf, maf_exc, maf_fh[cbio_short], samp_id, norm_id)
                            sys.stderr.write('Completed processing ' + cur_maf + '\n')
                            cur_cnv = cnv_dir + '/' + dna_task_dict[bs_id] + cnv_suffix
                            sys.stderr.write('Processing cnv ' + cur_cnv + '\n')
                            sys.stderr.flush()
                            (cnv_dict, s_dict) = process_cnv(cbio_short, cnv_dict, s_dict, samp_id, cur_cnv)
                            sys.stderr.write('Completed processing ' + cur_cnv + '\n')
                            sys.stderr.flush()
mega_sample_sheet.close()

if skip_data != 'y':
    sys.stderr.write('Completed iterating through sample sheet. Outputting cnv files\n')

    for dx in cnv_dict:
        sys.stderr.write('Outputting data for dx ' + dx + '\n')
        sys.stderr.flush()
        cnv_fh[dx].write('\t' + '\t'.join(s_dict[dx]) + '\n')
        for gene in cnv_dict[dx]:
            cnv_fh[dx].write(gene)
            for samp in s_dict[dx]:
                if samp in cnv_dict[dx][gene]:
                    cnv_fh[dx].write('\t' + cnv_dict[dx][gene][samp])
                else:
                    cnv_fh[dx].write('\t2')
            cnv_fh[dx].write('\n')
        cnv_fh[dx].close()

sys.stderr.write('Outputting dx-specific patient info\n')
sys.stderr.flush()

for i in range(0, 5, 1):
    next(mega_patient_sheet)
for line in mega_patient_sheet:
    pt_data = line.rstrip('\n').split('\t')
    if pt_data[0] in pt_dict:
        for dx in pt_dict[pt_data[0]]:
            patient_fh[dx].write(line)
for keys in patient_fh:
    patient_fh[keys].close()
    sample_fh[keys].close()
    if skip_data != 'y':
        cnv_fh[keys].close()
        maf_fh[keys].close()
sys.stderr.write('Fin!\n')
