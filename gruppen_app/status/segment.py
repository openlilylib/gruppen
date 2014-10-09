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

class Segment(object):
    
    def __init__(self, voice_row, segment_name):
        self.owner = voice_row
        self.name = segment_name
        self.segment_grid = self.owner.owner
        self.project = self.owner.project
        self.vcs = self.owner.vcs
        
        self.filename = os.path.join(self.project['paths']['music'], 
                                     self.owner.voice_name, 
                                     self.name) + '.ily'
        if not os.path.isfile(self.filename):
            self.deleted = True
            self.deleted_by = ''
        else:
            self.deleted = False        
            self.meta_fields = {}
            self.read_file()
            self.parse_file()

    def comma_list(self, input):
        """return a cleaned list of comma-separated entries"""
        return [entry.strip() for entry in input.split(',')]
        
    def parse_file(self):
        """Analyse the file"""
        self.parse_meta_fields()
        
    def parse_meta_fields(self):
        """Read the metadata fields from the
        header comment section."""
        for line in self.file_content:
            m = re.search('(@entered-by|@entry-date|@proofread-by|@proof-date).*:', line)
            if m:
                self.meta_fields[m.group(1)[1:]] = self.comma_list(line[m.end()+1:])
        
    def read_file(self):
        """Load the segment from file"""
        try:
            f = f = codecs.open(self.filename, 'r', 'utf-8')
            self.file_content = f.readlines()
        except:
            raise
        

