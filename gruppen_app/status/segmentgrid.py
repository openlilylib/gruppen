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

from collections import Counter
import datetime
import json

import voicerow
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
        self._deletions = None
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

    def deleted_by(self, voice, segment):
        """Return the name of the contributor who has deleted the given file.
        Returns an empty string if the file hasn't been deleted or noone can
        be reliably determined."""
        if not self._deletions:
            self._deletions = self.vcs.deletions()
            # add empty records for voices without deleted files
            for v in self.voice_names():
                if not v in self._deletions:
                    self._deletions[v] = {}
            debug(json.dumps(self._deletions, sort_keys = True, indent = 2))
        return self._deletions[voice][segment]
        
    def metadata(self):
        return {
            'dateTime': datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), 
            'voiceCount': self.voice_count(), 
            'completion': self.completion(), 
            'branch': self.vcs.current_branch(), 
            'reviewBranches': self.review_branches(), 
            'currentCommit': self.vcs.last_commit(), 
            'totalCommits': self.vcs.total_commits(), 
            'contributors': self.vcs.contributors(), 
            'segmentsInfo': self.segments_info()
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
        for rb in self.vcs.review_branches():
            chat("review branch {}".format(rb))
            

            # Get relevant base data from Git to parse non-checked-out branch information
            merge_base = ''.join(self.vcs._run_command('merge-base HEAD {}'.format(rb)))
            diff = self.vcs.exec_('diff {m} {o} {d} | grep \"@entered-by\\|+++\\|---\"'.format(
                                        m = merge_base, 
                                        o = rb, 
                                        d = self.project['paths']['music']))
            # collect information on the changed segments
            changed_segments = cs = []
            for line in diff:
                if line.startswith('---'):
                    cs.append({'our-file': line.lstrip(' -')})
                if line.startswith('+++'):
                    cs[-1]['their-file'] = line.lstrip(' +')
                if line.startswith('- '):
                    cs[-1]['our-entered'] = line[line.find(':')+1:].lstrip()
                if line.startswith('+ '):
                    cs[-1]['their-entered'] = line[line.find(':')+1:].lstrip()
            
            # process all segments from the current branch
            for seg in cs:
                segment_added = False
                segment_deleted = False
                segment_modified = False
                if seg['our-file'] == '/dev/null':
                    segment_added = True
                    file = seg['their-file'][2:]
                elif seg['their-file'] == '/dev/null':
                    segment_deleted = True
                    file = seg['our-file'][2:]
                else:
                    segment_modified = True
                    file = seg['our-file'][2:]
                # strip leading path
                file = file[len(self.project['paths']['music'])+1:]
                voice, seg_file = os.path.split(file)
                seg_name = os.path.splitext(seg_file)[0]
                # get Segment object
                segment = self[voice][seg_name]
                
                # update Segment object
                if segment_added:
                    segment.meta_fields = {'entered-by': seg['their-entered']}
                elif segment_deleted:
                    segment.deleted = True
                    segment.meta_fields['deleted-by'] = 'branch {}'.format(rb)
                else:
                    segment.meta_fields['entered-by'] = seg['their-entered']
                segment.meta_fields['review-branch'] = rb
            
            
#            rb = self._review_branch(b)
#            self._review_branches.append(rb)
#            # Update segment objects with review status
#            for voice in rb['segments']:
#                for s in rb['segments'][voice]:
#                    seg = self[voice][s]
#                    chat("Segment " + voice + ' ' + seg.name)
#                    try:
#                        seg.meta_fields['review-branch'] = rb['name']
#                    except:
                        #TODO: This is only a workaround for a bug:
                        # when a file has been *added* in the review branch
                        # it is initialized as 'deleted' and we can't update it this way.
#                        pass
                        
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
