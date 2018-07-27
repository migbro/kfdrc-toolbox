#!/usr/bin/env python3

import sevenbridges as sbg
import sys
from requests import request

token = sys.argv[2]
# config = sbg.Config(profile='cavatica')
# api = sbg.Api(config=config)
api = sbg.Api(url='https://cavatica-api.sbgenomics.com/v2', token=token)

task_list = sys.argv[1]

for task in open(task_list):
    task = task.rstrip('\n')
    task_obj = api.tasks.get(id=task)
    sys.stderr.write('Updating task ' + task_obj.name + ' with ID ' + task + ' to run\n')
    task_obj.run()

