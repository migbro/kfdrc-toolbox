#!/usr/bin/env python3
import sys
import os

study_index = open('/Users/brownm28/Documents/2018-Aug-15_cbttc_launch/portal_metadata/dx_index.txt')
cwd = '/Users/brownm28/Documents/2018-Aug-15_cbttc_launch/portal_metadata/'
os.chdir(cwd)
study_dict = {}
for line in study_index:
    info = line.rstrip('\n').split('\t')
    cid = info[1]
    study_dx = info[0]
    study_dict[study_dx] = cid

pt_fh = {}
samp_fh = {}
pt_head = '#Patient Identifier\tGENDER\tAGE\tTUMOR_SITE\tRACE\tETHNICITY\n'\
'#Patient identifier\tGender or sex of the patient\tAge at which the condition or disease was first diagnosed, in years\tTumor location\tracial demographic\tethnic demographic\n'\
'#STRING\tSTRING\tNUMBER\tSTRING\tSTRING\tSTRING\n'\
'#1\t1\t1\t1\t1\t1\n'\
'PATIENT_ID\tGENDER\tAGE\tTUMOR_SITE\tRACE\tETHNICITY\n'

sys.stderr.write(pt_head)
# IMPORTANT! will use external sample id as sample id, and bs id as a specimen id
samp_head = '#Patient Identifier\tSample Identifier\tSPECIMEN_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tMATCHED_NORMAL_SAMPLE_ID\tMATCHED_NORMAL_SPECIMEN_ID\n'\
'#Patient identifier\tSample Identifier using external_sample_id\tkfdrc tumor biopsecimen ID\tStudy-defined cancer type\tStudy-defined cancer type detail\ttumor tissue location\tprimary v metastatic tumor designation\tmatched normal external_sample_id\tkfdrc matched normal biospecimen ID\n'\
'#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\n'\
'#1\t1\t1\t1\t1\t1\t1\t1\t1\n'\
'PATIENT_ID\tSAMPLE_ID\tSPECIMEN_ID\tCANCER_TYPE\tCANCER_TYPE_DETAILED\tTUMOR_TISSUE_SITE\tTUMOR_TYPE\tMATCHED_NORMAL_SAMPLE_ID\tMATCHED_NORMAL_SPECIMEN_ID\n'

