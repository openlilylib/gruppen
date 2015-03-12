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
Voice (in the sense of a voice directory)
"""
import os, sys
import script
import segments
from report import *

class Voice(object):

    def __init__(self, project, properties):
        self._properties = properties
        self._properties['project'] = project
        self._segment_names = self['project']['segment_names']
        self._root_dir = project['paths']['root']
        self.music_dir = os.path.join(self._root_dir,
                                      project['paths']['music'],
                                      properties['basename'])

        # Safety check - may be done smarter in the future:
        if os.path.exists(self.music_dir):
            error(("Target directory already exists:\n  {}\n" +
                "I'm not smart enough yet, aborting.").format(self.music_dir))
            sys.exit(1)

        self.segments = segments.Segments(self)


    def __getitem__(self, property):
        """Return project property - as if Project were a dict object"""
        return self._properties[property]
