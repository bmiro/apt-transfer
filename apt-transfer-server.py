#!/usr/bin/env python3
#-*- coding: utf-8 -*-

VERSION="pre-alpha"

def print_help():
    print("apt-transfer %s \n" % VERSION)
    print("Usage: apt-transfer-server command command-options\n")
    print("apt-transfer-server is a tool to share the list of installed \
packages on the \n machine and let another one with the apt-transfer-client to \
install them. \n It also can be used to create local mirrors of the debian-base \
repositories.\n")
    print("\nCommands:")
    print("\tmirror *source* - create a mirror of the given repository at the \
source with\n\t\t\tthe same sintax as sources.list")
    print("\tinitilize - prepare the system to start the service")
    print("\tupdate - updates the mirror packages")
    print("\tstart - start mirror server and allows access to packages list")
    print("\tstop - stop mirror server and denies access to packages list")
    print("\tclean - delete the full repository mirror")


if __name__=='__main__':

    arg = arg_parsing()

    if !action:
        print_help()
        exit()


    if arg["action"] == "mirror":
        mirror(arg["url"], arg["distro"], arg["section_list"])

    elif arg["action"] == "initialize":
        initialize()

    elif arg["action"] == "update":
        update(arg["url"], arg["distro"], arg["section_list"])

    elif arg["action"] == "start":
        start()

    elif arg["action"] == "stop":
        stop()

    elif arg["action"] == "clean":
        clean()
    
    else:
        print("Chuck Norris is dead.")

