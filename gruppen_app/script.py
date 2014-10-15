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

VERBOSITY_MUTE = 0
VERBOSITY_QUIET = 1
VERBOSITY_DEFAULT = 2
VERBOSITY_VERBOSE = 3
VERBOSITY_DEBUG = 4

verbosity_level = VERBOSITY_DEFAULT

def set_verbosity(argument):
    global verbosity_level
    
    verbosity_levels = {
        'mute': VERBOSITY_MUTE, 
        'quiet': VERBOSITY_QUIET, 
        'default': VERBOSITY_DEFAULT, 
        'verbose': VERBOSITY_VERBOSE, 
        'debug': VERBOSITY_DEBUG}
    verbosity_level = verbosity_levels[argument]
