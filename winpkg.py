#!/usr/bin/env python

import os, sys
sys.path.append(os.curdir)


import sqlite3, logging
from wpm_db import db
from wpm_shell import shell

x = shell('logfile')

x.cmd(sys.argv)

