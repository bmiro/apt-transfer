#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from sys import argv


VERSION="pre-alpha"
AVALIABLE_SECTIONS=["main", "contrib", "non-free",          # Debian
                    "universe", "multiverse", "restricted"] # Ubuntu specific

# apt-transfer-server mirror http://ftp.debian.org/debian/ testing main contrib non-free --dest-path /var/www/debian-mirror
MIRROR_REGEX=r""
UPDATE_REGEX=r""


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

    return None


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

    if not arg:
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

