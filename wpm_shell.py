#!/usr/bin/env python

import os, argparse, logging
import wpm_db, db_wrapper
from wpm_app import app
import time
from datetime import date
from datetime import timedelta


class shell:
    # __init__
    # Parameters: logFileName is string
    # Initializes the command line interface for Windows Package Manager
    # logFileName is a relative path to the log file 
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
    # Parameters: argv is string
    # Takes in sys.argv, trims off sys.argv[0] and run command
    # TODO: This needs to be fixed to print help if programs aren"t supplied
    def cmd(self, argv=""):
        if len(argv) < 2:
            self.parser.print_help()
            return -1
        else:
            self.args = self.parser.parse_args(argv[1:])
            return 0

# processCmd
# Custom action to interpret argument flags, direct execution database queries and application calls
# Parameters: argpase.Action is the action method of the argparse for class
# TODO: overload print function to check for flag.verbose
class processCmd(argparse.Action):

    # TODO: Get rid of ugly globals
    global mydb
    mydb = wpm_db.db("dbFile", "dbLog")
    global appLogFileName
    appLogFileName = "appLog"

    def __call__(self, parser, flag, pkg_list, option_string=None):


        # Inform user of incomplete program functionality if used
        self.notImplemented(flag)

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
                print("DEMO: Query for dependencies of %s" % pkg)

                # TODO: Use data from db queries
                # append to execution list
                for deps in test_depends:
                    print("DEMO: Adding %s as a dependency to %s" % (deps, pkg))
                    pkg_order.insert(pkg_order.index(pkg)+1, deps)

            # Check on the status of programs that depend on `pkg"
            if flag.upward_recursive:
                test_updepends = ["Udep1", "Udep2", "Udep3"]
                print("DEMO: Query for programs which have %s as a dependency" % pkg)

                # TODO: Use data from db queries
                # append to execution list
                for deps in test_updepends:
                    print("DEMO: Adding %s as a dependency to %s" % (deps, pkg))
                    pkg_order.insert(pkg_order.index(pkg)+1, deps)

        #if flag.verbose:
        #print("Order of execution: %s\n" % pkg_order[::-1])


        # If no packages implemented in execution:
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
            # Pass in pkg_order in reverse to preseve execution order
            if (flag.command == "info"):
                self.cmdInfo(pkg_order[::-1], flag)
            elif (flag.command == "update"):
                self.cmdUpdate(pkg_order[::1], flag)
            elif (flag.command == "install"):
                self.cmdInstall(pkg_order[::1], flag)
            elif (flag.command == "remove"):
                self.cmdRemove(pkg_order[::1], flag)
            else:
                print("Problem. Shouldn\'t ever make it here\n")


    # cmdInfo
    # Parameters: pkg and flag are lists
    # Takes a list of packages and returns version number and up-to-date status
    # Will attempt to download updates if available and flag.no_execute not set
    # TODO: Move download functionality into `update` 
    def cmdInfo(self, pkg, flag):

        if pkg == None:
            # Query for all installed packages
            prog_list = db_wrapper.get_applications(mydb)

        else:
            # Query db for requested package
            prog_list = (True,  pkg )
            #print(prog_list[1])

        # Print header to the package table
        print("")
        print("{0:15s} {1:10s} {2:10s}").format("Name", "Version", "Up-to-date?")
        print("{0:15s} {1:10s} {2:10s}").format("----", "-------", "-----------")
        for p in prog_list[1]:
            result = db_wrapper.get_app_version(mydb, p)

            pkg_current = "Y"

            if flag.keep_going or (result[0] == True and result[1] != []) :

                if result[1] != []:
                    pkg_version = result[1][0]
                else:
                    pkg_version = "N/A"
                    pkg_current = "Not found"

            else:
                print("{0:15s} {1:10s} {2:10s}").format(p, "N/A", "Not found")
                continue


            # Check if new version has been checked "recently"
            # TODO: Define check frequency in settings.py
            if result[1] != []:
                last_checked = date.fromtimestamp(float(result[1][1]))
                today = date.fromtimestamp(time.time())

                # Check for new versions only once a day
                if flag.force or (today - last_checked ) > timedelta(days=1):
                    pass
                    # Check if out of date
                        # download new version if available
                        # set out-of-date

                    # Download updates if they are available and !(flag.no_execute)
                    if not flag.no_execute:
                        prog = app(pkg, mydb, appLogFileName)
                        #prog.dlUpdates()


                else:
                    # If version has been checked already...
                    pkg_current = "N"

                # if out of date and !(flag.no_execute):
                    #prog.dlUpdates()

            # Display installed packages, version and up to date status
            print("{0:15s} {1:10s} {2:10s}").format(p, pkg_version, pkg_current)

        print("")

    # cmdUpdate
    # Parameters: pkg and flag are lists
    # Takes in a list of packages and downloads new packages and updates the old packages
    # Updates the version references in the database 
    def cmdUpdate(self, pkg, flag):
        return

        if pkg == None:
            # Query for all installed packages
            prog_list = db_wrapper.get_applications(mydb)

        else:
            # Query db for requested package
            prog_list = (True,  pkg )
            #print(prog_list[1])
        for p in prog_list[1]:
            pass

            # Check for new versions only once a day
            if flag.force or (today - last_checked ) > timedelta(days=1):
                pass
                # Check if out of date
                    # download new version if available
                    # set out-of-date

                # Download updates if they are available and !(flag.no_execute)
                if not flag.no_execute:
                    prog = app(pkg, mydb, appLogFileName)
                    #prog.dlUpdates()

            # if out of date and !(flag.no_execute):
                #prog.dlUpdates()

    # cmdInstall
    # Parameters: pkg and flag are lists
    # Takes in a list of packages, downloads and installs them, then registers them with the database
    def cmdInstall(self, pkg, flag):
        pass

    # cmdRemove
    # Parameters: pkg and flag are lists
    # Takes in a list of packages, and uninstalls them and unregisters them with the database
    def cmdRemove(self, pkg, flag):
        pass

    # For demo purposes
    def notImplemented(self, flag):


        ## Options
        if flag.after_install:
            print("-A functionality has not yet been implemented")

        if flag.before_install:
            print("-B functionality has not yet been implemented")

        if flag.emit_summaries:
            print("-e functionality has not yet been implemented")

        if flag.fetch_only:
            print("-F functionality has not yet been implemented")

        if flag.log_file != os.curdir:
            print("-l functionality has not yet been implemented")

        if flag.omit_check:
            print("-O functionality has not yet been implemented")

        if flag.verbose:
            print("-v functionality has not yet been implemented")

        if flag.exclude:
            print("-x functionality has not yet been implemented")

        ## Commands
        if flag.command == "update":
            print("\"Update\" functionality has not yet been implemented")

        if flag.command == "install":
            print("\"Install\" functionality has not yet been implemented")

        if flag.command == "remove":
            print("\"Remove\" functionality has not yet been implemented")

