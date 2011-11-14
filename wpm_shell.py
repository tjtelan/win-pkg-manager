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
        # TODO: quiet flag?
        self.parser.add_argument("-a", "--all", action="store_true", help="Do with all the installed packages (implies -rR)")
        self.parser.add_argument("-A", "--after-install", metavar="CMD", nargs=1, help="Run the specified command after each installation")
        self.parser.add_argument("-B", "--before-install", metavar="CMD", nargs=1, help="Run the specified command before each installation")
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
        self.parser.add_argument("pkg_name", nargs="*", action=processCmd, help="Package(s) to act on")

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

# Custom action to interpret argument flags, direct execution database queries and application calls
# TODO: overload print function to check for flag.verbose
class processCmd(argparse.Action):
    def __call__(self, parser, flag, pkg_list, option_string=None):
        #print("flag: %r \nvalues: %r \noption_string %r" % (namespace, values, option_string))

        # Set custom log file location
        if flag.log_file:
            pass
            # Try to set location as log file path and name
            # Exit on fail


        pkg_order = []
        pkg_order.extend(pkg_list)

        # "-a" flag implies upward and downward recursive
        if flag.all:
            flag.recursive = True
            flag.upward_recursive = True

        # Program execution list looks like:
        # [ prog1, prog1_depends..., progN, progN_depends..., ]

        # TODO: Is one level of dependency checking sufficient?
        for pkg in pkg_list:
            # Check on the status of dependencies of `pkg"
            if flag.recursive:
                test_depends = ["dep1", "dep2", "dep3"]
                print("Query for dependencies of %s" % pkg)

                # TODO: Use data from db queries
                # append to execution list
                for deps in test_depends:
                    print("Adding %s as a dependency to %s" % (deps, pkg))
                    pkg_order.insert(pkg_order.index(pkg)+1, deps)

            # Check on the status of programs that depend on `pkg"
            if flag.upward_recursive:
                test_updepends = ["Udep1", "Udep2", "Udep3"]
                print("Query for programs which have %s as a dependency" % pkg)

                # TODO: Use data from db queries
                # append to execution list
                for deps in test_updepends:
                    print("Adding %s as a dependency to %s" % (deps, pkg))
                    pkg_order.insert(pkg_order.index(pkg)+1, deps)

        #if flag.verbose:
        print("Order of execution: %s\n" % pkg_order)


        # If no packages defined in execution:
            # `info` should spit out detail on all installed packages
            # `update` should attempt to update all installed packages

        # TODO: Feature creep - Should skip current program on ^C and move to next
        # TODO:               - if none or wildcards in pkg, Query for installed packages before entering loop

        if len(pkg_order) == 0 and (flag.command == "info" or flag.command == "update") :

            if flag.command == "info":
                self.cmdInfo(None, flag)
            else:
                self.cmdUpdate(None, flag)
        else:
            for pkg in reversed(pkg_order):

                #if flag.verbose:
#                print("Performing %s on %s" % (flag.command, pkg))
#                print("Query for %s in db" % pkg)
#
#                print("DB: Query for version info for %s" % pkg)
#                print("DB: Check if %s has been checked for \'out-of-date-ness\' recently" % pkg)
#                print("APP: Check for current version if needed\n")

                if (flag.command == "info"):
                    self.cmdInfo(pkg, flag)
                elif (flag.command == "update"):
                    self.cmdUpdate(pkg, flag)
                elif (flag.command == "install"):
                    self.cmdInstall(pkg, flag)
                elif (flag.command == "remove"):
                    self.cmdRemove(pkg, flag)
                else:
                    print("Problem. Shouldn\'t ever make it here\n")

    def cmdInfo(self, pkg, flag):
        pass

        # if pkg = None:
            # Query for all installed packages
        # else:
            # Query db
            # ()
            # throw error -- db not available

        # if flag.keep_going OR return true:
            # pass
        # else
            # throw error -- pkg not found


        # if pkg hasn't been version checked "recently" and !(flag.no_execute):
            # Check if out of date
                # download new version if available
                # set out-of-date
            # else:
                # set up-to-date

            # Update db, saying check was made

        # print pkg,  version number and up-to-date status

    def cmdUpdate(self, pkg, flag):
        pass
#        print("APP: Go out and download installer")
#        print("APP: Run through update script (This will need fitting to each program)")
#        print("DB: Update version information for %s when complete\n" % pkg)
#        print("(APP: Probably need to have functionality to update all installed programs when shell run with no program)")

    def cmdInstall(self, pkg, flag):
        pass
#        print("(Install is assumed to be interactive in most cases, but could add functionality later to be batched)")
#        print("SHELL: Ask for details for the installer (Programs will have to be fitted to this package manager)")
#        print("DB: Create a new profile using those defaults")
#        print("APP: Fetch and install using info from the DB\n")

    def cmdRemove(self, pkg, flag):
        pass
#        print("DB: Check for an uninstaller")
#        print("APP: Run uninstaller if DB says there is one")
#        print("APP: Run uninstall script, if you had to create one with the installer")
#        print("APP: Respond with error if %s cannot be uninstalled with this tool" % pkg)
#        print("DB: Remove profile from DB if successfullly removed\n")

