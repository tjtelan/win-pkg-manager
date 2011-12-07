#!/usr/bin/env python2.7

import os, sys
sys.path.append(os.curdir)


import sqlite3, logging
from wpm_shell import shell

# TODO: Load settings.py and pass relevant settings to shell

x = shell('logfile')

x.cmd(sys.argv)

