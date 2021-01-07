#!/usr/bin/env python3

"""tests for make_slurm_script.py"""

import hashlib
import os
import random
import re
import string
import glob
from subprocess import getstatusoutput

prg = '../make_slurm_script.py'
pi_name = 'my_boss'
out_msg = "Script generator complete"
default_script_name = 'my_script'


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
    assert os.path.exists("my_script.slurm")


# --------------------------------------------------
def test_shebang():
    """Test first line of script is #! (shebang)"""

    script_string = open(default_script_name+'.slurm').read()
    assert script_string.startswith("#!")


# --------------------------------------------------
def test_script_body_correctly_replaced():
    """Test if the handles in the script body
        was correctly replaced in output"""

    rv, out = getstatusoutput(f'{prg} {pi_name}')
    assert rv == 0
    assert re.findall(out_msg, out)

    output_script = open(default_script_name+'.slurm').read()
    handles = ["NODES", "MEMORY"] # testing two handles is enough

    for h in handles:
        result_search = re.findall(h, output_script)
        assert result_search == []


# --------------------------------------------------
def test_find_sbatch():
    """Find #SBATCH in the output"""

    output_script = open(default_script_name+'.slurm').read()

    assert re.findall("#SBATCH ", output_script)

# --------------------------------------------------
