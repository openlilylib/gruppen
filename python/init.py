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

#
# main module of the python directory (standalone scripts)
# Every script should import this file to set up the environment
#

from __future__ import unicode_literals

import sys
import os
import argparse
import atexit

# append the _app path to Python's search path 
# so standalone scripts have direct access to the app's modules.

def we_are_frozen():
    # All of the modules are built-in to the interpreter, e.g., by py2exe
    return hasattr(sys, "frozen")

def module_path():
    encoding = sys.getfilesystemencoding()
    if we_are_frozen():
        return os.path.dirname(unicode(sys.executable, encoding))
    return os.path.dirname(unicode(__file__, encoding))

app_path = os.path.normpath(os.path.join(module_path(), '..', 'gruppen_app'))
sys.path.append(app_path)



# instantiate info object
import info
# add plain script name to info
info.scriptname = os.path.splitext(os.path.split(sys.argv[0])[1])[0]

# initialize command line parsing
import commandline


# Finishing of the script
import script
def exit_handler():
    script.proj.write_properties_to_json()

atexit.register(exit_handler)
    
