#!/usr/bin/env python3
import sys
import os
import re
import pdb

recon = open(sys.argv[1])
super_tbl = open(sys.argv[2])
dna = open(sys.argv[3])
rna = open(sys.argv[4])
cl_fh = open(sys.argv[5])


cwd = '/Users/brownm28/Documents/2018-Aug-15_cbttc_launch/portal_metadata/mega_table'
os.chdir(cwd)

recon_dx_index = {}
next(recon)
for line in recon:
    info = line.rstrip('\n').split('\t')
    c_event = info[1]
    if c_event not in recon_dx_index:
        recon_dx_index[c_event] = []
        for i in range(-3, 0, 1):
            if info[i] != '':
                recon_dx_index[c_event].append(info[i])

next(super_tbl)
pt_super = {}
# will be dict of bs ids as keys - keys have array with pt id, ext id, and array of locations
samp_super = {}
samp_patch = {}
norm_index = {}
black_list = {}
for bs_id in cl_fh:
    black_list[bs_id.rstrip('\n')] = 0
for line in super_tbl:
    info = line.rstrip('\n').split('\t')
    pt_id = info[0]
    sites = info[9]
    site = []
    if sites != '':
        try:
            site = list(set(re.split(';|\|', sites)))
        except:
            sys.stderr.write('Failed at line\n' + line + sites + '\n')
            exit(1)
        try:
            site.remove('')
        except:
            i_dont_care = 0

    else:
        site.append('')
    ages = info[8]
    age = ''
    if ages != '':
        age = 999
        p1 = ages.split('|')
        for item in p1:
            p2 = item.split(';')
            for entry in p2:
                if entry != '' and int(entry) < age:
                    age = int(entry)
        if age == 999:
            age = ''

    ethnicity = info[1]
    race = info[2]
    gender = info[3]
    pt_super[pt_id] = '\t'.join((gender, str(age), ';'.join(site), race, ethnicity))
    bs_loc = info[9].split('|')
    tum_bs = info[4].split(',')
    tum_ext = info[5].split(',')
    site_prime = sites.split('|')
    for i in range(0, len(tum_bs), 1):
        if tum_bs[i] not in black_list:
            if tum_ext[i] not in samp_super:
                samp_super[tum_ext[i]] = []
                samp_super[tum_ext[i]].append(pt_id)
                samp_super[tum_ext[i]].append(tum_bs[i])
                cur_sites = ''
                if site_prime != '':
                    cur_sites = list(set(site_prime[i].split(';')))
                    try:
                        cur_sites.remove('')
                    except:
                        i_dont_care = 1
                samp_super[tum_ext[i]].append(cur_sites)
            else:
                samp_super[tum_ext[i]][1] += ';' + tum_bs[i]
        samp_patch[tum_bs[i]] = tum_ext[i]
        norm_bs = info[-3].split(',')
        norm_ext = info[-2].split(',')
        for i in range(0, len(norm_bs), 1):
            norm_index[norm_bs[i]] = norm_ext[i]
pt_check = {}
ext_check = {}
pt_head = '#Patient Identifier\tGENDER\tAGE\tTUMOR_SITE\tRACE\tETHNICITY\n#Patient identifier' \
          '\tGender or sex of the patient\tAge at which the condition or disease was first diagnosed, in years' \
          '\tTumor location\tracial demographic\tethnic demographic\n#STRING\tSTRING\tNUMBER\tSTRING\tSTRING' \
          '\tSTRING\n#1\t1\t1\t1\t1\t1\nPATIENT_ID\tGENDER\tAGE\tTUMOR_SITE\tRACE\tETHNICITY\n'

sys.stderr.write(pt_head)
# IMPORTANT! will use external sample id as sample id, and bs id as a specimen id
samp_head = '#Patient Identifier\tSample Identifier\tSPECIMEN_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED' \
            '\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tMATCHED_NORMAL_SAMPLE_ID\tMATCHED_NORMAL_SPECIMEN_ID' \
            '\n#Patient identifier\tSample Identifier using external_sample_id\tkfdrc tumor biopsecimen ID' \
            '\tStudy-defined cancer type\tStudy-defined cancer type detail\ttumor tissue location' \
            '\tprimary v metastatic tumor designation\tmatched normal external_sample_id' \
            '\tkfdrc matched normal biospecimen ID\n#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING' \
            '\tSTRING\n#1\t1\t1\t1\t1\t1\t1\t1\t1\nPATIENT_ID\tSAMPLE_ID\tSPECIMEN_ID\tCANCER_TYPE' \
            '\tCANCER_TYPE_DETAILED\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tMATCHED_NORMAL_SAMPLE_ID' \
            '\tMATCHED_NORMAL_SPECIMEN_ID\n'
sys.stderr.write(samp_head)

pt_out = open('data_clinical_patient.txt', 'w')
samp_out = open('data_clinical_sample.txt', 'w')

pt_out.write(pt_head)
samp_out.write(samp_head)

next(dna)
for data in dna:
    info = data.rstrip('\n').split('\t')
    tum_bs = info[2]
    ext = samp_patch[tum_bs]
    if tum_bs not in black_list and ext not in ext_check:
        ext_check[ext] = 1
        norm_bs = info[5]
        c_event = info[1]
        ext_ref = samp_super[ext]
        pt_id = ext_ref[0]
        sample_id = ext
        spec_ids = ext_ref[1]
        cancer_type = ';'.join(recon_dx_index[c_event])
        bs_loc = ';'.join(ext_ref[2])
        tum_type = 'Primary'
        if cancer_type == 'Metastatic secondary tumors':
            tum_type = 'Metastatic'
        norm_sample_id = norm_index[norm_bs]
        if pt_id not in pt_check:
            pt_check[pt_id] = 1
            pt_out.write(pt_id + '\t' + pt_super[pt_id] + '\n')
        # pdb.set_trace()
        samp_out.write('\t'.join((pt_id, sample_id, spec_ids, cancer_type, cancer_type, bs_loc, tum_type,
                                  norm_sample_id, norm_bs)) + '\n')

next(rna)
for data in rna:
    info = data.rstrip('\n').split('\t')
    tum_bs = info[0]
    ext = samp_patch[tum_bs]
    if tum_bs not in black_list and ext not in ext_check:
        (bo_sample_id, assay) = info[1].split('.')
        c_info = bo_sample_id.split('-')
        c_event = c_info[0] + '-' + c_info[1]
        ext_ref = samp_super[ext]
        pt_id = ext_ref[0]
        bo_pt_id = info[3]
        sample_id = ext
        spec_ids = ext_ref[1]
        cancer_type = ';'.join(recon_dx_index[c_event])
        bs_loc = ';'.join(ext_ref[2])
        tum_type = 'Primary'
        if cancer_type == 'Metastatic secondary tumors':
            tum_type = 'Metastatic'
        if pt_id not in pt_check:
            pt_check[pt_id] = 1
            pt_out.write(pt_id + '\t' + pt_super[pt_id] + '\n')
        samp_out.write('\t'.join((pt_id, sample_id, spec_ids, cancer_type, cancer_type, bs_loc, tum_type, '', ''))
                       + '\n')
