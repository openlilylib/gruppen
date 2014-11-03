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
Remove deprecated \\annotate calls in segment files
and replace them with the corresponding new functions.
"""

import sys
import os
import codecs

import init
import commandline
import project
import script
from report import *

annotation_types = {
    'musical-issue': 'musicalIssue', 
    'musical-question': 'musicalIssue', 
    'critical-remark': 'criticalRemark', 
    'critical remark': 'criticalRemark', 
    'critical-issue': 'criticalRemark', 
    'lilypond-issue': 'lilypondIssue', 
    'question': 'question', 
    'todo': 'todo'}

def cleanup(segment):
    """Try to replace deprecated annotations
    with their new counterpart and clean up the content fields."""
    cnt = ''.join(segment.file_content)
    index = cnt.find('\\annotate')
    if index < 0:
        return
    while index >= 0:
        cnt, new_ind = parse_annotation(cnt, index)
        index = cnt.find('\\annotate', new_ind)
    f = codecs.open(segment.filename, 'w', 'utf-8')
    f.write(cnt)
    f.close()
    info('Updated: {} {}'.format(segment.voice_name, segment.name))

def parse_annotation(cnt, index):
    """Parse and replace an annotation."""
    # Determine indentation level of the annotation
    indent = ' ' * (index + 1 - cnt.rfind('\n', 0, index))
    
    # split file into parts (middle will be replaced)
    leading = cnt[:index]
    ann = cnt[index:cnt.find('}', index)+1]
    ann_cnt = ann[ann.find('{')+1:-1].strip()
    remainder = cnt[index + len(ann):]
    
    # parse fields
    fields = {}
    eq_ind = ann_cnt.find('=')
    while eq_ind >= 0:
        key = ann_cnt[:eq_ind].strip()
    
        ann_cnt = ann_cnt[ann_cnt.find('\"')+1:]
        value = ann_cnt[:ann_cnt.find('\"')]
        ann_cnt = ann_cnt[ann_cnt.find('\"')+1:]
        fields[key] = value
        eq_ind = ann_cnt.find('=')
    
    # skip annotations with unknwon (misspelled?) type
    if not fields['type'] in annotation_types:
        return cnt, index + 2

    # construct the new annotation
    new_ann = '\\' + annotation_types[fields['type']] + ' \\with {\n'
    try:
        new_ann += indent + 'author = \"{}\"\n'.format(fields.get('author', 'NN'))
        new_ann += indent + 'message = \"{}\"\n'.format(fields.get('message', ''))
    except UnicodeEncodeError:
        #skip annotations that result in unicode errors
        return cnt, index + 2
    for f in fields:
        if not f in ['type', 'author', 'message', 'context', 'date']:
            new_ann += indent + f + ' = \"{}\"\n'.format(fields[f])
    new_ann += indent[:-2] + '}'
    
    return leading + new_ann + remainder, index + len(new_ann)

def main():
    
    info('Trunknes Lied - clean up \\annotate\n')
        
    args = commandline.parse()
        
    proj = script.open_project(args)
    
    proj.read_voices()
    
    grid = proj.status.grid()
    for v in proj['voice_names']:
        for s in proj['segment_names']:
            if not grid[v][s].deleted:
                cleanup(grid[v][s])
        

# ####################################
# Finally launch the program
if __name__ == "__main__":
    main()

