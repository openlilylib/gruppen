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

import os, sys
from collections import Counter
import datetime
import json

import voicerow
from segment import parse_segment_meta_fields
import status
from report import *
from script import pretty_floats


class SegmentGrid(object):
    """Represents the two-dimensional array of segments"""
    def __init__(self, status):
        chat('Create SegmentGrid() object')
        
        self.owner = status
        self.project = self.owner.project
        self.vcs = self.project.vcs
        self._voices = {}
        self._completion = {}
        self._segments_completion = {}
        self._deletions = {}
        self._review_branches = []
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
        
    def add_voices(self, voice_names):
        """Add multiple VoiceRow objects, their names being passed as a list."""
        for v in voice_names:
            self.add_voice(v)
        
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

    def _generate_deletions(self):
        """Generate deletion data, ensuring that
        voices without deleted files get at least empty entries."""
        self._deletions = self.vcs.deletions()
        for v in self.voice_names():
            if not v in self._deletions:
                self._deletions[v] = {}
                debug("emtpy voice {} added.".format(v))
        debug(json.dumps(self._deletions, sort_keys = True, indent = 2))

    def deleted_by(self, voice, segment):
        """Return the name of the contributor who has deleted the given file.
        Returns an empty string if the file hasn't been deleted or noone can
        be reliably determined."""
        if not self._deletions:
            self._generate_deletions()
        return self._deletions[voice][segment]
        
    def deletions(self):
        if not self._deletions:
            self._generate_deletions()
        return self._deletions
        
    def invalidate_completion_data(self):
        """Delete all completion data to force
        their regeneration for next access."""
        self._completion = {}
        self._segments_completion = {}
        for v in self._voices:
            self._voices[v]._completion_data = {}
        
    def metadata(self):
        return {
            'dateTime': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), 
            'voiceCount': self.voice_count(), 
            'branch': self.vcs.current_branch(), 
            'reviewBranches': self.review_branches(), 
            'currentCommit': self.vcs.last_commit(), 
            'totalCommits': self.vcs.total_commits(), 
            'contributors': self.vcs.contributors(), 
            'segmentsInfo': self.segments_info(), 
            'completion': self.completion() 
            }

    def _review_branch(self, branch_name):
        """Return a dictionary for the given review branch.
        Update affected segments' status."""
        result = {'name': branch_name[len('origin/review/'):], 
                  'segments': self.vcs.changed_segments(branch_name)}
        return result
        
    def review_branches(self):
        """Return a list containing ready-for-review branches.
        If that hasn't been generated it will be done for the
        first time, and all affected segments will be updated."""
        if self._review_branches:
            return self._review_branches
        
        info('Parse ready-for-review branches')
        for review_branch in self.vcs.review_branches():
            chat("review branch {}".format(review_branch))
            
            # create new review-branch entry for metadata
            rb = {'name': review_branch[len('origin/review')+1:], 
                  'segments': []}

            # Get relevant base data from Git to parse non-checked-out branch information
            merge_base = ''.join(self.vcs._run_command('merge-base HEAD {}'.format(review_branch)))
            affected_files = self.vcs.exec_('diff --name-status {m} {o} {d}'.format(
                                        m = merge_base, 
                                        o = review_branch, 
                                        d = self.project['paths']['music']))
            
            for line in affected_files:
                # parse line
                operation = line[0]
                file_name = line[1:].lstrip()
                voice, seg_file = os.path.split(file_name[len(self.project['paths']['music'])+1:])
                seg_name = os.path.splitext(seg_file)[0]
                
                # get Segment object
                seg_obj = self[voice][seg_name]
                
                # handle files that are deleted on the review branch
                if operation == 'D':
                    seg_obj.deleted = True
                    seg_obj.meta_fields = {'deleted-by': rb['name']}
                    self.deletions()[voice][seg_name] = rb['name']
                else:
                    # get file content from the review branch
                    content = self.vcs.exec_('show {b}:{f}'.format(
                                             b = review_branch, 
                                             f = file_name))
                    # parse content from the review branch and apply to segment object
                    seg_obj.meta_fields = parse_segment_meta_fields(content)
                    
                # mark segment as ready-for-review
                seg_obj.meta_fields['review-branch'] = rb['name']
                
                # add segment to branch's list of affected segments
                rb['segments'].append((voice, seg_name))
            
            # finally append the generated dict to the output list
            self._review_branches.append(rb)
        
        return self._review_branches
        
    def segment_completion(self, segment_name):
        """Return completion data for a vertical segment"""
        
        # data is cached
        if segment_name in self._segments_completion:
            return self._segments_completion[segment_name]
            
        # init new dict
        self._segments_completion[segment_name] = sc = status.completion_entries.copy()
        
        # count status of segments
        for v in self._voices:
            sc[self._voices[v][segment_name].status()] += 1
        
        # calculate remaining values
        sc['total'] = self.voice_count()
        sc['valid'] = sc['total'] - sc['deleted']
        sc['completion'] = sc['reviewed'] / sc['valid'] * 100 if sc['valid'] > 0 else 100

        return sc

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

    def to_json(self, indent_level = 1):
        """Return a dictionary with to_json() objects for all voices."""
        
        info('Generate JSON data for SegmentGrid()')
        
        result = {'metadata': self.metadata(), 
                  'data': []}
        for v in self.project['voice_names']:
            result['data'].append(self._voices[v].to_json())
        if indent_level < 0:
            indent_level = None
        return json.dumps(pretty_floats(result), sort_keys = True, indent = indent_level)
        
    def voice_count(self):
        """Return the number of voices in the project"""
        return len(self._voices)
        
    def voice_names(self):
        """Return the project's list of voice_names"""
        return self.project['voice_names']
