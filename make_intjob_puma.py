#!/usr/bin/env python
"""
Author : Nathalia Graf-Grachet <nathaliagg@arizona.edu>
Date   : 2020-12-11
Purpose: Interactive job generator Puma
"""

import argparse
import os

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Interactive job for standard queue in Puma",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

    parser.add_argument('nodes',
                        metavar='num_nodes',
                        help="Number of nodes. Always nodes = 1 unless GNU Parallel",
                        type=str)

    parser.add_argument('cores',
                        metavar='num_cores',
                        help="Number of cores or processors, min = 1, max = 96",
                        type=str)

    parser.add_argument('jobName',
                        metavar='jobName',
                        help = 'Job name',
                        type=str)

    parser.add_argument('wallTime',
                        metavar='walltime',
                        help='Walltime [hh:mm:ss]. Choose more than you need, max 240h',
                        type=str)

    parser.add_argument('principal_investigator',
                        help="Malak (:",
                        metavar="who's_the_boss?",
                        type=str)

    args = parser.parse_args()


    return args


# --------------------------------------------------
def main():
    """Interactive job generator for Tfaily Lab"""

    args = get_args()

    script_body = """srun --nodes=NODES --ntasks=CORES --ntasks-per-node=CORES --mem-per-cpu=MEMORYGb --time=WALLTIME --job-name=JOBNAME --account=windfall --pty bash -i\n"""

    to_replace = [("NODES", args.nodes),
                  ("CORES", args.cores),
                  ("MEMORY", str(int(int(args.cores)*5.333))),
                  ("JOBNAME", args.jobName),
                  ("WALLTIME", args.wallTime),
                  ("PI", args.principal_investigator)]

    for op in to_replace:
            script_body = script_body.replace(op[0], op[1])

    print(script_body)


# --------------------------------------------------
if __name__ == '__main__':
    main()
