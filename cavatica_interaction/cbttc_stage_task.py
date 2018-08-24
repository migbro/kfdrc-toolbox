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
        try:
            source_cram = api.files.query(project=source_project, names=[cram])[0]
            source_crai = api.files.query(project=source_project, names=[crai])[0]
            source_cram.copy(project=cur_project, name=cram)
            source_crai.copy(project=cur_project, name=crai)
        except:
            sys.stderr.write('Cannot find cram ' + cram + '\n')
            return 'missing'
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
    inputs['threads'] = 28
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
    except:
        print('Could not create task for ' + task_name + '!\n')


# In[28]:

if len(sys.argv) < 4:
    sys.stderr.write('Usage: ' + sys.argv[0] + '<file with T/N bs ids and crams> <bs id to skip. enter \'none\' if '
                                            'none are to be skipped> <csv separated args for columns containing ids>')
    exit(1)
master_file = sys.argv[1]
bsid_skip_file = sys.argv[2]
col_list = sys.argv[3]
(tid, tcram, nid, ncram) = list(map(int, col_list.split(',')))
kfdrc_url = 'https://kf-api-dataservice.kidsfirstdrc.org'
mh = open(master_file)
head = next(mh)
cur_project = 'kfdrc-harmonization/sd-bhjxbdqk-07'
source_project = 'kids-first-drc/sd-bhjxbdqk-har'
bs_id_skip = {}
if bsid_skip_file != 'none':
    for bs_id in open(bsid_skip_file):
        bs_id_skip[bs_id.rstrip('\n')] = 0
for line in (mh):
    info = line.rstrip('\n').split('\t')
    tumor_id = info[tid]
    normal_id = info[nid]
    if tumor_id in bs_id_skip or normal_id in bs_id_skip:
        sys.stderr.write('BS ID to skip found in line, skipping!\n' + line)
        continue
    tumor_cram_obj = find_copy_cram(cur_project, source_project, info[tcram])
    normal_cram_obj = find_copy_cram(cur_project, source_project, info[ncram])
    if tumor_cram_obj == 'missing' or normal_cram_obj == 'missing':
        sys.stderr.write('Job is missing a file.  Skipping task creation!\n')
    else:
        create_task(tumor_id, normal_id, tumor_cram_obj, normal_cram_obj, api, cur_project)

