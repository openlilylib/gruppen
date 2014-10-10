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

import segmentgrid

# define empty dicts as globally available templates
completion_entries = {
        'total': None, 
        'valid': None, 
        'entered': None, 
        'reviewed': None, 
        'deleted': None, 
        'not-done': None, 
        'completion': None, 
        }
        
segment_states = [
        'entered', 
        'reviewed', 
        'deleted', 
        'not-done', 
        ]



class Status(object):
    """Represents the status of a repository, in terms of
    completed segments and reservations etc."""
    def __init__(self, project):
        self.project = project
        self.vcs = project.vcs
        self._segment_grid = segmentgrid.SegmentGrid(self)
        
