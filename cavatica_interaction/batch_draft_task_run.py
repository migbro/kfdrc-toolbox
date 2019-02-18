#!/usr/bin/env python3

import sevenbridges as sbg
import argparse
from sevenbridges.http.error_handlers import rate_limit_sleeper, maintenance_sleeper
import sys
import time


def date_time():
    cur = ">" + time.strftime("%c") + '\n'
    return cur


parser = argparse.ArgumentParser(description='Run a subset of drafted tasks at all times.'
                                             'Use in conjunction with cron tab')
parser.add_argument('-p', '--project', action='store', dest='project', help='cavatica file id list')
parser.add_argument('-q', '--profile', action='store', dest='profile', help='cavatica profile name')
parser.add_argument('-j', '--num-jobs', action='store', dest='num_jobs', help='Num jobs to keep running')
parser.add_argument('-o', '--output', action='store', dest='output', help='Output log file name')

if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

config = sbg.Config(profile=args.profile)
api = sbg.Api(config=config, error_handlers=[rate_limit_sleeper, maintenance_sleeper])


limit = int(args.num_jobs)
draft_tasks = api.tasks.query(project=args.project, status='DRAFT')
running_tasks = api.tasks.query(project=args.project, status='RUNNING')
cur_run = len(running_tasks)
out_fh = open(args.output, 'a')
out_fh.write(date_time() + 'Checking draft/running jobs for project ' + args.project + '\n')
if len(draft_tasks) == 0:
    out_fh.write('0 tasks in draft.  Exiting.\n')
elif cur_run >= limit:
    out_fh.write('Num of tasks run at or above max specified: ' + str(cur_run) + ' running jobs, limit set: '
                 + args.num_jobs + '\n')
else:
    out_fh.write(str(limit-cur_run) + ' spots open for submission\n')
    stop = limit
    if len(draft_tasks) < stop:
        stop = len(draft_tasks)
    for i in range(cur_run, stop):
        draft_tasks[i].run()
        out_fh.write('Running task ' + draft_tasks[i].id + ' ' + draft_tasks[i].name + '\n')
out_fh.close()
