#!/usr/bin/env python

import os, sys
sys.path.append(os.curdir)

#from wpm_db import db
from wpm_shell import shell

x = shell('logfile')

x.cmd(sys.argv)

