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
Segment properties
"""

import os
import re
import codecs

from report import *

def comma_list(input):
    """return a cleaned list of comma-separated entries"""
    return [entry.strip() for entry in input.split(',')]
    
def parse_segment_meta_fields(content):
    """Read the metadata fields from the
    header comment section of a segment.
    Return a dictionary with four values."""
    result = {}
    for line in content:
        m = re.search('(@entered-by|@entry-date|@proofread-by|@proof-date).*:', line)
        if m:
            result[m.group(1)[1:]] = comma_list(line[m.end():].lstrip())
    return result
    
class Segment(object):
    
    def __init__(self, voice_row, segment_name):
        self.owner = voice_row
        self.voice_name = voice_row.voice_name
        self.name = segment_name
        self.segment_grid = self.owner.owner
        self.status_obj = self.owner.status
        self.project = self.owner.project
        self.vcs = self.owner.vcs
        
        self.filename = os.path.join(self.project['paths']['root'], 
                                     self.project['paths']['music'], 
                                     self.owner.voice_name, 
                                     self.name) + '.ily'
        if not os.path.isfile(self.filename):
            self.deleted = True
        else:
            self.deleted = False        
            self.meta_fields = {}
            self.read_file()
            self.parse_file()
        
        del_str = '(deleted) ' if self.deleted else ''
        debug('Added {d} segment from {f}'.format(
                    d = del_str, 
                    f = self.filename))

    def deleted_by(self):
        """Return the name of the deleter of the segment file
        or an empty string if it is not deleted."""
        if not self.deleted:
            return ''
        return self.segment_grid.deleted_by(self.voice_name, self.name)
        
    def to_json(self):
        """Return a JSON compatible representation.
        Note that this is *not* a JSON object but
        a dictionary that can easily be used in a JSON object."""
        result = {'status': self.status()}
        if self.deleted:
            result['deleted-by'] = self.deleted_by()
            return result
        if self.status() != 'not-done':
            result['entered-by'] = self.meta_fields['entered-by']
            result['entry-date'] = self.meta_fields['entry-date']
            result['proofread-by'] = self.meta_fields['proofread-by']
            result['proof-date'] = self.meta_fields['proof-date']
        if self.status() == 'ready-for-review':
            result['review-branch'] = self.meta_fields['review-branch']
        
        return result
        
    def parse_file(self):
        """Analyse the file"""
        self.parse_meta_fields()
        
    def parse_meta_fields(self):
        """Read the metadata fields from the
        header comment section."""
        self.meta_fields = parse_segment_meta_fields(self.file_content)
        
    def read_file(self):
        """Load the segment from file"""
        try:
            f = f = codecs.open(self.filename, 'r', 'utf-8')
            self.file_content = f.readlines()
        except:
            raise
        
    def status(self):
        """Return the status property of the segment."""
        if self.deleted:
            return "deleted"
        if self.meta_fields['entered-by'][0]:
            if self.meta_fields['proofread-by'][0]:
                return "reviewed"
            else:
                return "entered"
        if 'review-branch' in self.meta_fields:
            return "ready-for-review"
        else:
            return "not-done"
    


