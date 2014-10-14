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

from __future__ import division

import os

import segment
import status

class VoiceRow(object):
    def __init__(self, segment_grid, voice_name):
        self.owner = segment_grid
        self.voice_name = voice_name
        self.project = self.owner.project
        self.vcs = self.project.vcs
        self._segments = {}
        self._completion_data = {}
        self._dir = os.path.join(self.project['paths']['music'], voice_name)
        
        for seg in self.segment_names():
            self._segments[seg] = self.read_segment(seg)
    
    def __getitem__(self, segment_name):
        """Return a segment object as if we were a dictionary."""
        return self._segments[segment_name]
        
    def _calculate_statistics(self):
        """Calculate and cache statistics for the row"""
        states = {}
        for s in status.segment_states:
            states[s] = 0
            
        for seg in self._segments:
            states[self._segments[seg].status()] += 1
        self._completion_data = status.completion_entries.copy()
        self._completion_data['total'] = self.project.segment_count()
        self._completion_data['valid'] = self._completion_data['total'] - states['deleted']
        self._completion_data['entered'] = states['entered']
        self._completion_data['reviewed'] = states['reviewed']
        self._completion_data['deleted'] = states['deleted']
        self._completion_data['not-done'] = states['not-done']
        self._completion_data['completion'] = self._completion_data['reviewed'] / self._completion_data['valid'] * 100
        
    def completion(self):
        """Return a dictionary with statistical completion data."""
        if not self._completion_data:
            self._calculate_statistics()
        return self._completion_data.copy()
        
    def completion_tuple(self):
        """Return a tuple with strings for
        - completion percentage
        - reviewed segments
        - total valid segments"""
        return ('%.2f' % self.count('completion'), 
                str(self.count('reviewed')), 
                str(self.count('valid')))
        
    def count(self, type):
        """Return the number of segments of a given type"""
        if not self._completion_data:
            self._calculate_statistics()
        return self._completion_data[type]
        
    def to_json(self):
        """Return a JSON compatible representation of the part row."""
        result = {
            'completion': self.completion(), 
            'segments': {}}
        for seg in self._segments:
            if self._segments[seg].status() != 'not-done':
                result['segments'][seg] = self._segments[seg].to_json()
        return result

    def read_segment(self, segment_name):
        """Return a new Segment object"""
        return segment.Segment(self, segment_name)

    def segment_names(self):
        """Return the project's list of segment_names"""
        return self.project['segment_names']
        
