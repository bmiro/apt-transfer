#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from sys import argv

##########################################################################
#   This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
#   This program is distributed in the hope that it will be useful,      #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
##########################################################################



VERSION="pre-alpha"

SOURCES_VERSIONS=[# Debian
                 "oldstable", "stable", "testing", "unstable", "experimental",\
                 "buzz", "rex", "bo", "hamm", "slink", "potato","woody", \
                 "sarge", "etch", "lenny", "squeeze", "wheezy", "jessie",\
                 "sid",\
                 # Ubuntu
                 "warty", "hoary", "breezy", "dapper", "edgy", "feisty", \
                 "gutsy", "hardy", "intrepid", "jaunty", "karmic", \
                 "maverick", "lucid", "natty", "oneiric", "precise", "quantal"]

SOURCES_SECTIONS=["main", "contrib", "non-free",          # Debian
                  "universe", "multiverse", "restricted"] # Ubuntu specific

COMMAND_LIST = ["mirror", "initialize", "update", "start", "stop", "clean"]

# apt-transfer-server mirror http://ftp.debian.org/debian/ \
#                            testing main contrib non-free \
#                            --dest-path /var/www/debian-mirror


def print_help():
    print("apt-transfer %s \n" % VERSION)
    print("Usage: apt-transfer-server command command-options\n")
    print("apt-transfer-server is a tool to share the list of installed \
packages on the \n machine and let another one with the apt-transfer-client to \
install them. \n It also can be used to create local mirrors of the debian-base \
repositories.\n")
    print("\nCommands:")
    print("\tmirror *source* - create a mirror of the given repository \
at the source with\n\t\t\tthe same sintax as sources.list to the given path.")
    print("\t\t[--dest-path *path*] - specify were the mirror will be stored")
    print("\tinitilize - prepare the system to start the service")
    print("\tupdate - updates the mirror packages")
    print("\tstart - start mirror server and allows access to packages list")
    print("\tstop - stop mirror server and denies access to packages list")
    print("\tclean - delete the full repository mirror")

    print("\nExamles:")
    #TODO put examples of each invocation


""" Argument parsing.
" @return: dict with command name and correspoding parameters depeding
" on which options has de command.
"""
def arg_parsing(arg_v):

    print arg_v

    command = arg_v[1]

    if not command in COMMAND_LIST:
        return {"error" : "I don't understand the command " + command}


    if command == "mirror":
        url = arg_v[2]
        if not validate_url(url):
            return {"error" : "I don't understand the mirror url " + url}

        version = arg_v[3]
        if not version in SOURCES_VERSION:
            return {"error" : "I don't understand the version " + version}

        sections = []
        i = 4 # The current index of the arg_v
        while arg_v[i] in SOURCES_SECTION:
            sections += arg_v[i]

        if not sections:
            return {"error" : "I don't detect any software section (ie main)"}


    elif command == "initialize":

    elif command == "update":

    elif command == "start":

    elif command == "stop":

    elif command == "clean":
        

    


    return None


def validate_url(url):
    return True


def mirror():
    pass


def initialize():
    pass


def start():
    pass


def stop():
    pass


def clean():
    pass


if __name__=='__main__':

    arg = arg_parsing(argv)

    if "error" in arg:
        print_help()
        exit()


    if arg["command"] == "mirror":
        mirror(arg["url"], arg["distro"], arg["section_list"], arg["path"])

    elif arg["command"] == "initialize":
        initialize()

    elif arg["command"] == "update":
        update(arg["url"], arg["distro"], arg["section_list"])

    elif arg["command"] == "start":
        start()

    elif arg["command"] == "stop":
        stop()

    elif arg["command"] == "clean":
        clean()
    
    else:
        print("Chuck Norris is dead.")

