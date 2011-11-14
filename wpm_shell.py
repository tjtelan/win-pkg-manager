#!/usr/bin/env python

import os, argparse, logging
from wpm_db import db
from wpm_app import app

class shell:
    # __init__
    #
    # Initializes the command line interface for Windows Package Manager
    def __init__(self, logFileName):

        self.parser = argparse.ArgumentParser(description="FreeBSD ports inspired package manager for Windows", prefix_chars="-")

        # Simplified usage message
        self.parser = argparse.ArgumentParser(prog="winpkg", usage="%(prog)s [options] command ... [pkg_name]", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # Optional flags
        self.parser.add_argument("-a", "--all", action="store_true", help="Do with all the installed packages")
        self.parser.add_argument("-A", "--afterinstall", metavar="CMD", nargs=1, help="Run the specified command after each installation")
        self.parser.add_argument("-B", "--beforeinstall", metavar="CMD", nargs=1, help="Run the specified command before each installation")
        self.parser.add_argument("-e", "--emit-summaries", action="store_true", help="Emit summary info after each package processing")
        self.parser.add_argument("-f", "--force", action="store_true", help="Force the upgrade of a package even if it is to be a downgrade or just a reinstall")
        self.parser.add_argument("-F", "--fetch-only", action="store_true", help="Only fetch packages. Do not build or install anything")
        self.parser.add_argument("-k", "--keep-going", action="store_true", help="Force the upgrade of a port even if some of the requisite packages have failed to upgrade")
        self.parser.add_argument("-l", "--log-file", metavar="PATH", nargs=1, type=str, default=os.curdir, help="Use log file at specified location")
        self.parser.add_argument("-n", "--no-execute", action="store_true", help="Do not upgrade any packages, but just show what would be done")
        self.parser.add_argument("-O", "--omit-check", action="store_true", help="Omit sanity checks for dependencies")
        self.parser.add_argument("-r", "--recursive", action="store_true", help="Do with all those depending on the given packages as well")
        self.parser.add_argument("-R", "--upward-recursive", action="store_true", help="Do with all those required by the given packages as well / Fetch recursively if -F is specified")
        self.parser.add_argument("-v", "--verbose", action="store_true", help="Be verbose")
        self.parser.add_argument("-x", "--exclude", metavar="GLOB", nargs="+", help="Exclude packages matching the specified glob pattern")

        # Positional arguments
        self.parser.add_argument("command", choices=["info", "update", "install", "remove"], action="store", help="")
        self.parser.add_argument("pkg_name", nargs="*", action=cmdProg, help="Package(s) to act on")

    # cmd
    #
    # Takes in sys.argv, trims off sys.argv[0] and run command
    # TODO: This needs to be fixed to print help if programs aren"t supplied
    def cmd(self, argv=""):
        if len(argv) < 2:
            self.parser.print_help()
            return -1
        else:
            self.args = self.parser.parse_args(argv[1:])
            #print("argv: %s" % argv[1:])
            #print("all_switch: =", self.args.all)
            return 0

# Custom action to control execution database queries and application calls
class cmdProg(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        #print("namespace: %r \nvalues: %r \noption_string %r" % (namespace, values, option_string))

        progs = []
        progs.extend(values)

        # "-a" flag implies upward and downward recursive
        if namespace.all:
            namespace.recursive = True
            namespace.upward_recursive = True

        # TODO: Build program execution list that looks like:
        #  [ prog1, prog1_depends, prog2, prog2_depends... ]

        for program in values:
            # Check on the status of dependencies of `program"
            if namespace.recursive:
                test_depends = ["dep1", "dep2", "dep3"]
                print("Query for dependencies of %s" % program)

                # append these programs to list progs
                for deps in test_depends:
                    print("Adding %s as a dependency to %s" % (deps, program))
                    progs.insert(progs.index(program)+1, deps)

            # Check on the status of programs that depend on `program"
            if namespace.upward_recursive:
                test_updepends = ["Udep1", "Udep2", "Udep3"]
                print("Query for programs which have %s as a dependency" % program)

                # append these programs to list progs
                for deps in test_updepends:
                    print("Adding %s as a dependency to %s" % (deps, program))
                    progs.insert(progs.index(program)+1, deps)

        print("Order of execution: %s\n" % progs)

        for program in reversed(progs):

            print("Performing %s on %s" % (namespace.command, program))

            #if namespace.verbose:
            print("Query for %s in db" % program)

            print("DB: Query for version info for %s" % program)
            print("DB: Check if %s has been checked for \'out-of-date-ness\' recently" % program)
            print("APP: Check for current version if needed\n")

            if (namespace.command == "info"):
                print("SHELL: Print name, current installed version, and newest version (if out of date), otherwise say \'up to date\'")
                print("(SHELL: May need to support wildcards? For uses like \'$ winpkg info *\' OR support input for 0 or more programs, with default all for 0)\n")
                print("DB: Possibly need a way to return all installed programs if run with no specific program")
            elif (namespace.command == "update"):
                print("APP: Go out and download installer")
                print("APP: Run through update script (This will need fitting to each program)")
                print("DB: Update version information for %s when complete\n" % program)
                print("(APP: Probably need to have functionality to update all installed programs when shell run with no program)")
            elif (namespace.command == "install"):
                print("(Install is assumed to be interactive in most cases, but could add functionality later to be batched)")
                print("SHELL: Ask for details for the installer (Programs will have to be fitted to this package manager)")
                print("DB: Create a new profile using those defaults")
                print("APP: Fetch and install using info from the DB\n")
            elif (namespace.command == "remove"):
                print("DB: Check for an uninstaller")
                print("APP: Run uninstaller if DB says there is one")
                print("APP: Run uninstall script, if you had to create one with the installer")
                print("APP: Respond with error if %s cannot be uninstalled with this tool" % program)
                print("DB: Remove profile from DB if successfullly removed\n")
            else:
                print("Problem. Shouldn\'t ever make it here\n")




