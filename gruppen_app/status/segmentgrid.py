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

from __future__ import division

import datetime

import voicerow
import status

class SegmentGrid(object):
    """Represents the two-dimensional array of segments"""
    def __init__(self, status):
        self.owner = status
        self.project = self.owner.project
        self.vcs = self.project.vcs
        self._voices = {}
        self._completion = {}
        self.modified = False
        

    def __getitem__(self, voice_name):
        """Return a VoiceRow as if we were a dictionary."""
        return self._voices[voice_name]
        
    def __iter__(self):
        """Iterate over voices in the order given by self._voice_list."""
        for v in self._voice_list:
            yield self.voices[v]
    
    def _add_dicts(self, a, b):
        """Return the 'sum' of two dictionaries.
        values for keys existing in both dicts are added,
        otherwise the key will be added."""
        return dict(Counter(a) + Counter(b))
        
    def add_voice(self, voice_name):
        """Add a VoiceRow object and let it parse the directory"""
        if not voice_name in self.voice_names():
            self.project['voice_names'].append(voice_name)
        self._voices[voice_name] = voicerow.VoiceRow(self, voice_name)
        
    def completion(self):
        """Return a dictionary with statistical completion data"""
        
        # the dictionary is cached
        if self._completion:
            return self._completion
        
        self._completion = status.completion_entries.copy()
        for v in self._voices:
            # "add" the completion dict values of the voice to the current one
            self._completion = self._add_dicts(self._completion, self._voices[v].completion())
        
        # recalculate the completion ratio
        self._completion['completion'] = self._completion['reviewed'] / self._completion['valid'] * 100
        return self._completion

    def metadata(self):
        return {
            'dateTime': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), 
            'voiceCount': self.voice_count(), 
            'completion': self.completion(), 
            'branch': self.vcs.current_branch(), 
            'currentCommit': self.vcs.last_commit(), 
            'totalCommits': self.vcs.total_commits(), 
            'contributors': self.vcs.contributors(), 
            'segmentsInfo': self.segments_info()
            }

        
    def segment_completion(self, segment_name):
        """Return completion data for a vertical segment"""
        states = {
            'entered': 0, 
            'reviewed': 0, 
            'deleted': 0, 
            'not-done': 0}
        for v in self._voices:
            states[self._voices[v][segment_name].status()] += 1

        total = self.voice_count() - states['deleted']
        processed = states['reviewed']
        percentage = (processed / total * 100) if total > 0 else 100
        
        return ('%.2f' % percentage, 
                str(processed), 
                str(total))
                
    def segment_names(self):
        """Return the project's list of segment_names"""
        return self.project['segment_names']

    def segments_info(self):
        """Return a list with name and completion info on all segments.
        This has to be a list because"""
        result = []
        for seg in self.segment_names():
            result.append({
                'name': seg, 
                'completion': self.segment_completion(seg)
                })
        return result
        
    def to_json(self):
        """Return a dictionary with to_json() objects for all voices."""
        result = [{'metadata': self.metadata()}]
        
#        for v in self._voices:
#            result[v] = self._voices[v].to_json()
        return result
        
    def voice_count(self):
        """Return the number of voices in the project"""
        return len(self._voices)
        
    def voice_names(self):
        """Return the project's list of voice_names"""
        return self.project['voice_names']
