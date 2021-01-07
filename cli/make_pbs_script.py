#!/usr/bin/env python

"""
Author : Nathalia Graf-Grachet
Date   : 2020-08-31
Purpose: PBS script generator
"""

import argparse
import os

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Basic PBS script for Ocelote",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument('-s', '--script_name',
                        metavar='str',
                        help='Script filename, e.g., my_script, so filename will be my_script.pbs',
                        default="my_script")

    parser.add_argument('-n', '--nodes',
                        metavar='str',
                        help="Number of nodes. Always nodes = 1 unless GNU Parallel",
                        type=str,
                        default='1')

    parser.add_argument('-q', '--queue',
                        metavar='str',
                        help="Main queues: debug, standard, windfall",
                        type=str,
                        default='standard')

    parser.add_argument('-c', '--cores',
                        metavar='str',
                        help="Number of cores or processors, min = 1, max = 28",
                        type=str,
                        default='10')

    parser.add_argument('-j', '--jobName',
                        metavar='str',
                        help="Job name",
                        type=str,
                        default="my_job")

    parser.add_argument('-w', '--walltime',
                        metavar='str',
                        help='Walltime [hh:mm:ss]. Choose more than you need, max 240h',
                        type=str,
                        default="12:00:00")

    parser.add_argument('-e', '--email',
                        help='Optional, your netid@email.arizona.edu, BEGIN|END|ABNORMAL',
                        metavar='str',
                        type=str,
                        default=None)

    parser.add_argument('positional',
                        help="Your PI name",
                        metavar='PI name',
                        type=str,
                        default=None)

    args = parser.parse_args()

    return args


# --------------------------------------------------
def main():
    """PBS script generator"""

    args = get_args()
    # print(args)

    script_body = """#!/bin/bash\n#PBS -q QUEUE\n#PBS -l select=NODES:ncpus=CORES:mem=MEMORYgb\n#PBS -N JOBNAME\n#PBS -W group_list=PI\n#PBS -l place=free:shared\n#PBS -l walltime=WALLTIME\n"""

    if args.email:
        script_body+= """#PBS -m bea\n#PBS -M EMAIL\n"""

    script_body+= "\ncd $PBS_O_WORKDIR\n"

    script_body_replaced = replace_handles(script_body, args)
    # print(script_body_replaced)

    with open(args.script_name+".pbs", 'w') as out:
        out.write(script_body_replaced+'\n')

    print('Script generator complete.')


# --------------------------------------------------
def replace_handles(script_body, args):
    """Replace the arguments in the script body"""

    to_replace = [("NODES", args.nodes),
                  ("CORES", args.cores),
                  ("QUEUE", args.queue),
                  ("MEMORY", str(int(args.cores)*6)),
                  ("JOBNAME", args.jobName),
                  ("WALLTIME", args.walltime),
                  ("PI", args.positional)]

    if args.email:
                  to_replace.append(("EMAIL", args.email))

    for op in to_replace:
            script_body = script_body.replace(op[0], op[1])

    return script_body


# --------------------------------------------------
if __name__ == '__main__':
    main()
