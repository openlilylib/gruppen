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

def main():
    global project
    args = commandline.parse()
    # try to open a project
    try:
        project = project.Project(args)
    except AssertionError, e:
        print '\n', e, '\n'
        sys.exit(1)
    
    #testing Git functionality

    print "Opened repository:", project.vcs.root
    print "Testing VCS functionality"
    
    git = project.vcs
    print
    print git.version
    print
    print "Current branch:", git.current_branch()
    print
    print "Last commit:"
    print git.last_commit()
    print
    print "Total commits:"
    print git.total_commits()
    print 
    print "Contributors:"
    print git.contributors()
    print
    print
    print "Deleted files:"
    import vcs
    try:
        print '\n'.join(git.deleted_files_with_deleters(project['paths']['music']))
    except vcs.VCSError as e:
        print e
    try:
        print "Deletions:"
        print git.deletions()
    except vcs.VCSError as e:
        print e
    
        

# ####################################
# Finally launch the program
if __name__ == "__main__":
    main()

