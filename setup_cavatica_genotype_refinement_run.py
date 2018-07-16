#!/usr/bin/env python3

import sevenbridges as sbg
import sys
from requests import request

config = sbg.Config(profile='cavatica')
api = sbg.Api(config=config)


def get_bs_id(url):
    pt_info = request('GET', url)
    return pt_info.json()['results'][0]['kf_id']


def build_ped_entry(url, fam_id, out):
    info = request('GET', url)
    patient_sex = 'unkown'
    ind_id = ''
    paternal_id = ''
    maternal_id = ''
    # currently assumed all prbands have phenotype!!! can actually check iof needed
    phenotype = '2'
    sex = {'Male': '1', 'Female': '2'}
    # ped file output format:
    # fam_id\tindividual_id\tpaternal_id\tmaternal_id\tsex<0,1,2>\tphenotype<-9,0,1,2>
    for person in info.json()['results']:
        bs_url = 'http://localhost:1080' + person['_links']['biospecimens']
        bs_id = get_bs_id(bs_url)
        if person['is_proband'] == True:
            if person['gender'] in sex:
                patient_sex = sex[person['gender']]
            ind_id = bs_id
        elif person['gender'] == 'Female':
            maternal_id = bs_id
        else:
            paternal_id = bs_id
    new_ped = open(out, 'w')
    new_ped.write('\t'.join((fam_id, ind_id, paternal_id, maternal_id, patient_sex, phenotype)) + '\n')
    new_ped.close()


project = 'brownm28/kf-genotype-refinement-workflow'
tag_search = 'Trio Joint Genotyping'

files = api.files.query(project=project)
sys.stderr.write('Getting files for ' + project + '\n')
vcf_list = []
for file_obj in files:
    for tag in file_obj.tags:
        if tag == tag_search and file_obj.name[-7:] == '.vcf.gz':
            vcf_list.append(file_obj)
            sys.stderr.write('Found relevant file ' + file_obj.name + '\n')

sys.stderr.write('Building and uploading .ped files to project\n')
for vcf in vcf_list:
    fam_id =  vcf.metadata['Kids First ID']
    url = 'http://localhost:1080/participants?family_id=' + fam_id
    out = fam_id + '.ped'
    build_ped_entry(url, fam_id, out)
    sys.stderr.write('Uploading ' + out + ' to cavatica for project ' + project + '\n')
    api.files.upload(project=project, path=out)