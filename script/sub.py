#!/usr/bin/env python3

import subprocess


def call(cmd, debug=False, dry=False):
    if debug:
        print("+", cmd)
    r = ""
    if not dry:
        r = subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout.decode('ascii').strip()
        if debug:
            print(r)
    return r
