#!/usr/bin/env python3
# coding: utf-8

# ## Initialize api and imports

# In[1]:


import sevenbridges as sbg
import sys
from requests import request

config = sbg.Config(profile='cavatica')
api = sbg.Api(config=config)


# ## Setup helper defs

# In[8]:


def get_bs_id(url):
    pt_info = request('GET', url)
    return pt_info.json()['results'][0]['kf_id']


def build_ped_entry(url, fam_id, out):
    info = request('GET', url)
    patient_sex = 'unkown'
    ind_id = ''
    paternal_id = ''
    maternal_id = ''
    # currently assumed all probands have phenotype!!! can actually check iof needed
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


def create_task(fam_id, ped_out, api, vcf, project):
    task_name = 'refinement-' + fam_id
    app_name = project + '/gatk-genotype-refinement'
    inputs = {}
    inputs['vqsr_vcf'] = vcf
    inputs['snp_sites'] = api.files.query(project=project, names=['1000G_phase3_v4_20130502.sites.hg38.vcf'])[0]
    inputs['reference'] = api.files.query(project=project, names=['Homo_sapiens_assembly38.fasta'])[0]
    inputs['ped'] = api.files.query(project=project, names=[ped_out])[0]
    try:
        task = api.tasks.create(name=task_name, project=project, app=app_name, inputs=inputs, run=False)
        task.inputs['output_basename'] = task.id
        task.save()
        print(task.inputs['vqsr_vcf'].name, fam_id, task.id)
    except SbError:
        print('Could not create task for ' + task_name + '!\n')


# ## Initialize inputs
# #### May want to switch to stdin in if running outside of notebook

# In[3]:

# 'brownm28/kf-genotype-refinement-workflow'
project = sys.argv[1]
# 'Trio Joint Genotyping'
tag_search = sys.argv[2]
exclude_list = sys.argv[3]

exclude_dict = {}
if exclude_list != 'none':
    sys.stderr.write('Exclude list given!\n')
    for fn in open(exclude_list):
        fn = fn.rstrip('\n')
        exclude_dict[fn] = 0
        sys.stderr.write('Excluding ' + fn + '\n')
else:
    sys.stderr.write('No exclusion list given.  Running all files of type ' + tag_search + '\n')
# ## Get vcf object list

# In[4]:


files = api.files.query(project=project, tags=tag_search)
sys.stderr.write('Getting files for ' + project + '\n')
# dir(files)
vcf_list = []
i = 0
for file_obj in files:
    #    for tag in file_obj.tags:
    #        if tag == tag_search and file_obj.name[-7:] == '.vcf.gz':
    if file_obj.name[-7:] == '.vcf.gz':
        if file_obj.name in exclude_dict:
            sys.stderr.write('File ' + file_obj.name + ' in exclude list, skipping!\n')
        else:
            vcf_list.append(file_obj)
            sys.stderr.write('Found relevant file ' + file_obj.name + '\n')
    i += 1
sys.stderr.write('Searched ' + str(i) + ' files for desired criteria\n')

# ## Create .ped files and set up cavatica jobs.  Requires data service running
# In[9]:


sys.stderr.write('Building and uploading .ped files to project\n')
for vcf in vcf_list:
    fam_id = vcf.metadata['Kids First ID']
    url = 'http://localhost:1080/participants?family_id=' + fam_id
    ped_out = fam_id + '.ped'
    build_ped_entry(url, fam_id, ped_out)
    sys.stderr.write('Uploading ' + ped_out + ' to cavatica for project ' + project + '\n')
    api.files.upload(project=project, path=ped_out)
    create_task(fam_id, ped_out, api, vcf, project)
sys.stderr.write('Completed setting up tasks, check output logs\n')

