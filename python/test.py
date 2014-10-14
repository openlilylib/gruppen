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

#
# Test file to check

import sys
import os

import init
import commandline
import project

def seglist():
    for i in ['eins', 'zwei', 'drei']:
        yield i

def main():
    global project
    args = commandline.parse()
    # try to open a project
    try:
        project = project.Project(args)
    except AssertionError, e:
        print '\n', e, '\n'
        sys.exit(1)
 
    
#    project.init_segment_names(project._segment_names_as_int_range(91, zero_based = False))
#    print project.status._segment_grid.segment_names()
#    print project.status._segment_grid.voice_names()
    project.status._segment_grid.add_voice('basstrombone')
    project.status._segment_grid.add_voice('cymbals')
    project.status._segment_grid.add_voice('doublebass')
    
    print project.status._segment_grid.to_json()
    
#    for s in project['segment_names']:
#        print s, project.status._segment_grid['basstrombone'][s].status()
#    print project.status._segment_grid['basstrombone'].count('reviewed')
#    print project.status._segment_grid['basstrombone']._count
#    print project.status._segment_grid.to_json()
#    project.init_voice_names(project._voice_names_by_dirlist)
#    project.status._segment_grid.set_segment_names(
#        [s for s in seglist()])
    
#    print project.status._segment_grid._segment_list
#    print [branch for branch in project.vcs.branches(False) if branch.find('review/') > 0]
                
    
    #testing output
#    project.write_properties_to_json()

# ####################################
# Finally launch the program
if __name__ == "__main__":
    main()

