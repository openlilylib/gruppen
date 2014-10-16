#!/usr/bin/env python
#-*- coding:utf-8 -*-

# This file is part of the Gruppen project
# https://git.ursliska.de/openlilylib/gruppen
#
# Copyright (c) 2014 by Urs Liska and others
# (as documented by the Git history)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,   
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.


"""
Command line parsing.
This is in a module so the app and all scripts can use it.
"""

import sys
import os
import argparse

import info
import script

# instantiate command line parser
parser = None
def create_parser():
    global parser
    parser = argparse.ArgumentParser(
        usage = ("{scriptname} [options]").format(scriptname = info.scriptname),
        version = "{appname} {scriptname} {version}".format(
            appname = info.appname, 
            scriptname = info.scriptname, 
            version = info.version),
        description = ("A LilyPond Project Manager"))
    parser.add_argument('-d', '--directory', 
        help=("Root directory of the project, relative or absolute path, " +
              "not passing this argument means 'current directory'."))
    parser.add_argument('-p', '--properties-file', 
        help=("Relative path to JSON file specifying project properties " +
              "(path etc.). Defaults to 'project/properties.json'. If such " +
              "a file is not present, default values are used."))
    parser.add_argument('-V', '--verbosity', 
        default = 'default', 
        choices = ['debug', 'verbose', 'default', 'warning', 'error', 'quiet'], 
        help = ("Detail level of information output."))
    parser.add_argument('-l', '--logfile', 
        help = ("Use the given logfile (relative to repository " +
                "root) and append --verbose output to that."))
    parser.add_argument('-m', '--mailto', 
        help = ("Do not print any output but try to send the output " +
                "of the script to the given email address"))

    # Make sure debugger options are recognized as valid. These are passed automatically
    # from PyDev in Eclipse to the inferior process.
    if "pydevd" in sys.modules:
        parser.add_option('-v', '--vm_type')
        parser.add_option('-a', '--client')
        parser.add_option('-p', '--port')
        parser.add_option('-f', '--file')
        parser.add_option('-o', '--output')

create_parser()


def parse():
    """Parse command line and return options and files (if applicable).
    Check project directory along the way (set project properties
    or raise an exception)."""

    args = sys.argv
    if os.name == 'nt' and args and 'python' in os.path.basename(args[0]).lower():
        args = args[2:]
    else:
        args = args[1:]
    args = vars(parser.parse_args(args))
    
    script.set_verbosity(args['verbosity'])   
    
    # set external target directory if passed
    script.target_directory = args['target_directory'] if args['target_directory'] else ''
    
    return args
