#!/usr/bin/env python3

"""tests for make_intjob_slurm.py"""

import hashlib
import os
import random
import re
import string
import glob
from subprocess import getstatusoutput

prg = '../make_intjob_slurm.py'
pi_name = 'boss'
out_msg = "Script generator complete"


# --------------------------------------------------
def test_exists():
    """Exists"""

    assert os.path.isfile(prg)


# --------------------------------------------------
def test_usage():
    """Usage"""

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{prg} {flag}')
        assert rv == 0
        assert re.match("usage", out, re.IGNORECASE)


# --------------------------------------------------
def test_no_args():
    """Output when no args are provided"""

    rv, out = getstatusoutput(f'{prg}')
    assert rv != 0
    error_string = 'arguments are required: PI name'
    assert re.findall(error_string, out, re.IGNORECASE)


# --------------------------------------------------
def test_pi_default_args():
    """Output using default"""

    rv, out = getstatusoutput(f'{prg} {pi_name}')
    assert rv == 0
    assert re.findall(out_msg, out)


# --------------------------------------------------
def test_qsub():
    """Test first line of script is srun"""

    rv, out = getstatusoutput(f'{prg} {pi_name}')
    assert rv == 0
    assert re.findall("srun ", out)


# --------------------------------------------------
