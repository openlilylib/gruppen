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
Row representing all segments in a voice
"""

import os

class VoiceRow(object):
    def __init__(self, segment_grid, voice_name):
        self.owner = segment_grid
        self.project = self.owner.project
        self.vcs = self.project.vcs
        self._segments = {}
        self._dir = os.path.join(self.project['paths']['music'], voice_name)
    
    def __getitem__(self, segment_name):
        """Return a segment object as if we were a dictionary."""
        return self._segments[segment_name]
        
