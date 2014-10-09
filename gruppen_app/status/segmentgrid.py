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
Segment grid representing the progress states of all segments
"""

class SegmentGrid(object):
    """Represents the two-dimensional array of segments"""
    def __init__(self, status):
        self.owner = status
        self.project = self.owner.project
        self.vcs = self.project.vcs
        self._voices = {}
        self._completion = None
        self.modified = False
        

    def __iter__(self):
        """Iterate over voices in the order given by self._voice_list."""
        for v in self._voice_list:
            yield self.voices[v]
    
    def segment_names(self):
        return self.project['segment_names']

    def voice_names(self):
        return self.project['voice_names']
