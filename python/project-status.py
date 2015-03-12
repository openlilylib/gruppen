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
Generate status data of a Gruppen compliant repository.
By default create a JSON file with timestamp, optionally an HTML file instead.
Optionally remove JSON files with a timestamp of the same day that are found
in the target directory (to have always at most *one* file per day).
"""

import sys
import os

import init
import commandline
import project
import script
from report import *

def main():
    
    info('Gruppen - project-status\n')
    info('Generate status information about a Crowd-Editing project')

    commandline.parser.add_argument(
        '-t', '--target-directory',
        help = ("directory where the JSON/HTML file will be " +
                "saved to (will be created if it doesn't exist). " +
                "accepts absolute or relative paths"))

    commandline.parser.add_argument(
        '--prune-directory',
        action = 'store_true',
        help=("Remove JSON/HTML files from the same day, " +
              "so there is at most one file per day."))

    args = commandline.parse()

    # set external target directory if passed
    script.target_directory = args['target_directory'] if args['target_directory'] else ''


        
    proj = script.open_project(args)
    
    # ensure the repo is in the right state
    init.prepare_repository(proj.vcs)
    
    try:
        # add all present voices
        proj.read_voices()
        
        # generate JSON data
        proj.status.write_json()
        
        # optionally prune output directory
        if args['prune_directory']:
            proj.status.prune_out_dir()
    finally:
        init.finish_repository(proj.vcs)

# ####################################
# Finally launch the program
if __name__ == "__main__":
    main()

