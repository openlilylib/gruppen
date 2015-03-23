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
Segment template
"""

import os, sys
import script
from report import *

class CellTemplate(object):

    def __init__(self, filename):
        self._content = self._read(filename)

    def _read(self, filename):
        """Load the template for segments
        from a template file."""
        try:
            f = open(filename)
            result = f.readlines()
            f.close()
            return result
        except:
            # for now simply re-throw the exception
            raise

    def content(self):
        """
        Return the content as a single string
        """
        return ''.join(self._content)