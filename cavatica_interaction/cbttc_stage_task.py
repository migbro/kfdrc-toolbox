#!/usr/bin/env python3
# coding: utf-8

# In[6]:


import sevenbridges as sbg
import sys
from requests import request

config = sbg.Config(profile='cavatica')
api = sbg.Api(config=config)


# In[27]:


def get_bsid(url, aliquot_id):
    ali_url = url + '/biospecimens?external_aliquot_id=' + aliquot_id
    sys.stderr.write(ali_url)
    bs_info = request('GET', ali_url)
    return bs_info.json()['results'][0]['kf_id']


# In[8]:


def find_copy_cram(cur_project, source_project, cram):
   
    try:
        cur_cram = api.files.query(project=cur_project, names=[cram])[0]
        return cur_cram
    except:
        sys.stderr.write(cram + ' not in' + cur_project + ', copying from ' + source_project + '\n')
        crai = cram + '.crai'
        source_cram = api.files.query(project=source_project, names=[cram])[0]
        source_crai = api.files.query(project=source_project, names=[crai])[0]
        source_cram.copy(project=cur_project, name=cram)
        source_crai.copy(project=cur_project, name=crai)
        cur_cram = api.files.query(project=cur_project, names=[cram])[0]
        return cur_cram


# In[26]:


def create_task(tumor_id, normal_id, tumor_cram_obj, normal_cram_obj, api, project):
    task_name = 'cbttc-dna-launch-' + tumor_id + '_' + normal_id
    app_name = project + '/cbttc-pipe-with-maf'

    inputs = {}
    inputs['tumor_cram'] = tumor_cram_obj
    inputs['normal_cram'] = normal_cram_obj
    inputs['tumor_id'] = tumor_id
    inputs['normal_id'] = normal_id
    inputs['threads'] = 36
    inputs['reference'] = api.files.query(project=project, names=['Homo_sapiens_assembly38.fasta'])[0]
    inputs['chr_len'] = api.files.query(project=project, names=['hs38_chr.len'])[0]
    inputs['ref_chrs'] = api.files.query(project=project, names=['GRCh38_everyChrs.tar.gz'])[0]
    inputs['ref_tar_gz'] = api.files.query(project=project, names=['hg38_snpeff.tgz'])[0]
    inputs['hg38_strelka_bed'] = api.files.query(project=project, names=['hg38_strelka.bed.gz'])[0]
    inputs['vep_cache'] = api.files.query(project=project, names=['homo_sapiens_vep_93_GRCh38_convert_cache.tar.gz'])[0]
    
    try:
        task = api.tasks.create(name=task_name, project=project, app=app_name, inputs=inputs, run=False)
        task.inputs['output_basename'] = task.id
        task.save()
        print ('Tumor: ', tumor_id, tumor_cram_obj.name, 'Normal:', normal_id, normal_cram_obj.name, 'Task:' + task.id)
    except SbError:
        print('Could not create task for ' + task_name + '!\n')


# In[28]:


master_file = sys.argv[1]
bsid_skip_file = sys.argv[2]
kfdrc_url = 'https://kf-api-dataservice.kidsfirstdrc.org'
mh = open(master_file)
cur_project = 'kfdrc-harmonization/sd-bhjxbdqk-07'
source_project = 'kids-first-drc/sd-bhjxbdqk-har'
bs_id_skip = {}
if bsid_skip_file != 'none':
    for bs_id in open(bsid_skip_file):
        bs_id_skip[bs_id.rstrip('\n')] = 0
for line in (mh):
    info = line.rstrip('\n').split('\t')
    tumor_id = info[3]
    normal_id = info[7]
    if tumor_id in bs_id_skip or normal_id in bs_id_skip:
        sys.stderr.write('BS ID to skip found in line, skipping!\n' + line)
        continue
    tumor_cram_obj = find_copy_cram(cur_project, source_project, info[4])
    normal_cram_obj = find_copy_cram(cur_project, source_project, info[8])
    create_task(tumor_id, normal_id, tumor_cram_obj, normal_cram_obj, api, cur_project)

