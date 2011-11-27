#!/usr/bin/env python2.7

import os, sys
sys.path.append(os.curdir)


import sqlite3, logging
from wpm_shell import shell

x = shell('logfile')

x.cmd(sys.argv)

