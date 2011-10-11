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


import argparse


class WindowsPackageManager:
    def cli(self, argv):
        parser = argparse.ArgumentParser(description='FreeBSD ports inspired package manager for Windows', prefix_chars='-')
        parser.add_argument('packages', metavar='pkg_glob', type=str, nargs='+', help='the name of a package to upgrade or install')

        parser.add_argument('-a', '--all', action='store_true', help='Do with all the installed packages')
        parser.add_argument('-A', '--afterinstall', nargs=1, help='Run the specified command after each installation')
        parser.add_argument('-B', '--beforeinstall', nargs=1, help='Run the specified command before each installation')
        parser.add_argument('-f', '--force', action='store_true', help='Force the upgrade of a port even if it is to be a downgrade or just a reinstall')
        parser.add_argument('-F', '--fetch-only', action='store_true', help='Only fetch distfiles or packages. Do not build or install anything')
        parser.add_argument('-I', '--show-info', action='store_true'. help='Show installed packages')
        parser.add_argument('-k', '--keep-going', action='store_true', help='Force the upgrade of a port even if some of the requisite ports have failed to upgrade')
        parser.add_argument('-n', '--no-execute', action='store_true', help='Do not upgrade any ports, but just show what would be done')
        parser.add_argument('-r', '--recursive', action='store_true', help='Do with all those depending on the given packages as well')
        parser.add_argument('-R', '--upward-recursive', action='store_true', help='Do with all those required by the given packages as well / Fetch recursively if -F is specified')
        parser.add_argument('-u', '--update-status', action='store_true', help='Display packages with available updates')
        parser.add_argument('-v', '--verbose', action='store_true', help='Be verbose')

        args = parser.parse_args()
        #print args.accumulate(args.packagess)
        return # return command output...


    def check_version(self, prog):
        # query database for program details
        # perform method for checking for updates (cli or website or...)

