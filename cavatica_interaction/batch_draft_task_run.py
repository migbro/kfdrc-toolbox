#!/usr/bin/env python3

import sevenbridges as sbg
import argparse
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import sys
import time
import re

def date_time():
    cur = ">" + time.strftime("%c") + '\n'
    return cur


parser = argparse.ArgumentParser(description='Run a subset of drafted tasks at all times.'
                                             'Use in conjunction with cron tab')
parser.add_argument('-p', '--project', action='store', dest='project', help='cavatica file id list')
parser.add_argument('-q', '--profile', action='store', dest='profile', help='cavatica profile name')
parser.add_argument('-j', '--num-jobs', action='store', dest='num_jobs', help='Num jobs to keep running')
parser.add_argument('-o', '--output', action='store', dest='output', help='Output log file name')
parser.add_argument('-x', '--prefix', action='store', dest='prefix', help='Task prefix ro run.  Set to ALL if any draft task should run')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

config = sbg.Config(profile=args.profile)
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])


limit = int(args.num_jobs)
draft_tasks = list(api.tasks.query(project=args.project, status='DRAFT').all())
running_tasks = list(api.tasks.query(project=args.project, status='RUNNING').all())
queued_tasks = list(api.tasks.query(project=args.project, status='QUEUED').all())
cur_run = len(running_tasks) + len(queued_tasks)
cur_draft = len(draft_tasks)
out_fh = open(args.output, 'a')
out_fh.write(date_time() + 'Checking draft/running jobs for project ' + args.project + '\n')
if cur_draft == 0:
    out_fh.write('0 tasks in draft.  Exiting.\n')
elif cur_run >= limit:
    out_fh.write('Num of tasks run at or above max specified: ' + str(cur_run) + ' running/queued jobs, limit set: '
                 + args.num_jobs + ', num draft tasks left: ' + str(cur_draft) + '\n')
else:
    out_fh.write(str(limit-cur_run) + ' spots open for submission\n')
    stop = limit
    start = cur_run
    if len(draft_tasks) < stop:
        stop = limit - cur_run
        if stop > len(draft_tasks):
            stop = len(draft_tasks)
        start = 0
    for i in range(start, stop):
        if args.prefix == 'ALL' or re.search(args.prefix, draft_tasks[i].name):
            draft_tasks[i].run()
            out_fh.write('Running task ' + draft_tasks[i].id + ' ' + draft_tasks[i].name + '\n')
        else:
            out_fh.write('Task ' + draft_tasks[i].id + ' ' + draft_tasks[i].name + ' skipped, prefix ' + args.prefix + ' did not match\n')
out_fh.close()
