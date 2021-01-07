#!/usr/bin/env python
"""
Author : Nathalia Graf-Grachet
Date   : 2020-08-29
Purpose: Interactive job generator Ocelote
"""

import argparse
import os

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Basic interactive PBS script for Ocelote",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

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

    parser.add_argument('positional',
                        help="Your PI name",
                        metavar='PI name',
                        type=str,
                        default=None)

    args = parser.parse_args()

    return args


# --------------------------------------------------
def main():
    """Interactive PBS script generator"""

    args = get_args()
    # print(args)

    script_body = "qsub -I -N JOBNAME -W group_list=PI -q QUEUE -l select=NODES:ncpus=CORES:mem=MEMORYgb -l walltime=WALLTIME\n"

    script_body_replaced = replace_handles(script_body, args)
    # print(script_body_replaced)

    print(script_body_replaced)

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

    for op in to_replace:
            script_body = script_body.replace(op[0], op[1])

    return script_body


# --------------------------------------------------
if __name__ == '__main__':
    main()
