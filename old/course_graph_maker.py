#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Eytan
#
# Created:     02/07/2014
# Copyright:   (c) Eytan 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import sys
import subprocess
from optparse import OptionParser
from Course import Course
import load_db
import os
import traceback


def main(argv):
    debug = False
    if "debug" in argv:
        debug = True
    config_file = "/".join(argv[0].split("/")[0:-1])
    if config_file != "":
        config_file += "/" +"config"
    else:
        config_file = "./config"
    if debug:
        print(config_file)
    with open(config_file, 'r') as config:
        dot_exec = config.readline().rstrip() # Modified to Linux location of dot
    COURSE_NOT_FOUND = "Course not in database"

    #create a dictionary of courses
    if debug:
        print("loading courses names")
    courses = load_db.get_courses("courses_db.txt")
    #commmand line parsing done right ;P
    parser = OptionParser()
    parser.add_option("-d", "--dot", dest="dot" )
    parser.add_option("--depth", dest="depth" )
    parser.add_option("-f", "--faculty", dest="facs", action='append' )
    parser.add_option("--file", dest="out_file")

    (options, args) = parser.parse_args(argv)
    if options.dot:
        dot_exec = options.dot
    graph_open_depth = None
    if options.depth:
        try:
            graph_open_depth = int(options.depth)
        except:
            graph_open_depth = None

    if debug:
        print("starting writing")
    if len(args) > 1:
        if args[1] not in courses:
            if debug:
                print(COURSE_NOT_FOUND)
            print(Course(111111, "")._make_fail_svg())
            return
        if options.out_file:
            if debug:
                print("writing to file")
            courses[args[1]].write_nexts_to_stream(dot_exec, args[2], depth=graph_open_depth, faculties=options.facs)
        else:
            if debug:
                print("writing to stream")
            courses[args[1]].write_nexts_to_stream( dot_exec , depth=graph_open_depth, faculties=options.facs)


if __name__ == '__main__':
    try:
        main(sys.argv[0:])
    except:
        traceback.print_exc()
        exit (1)
