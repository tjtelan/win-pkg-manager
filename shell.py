#!/usr/bin/env python

# installation protocol -- draft

# Other program will be responsible for updating the snapshot of the currently installed programs in the database
# This program will only update the snapshots for the current program if it has not yet been done in the current calendar day

# (-r flag applies first)
#
# download program
# check if dependencies satisfied (if not, recurse)
# (-B flag)
# install
# (-A flag)
#
# (apply -R flag now)
#
#
# suggestion: create a port-tree-like hierarchy for this program

# Get help to look similar to this:
# usage: portsnap [options] command ... [path]
# where options are flags
# and commands are update,install,info,remove...

import argparse


#class WindowsPackageManager:
#    def cli(self, argv):
parser = argparse.ArgumentParser(description='FreeBSD ports inspired package manager for Windows', prefix_chars='-')


#parser = argparse.ArgumentParser(prog='PROG', usage='%(prog)s [options] command ... [pkg_name]')
parser.add_argument('-a', '--all', action='store_true', help='Do with all the installed packages')
parser.add_argument('-A', '--afterinstall', metavar='CMD', nargs=1, help='Run the specified command after each installation')
parser.add_argument('-B', '--beforeinstall', metavar='CMD', nargs=1, help='Run the specified command before each installation')
parser.add_argument('-f', '--force', action='store_true', help='Force the upgrade of a port even if it is to be a downgrade or just a reinstall')
parser.add_argument('-F', '--fetch-only', action='store_true', help='Only fetch distfiles or packages. Do not build or install anything')
parser.add_argument('-k', '--keep-going', action='store_true', help='Force the upgrade of a port even if some of the requisite ports have failed to upgrade')
parser.add_argument('-l', '--log-file', metavar='path', nargs=1, help='Use log file at specified location')
parser.add_argument('-n', '--no-execute', action='store_true', help='Do not upgrade any ports, but just show what would be done')
parser.add_argument('-r', '--recursive', action='store_true', help='Do with all those depending on the given packages as well')
parser.add_argument('-R', '--upward-recursive', action='store_true', help='Do with all those required by the given packages as well / Fetch recursively if -F is specified')
parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose')


parser.add_argument('command', choices=['info', 'update', 'install', 'remove'], help='')
parser.add_argument('pkg_name', nargs='*', help='')

args = parser.parse_args()

print args

#    def check_version(self, prog):
#        # query database for program details
#        # perform method for checking for updates (cli or website or...)
#        return
