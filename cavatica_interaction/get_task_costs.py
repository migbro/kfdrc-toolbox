#!/usr/bin/env python3

import sevenbridges as sbg
import sys

#token = sys.argv[2]
config = sbg.Config(profile='cavatica')
api = sbg.Api(config=config)
# api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token=token)

task_list = sys.argv[1]
task_dict = {}
for line in open(task_list):
    task_dict[line.rstrip('\n')] = 0
project = sys.argv[2]
proj_tasks = api.tasks.query(project=project).all()
for task in proj_tasks:
    if task.id in task_dict and task.status == 'COMPLETED':
        print ('\t'.join((task.name, task.id, str(task.price.amount))))