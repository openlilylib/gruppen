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
Project status
"""

import datetime
import os

import segmentgrid
import script
from report import *

# define empty dicts as globally available templates
completion_entries = {
        'total': 0, 
        'valid': 0, 
        'entered': 0, 
        'ready-for-review': 0, 
        'reviewed': 0, 
        'deleted': 0, 
        'not-done': 0, 
        'completion': 0, 
        }
        
segment_states = [
        'entered', 
        'ready-for-review', 
        'reviewed', 
        'deleted', 
        'not-done', 
        ]



class Status(object):
    """Represents the status of a repository, in terms of
    completed segments and reservations etc."""
    def __init__(self, project):
        
        chat('Create Status() object')
        
        self._time_stamp = ''
        self._json_filename = ''
        self.project = project
        self.vcs = project.vcs
        self._segment_grid = None
        self.time_stamp()
        
    def date(self):
        "Return the date part of self.time_stamp()."
        return self.time_stamp()[:self.time_stamp().find('_')]
        
    def grid(self):
        """Return the SegmentGrid object"""
        if not self._segment_grid:
            self._segment_grid = segmentgrid.SegmentGrid(self)
        return self._segment_grid
        
    def prune_out_dir(self):
        """Remove any existing JSON/HTML files from the same day
        as the current one."""
        # do nothing if we haven't written a JSON file yet
        if not self._json_filename:
            return
        
        info('Prune output dir (remove previous files from today)')
        
        out_dir, current_filename = os.path.split(self._json_filename)
        date = self.date()
        for f in os.listdir(out_dir):
            # find and remove files from the same day but with a different timestamp
            if f.startswith(date) and f != current_filename:
                
                chat('Remove {}'.format(current_filename))
                
                os.remove(os.path.join(out_dir, f))
        
    def time_stamp(self):
        """Return the UTC timestamp of the data
        formatted to be used in a filename.
        Will only be generated once, after parsing the segment grid."""
        if not self._time_stamp:
            self._time_stamp = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
        return self._time_stamp
        
    def write_json(self, out_dir = None, indent = 1):
        """Write status to JSON file."""
        if not out_dir:
            out_dir = self.project.abs_path('status_output')
        if script.target_directory:
            out_dir = script.target_directory
        if not os.path.isdir(out_dir):
            os.mkdir(out_dir)
        self._json_filename = os.path.join(out_dir, self.time_stamp() + '.json')
        json_data = self.grid().to_json(indent)
        
        info('Write grid data to {}'.format(self._json_filename))
        
        try:
            f = open(self._json_filename, 'w')
            f.write(json_data)
            f.close()
        except Exception as e:
            print 'Exception while writing to JSON file'
            print e
        
