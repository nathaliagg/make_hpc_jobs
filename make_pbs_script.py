#!/usr/bin/env python
"""
Author : Nathalia Graf-Grachet <nathaliagg@arizona.edu>
Date   : 2020-08-31
Purpose: PBS script generator
"""

import argparse
import os


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Basic PBS script for standard queue in Ocelote",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )


    parser.add_argument('-s', '--script_name',
                        metavar='str',
                        help='Name of the script, e.g., name.pbs',
                        default="myscript")

    parser.add_argument('-n', '--nodes',
                        metavar='str',
                        help="Number of nodes. Always nodes = 1 unless GNU Parallel",
                        type=str,
                        default='1')

    parser.add_argument('-c', '--cores',
                        metavar='str',
                        help="Number of cores or processors, min = 1, max = 28",
                        type=str,
                        default='10')

    parser.add_argument('-j', '--jobName',
                        metavar='str',
                        help="Job name",
                        type=str,
                        default="myjob")

    parser.add_argument('-w', '--wallTime',
                        metavar='00:00:00',
                        help='Walltime [hh:mm:ss]. Choose more than you need, max 240h',
                        type=str,
                        default="12:00:00")

    parser.add_argument('-e', '--email',
                        help='Optional, your netid@email.arizona.edu',
                        metavar='e-mail',
                        type=str,
                        default=None)

    parser.add_argument('-pi', '--principal_investigator',
                        help="Who's the boss? Our cool PI (:",
                        metavar='boss',
                        type=str,
                        default="tfaily")

    args = parser.parse_args()


    return args


# --------------------------------------------------
def main():
    """PBS script generator for Tfaily Lab"""

    args = get_args()
    script_body = """#!/bin/bash\n#PBS -q standard\n#PBS -l select=NODES:ncpus=CORES:mem=MEMORYgb\n#PBS -N JOBNAME\n#PBS -W group_list=PI\n#PBS -l place=free:shared\n#PBS -l cput=560:00:00\n#PBS -l walltime=WALLTIME\n"""

    if args.email:
        script_body+= """#PBS -m bea\n#PBS -M EMAIL\n"""


    script_body+= "\ncd $PBS_O_WORKDIR\n"

    to_replace = [("NODES", args.nodes),
                  ("CORES", args.cores),
                  ("MEMORY", str(int(args.cores)*6)),
                  ("JOBNAME", args.jobName),
                  ("WALLTIME", args.wallTime),
                  ("PI", args.principal_investigator)]

    if args.email:
                  to_replace.append(("EMAIL", args.email))

    for op in to_replace:
            script_body = script_body.replace(op[0], op[1])

    with open(args.script_name+".pbs", 'w') as out:
            out.write(script_body+'\n')


# --------------------------------------------------
if __name__ == '__main__':
    main()
