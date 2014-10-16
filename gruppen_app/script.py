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
Global variables and status information for the Python script.
Parallel to the app module which (differently) contains PyQt.QApplication() specific data.
"""

import os

from report import *

# Target directory
target_directory = ''

def absolute_path(directory):
    """Return an absolute path to directory.
    If directory is empty, use current working directory.
    If it's an absolute path, simply return it.
    If it's a relative path, interpret that starting with the cwd."""
    if not directory:
        return os.getcwd()
    elif not os.path.isabs(directory):
        return os.path.normpath(os.path.join(os.getcwd(), directory))
    else:
        return directory

    
# #########
# Verbosity

# Verbosity level constants
VERBOSITY_QUIET = 0
VERBOSITY_ERROR = 1
VERBOSITY_WARNING = 2
VERBOSITY_DEFAULT = 3
VERBOSITY_VERBOSE = 4
VERBOSITY_DEBUG = 5

verbosity_levels = {
    'quiet': VERBOSITY_QUIET, 
    'error': VERBOSITY_ERROR, 
    'warning': VERBOSITY_WARNING, 
    'default': VERBOSITY_DEFAULT, 
    'verbose': VERBOSITY_VERBOSE, 
    'debug': VERBOSITY_DEBUG}

# Verbosity level of the script
verbosity_level = VERBOSITY_DEFAULT

# Match verbosity level from the command line argument
# (no error checking necessary as they are already
#  checked from the argparse library)
def set_verbosity(argument):
    global verbosity_level
    
    verbosity_level = verbosity_levels[argument]

def verbosity():
    """Return the string representing the verbosity of the script"""
    for key, value in verbosity_levels.items():
        if value == verbosity_level:
            return key

# #####################
# Global Project object

# globally available project object
proj = None

def open_project(args):
    """Create a Project() object, make it globally available and return it."""
    global proj
    # try to open a project
    try:
        from project import Project
        proj = Project(args)
        return proj
    except AssertionError, e:
        error(e)
        sys.exit(1)

def pretty_floats(obj):
    """Format floating point numbers (recursively) as percentage strings.
    Used for exporting completion data to JSON."""
    if isinstance(obj, float):
        return '{:.2%}'.format(obj / 100)
    elif isinstance(obj, dict):
        return dict((k, pretty_floats(v)) for k, v in obj.items())
    elif isinstance(obj, (list, tuple)):
        return map(pretty_floats, obj)             
    return obj

