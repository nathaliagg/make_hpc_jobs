#!/usr/bin/env python3

"""tests for make_pbs_script.py"""

import hashlib
import os
import random
import re
import string
import glob
from subprocess import getstatusoutput

prg = '../make_pbs_script.py'
pi_name = 'my_boss'


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

    default_script_name = 'my_script'

    rv, out = getstatusoutput(f'{prg} {pi_name}')
    assert rv == 0
    assert re.findall("PBS script complete", out)
    assert os.path.exists("my_script.pbs")


# --------------------------------------------------
def test_shebang():
    """Test first line of script is #! (shebang)"""

    default_script_name = 'my_script'

    script_string = open(default_script_name+'.pbs').read()
    assert script_string.startswith("#!")


# --------------------------------------------------
def test_script_body_correctly_replaced():
    """Test if the handles in the script body
        was correctly replaced in output"""

    default_script_name = 'my_script'

    rv, out = getstatusoutput(f'{prg} {pi_name}')
    assert rv == 0
    assert re.findall("PBS script complete", out)

    output_script = open(default_script_name+'.pbs').read()
    handles = ["NODES", "MEMORY"] # testing two handles is enough

    for h in handles:
        result_search = re.findall(h, output_script)
        assert result_search == []
