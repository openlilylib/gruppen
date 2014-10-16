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
Generic interface to report status and debug data 
"""

import script 

def debug(msg):
    """Report any data, depending on the command line configuration"""
    if script.verbosity_level >= script.VERBOSITY_DEBUG:
        print msg

def chat(msg):
    """Print additional status information"""
    if script.verbosity_level >= script.VERBOSITY_VERBOSE:
        print msg
        
def error(msg):
    """Print an error message"""
    if script.verbosity_level >= script.VERBOSITY_ERROR:
        print "Error:\n", msg

def info(msg):
    """Print a default information (e.g. progress of the script)."""
    if script.verbosity_level >= script.VERBOSITY_DEFAULT:
        print msg
    
def warn(msg):
    """Print a warning."""
    if script.verbosity_level >= script.VERBOSITY_WARNING:
        print 'Warning:\n', msg
    
