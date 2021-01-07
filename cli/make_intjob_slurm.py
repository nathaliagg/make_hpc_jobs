#!/usr/bin/env python
"""
Author : Nathalia Graf-Grachet
Date   : 2020-12-11
Purpose: Interactive job generator Puma
"""

import argparse
import os

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Basic interactive SLURM script for Puma",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument('-n', '--nodes',
                        metavar='str',
                        help="Number of nodes. Always nodes = 1 unless GNU Parallel",
                        type=str,
                        default='1')

    parser.add_argument('-c', '--cores',
                        metavar='str',
                        help="Number of cores or processors, min = 1, max = 94",
                        type=str,
                        default='10')

    parser.add_argument('-q', '--queue',
                        metavar='str',
                        help="Main queues: debug, standard, windfall",
                        type=str,
                        default='standard')

    parser.add_argument('-j', '--jobName',
                        metavar='str',
                        help="Job name",
                        type=str,
                        default="script")

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
    """Interactive SLURM script generator"""

    args = get_args()

    script_body = """srun --nodes=NODES --ntasks=CORES --ntasks-per-node=CORES --mem-per-cpu=MEMORYGb --time=WALLTIME --job-name=JOBNAME --account=QUEUE --pty bash -i\n"""

    script_body_replaced = replace_handles(script_body, args)

    print(script_body_replaced)

    print('Script generator complete.')


# --------------------------------------------------
def replace_handles(script_body, args):
    """Replace the arguments in the script body"""

    to_replace = [("NODES", args.nodes),
                  ("CORES", args.cores),
                  ("QUEUE", args.queue),
                  ("MEMORY", str(int(int(args.cores)*5.4))),
                  ("JOBNAME", args.jobName),
                  ("WALLTIME", args.walltime),
                  ("PI", args.positional)]

    for op in to_replace:
            script_body = script_body.replace(op[0], op[1])

    return script_body


# --------------------------------------------------
if __name__ == '__main__':
    main()
