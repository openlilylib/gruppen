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
Segments in a Voice
Handle the content part of the empty segments.
"""

import os, sys
import re
import celltemplate
from report import *


class Segment(object):
    """
    Represents one segment to be used as a grid segment template.
    """
    def __init__(self, content):
        self._name = ''
        # Extract segment content and remainder from the content string list
        # the remainder is used to generate the next segment from
        self.content, self.remaining_content = self.read_content(content)

    def _get_name(self):
        line = self.content[0].strip()
        name = line[:line.find(' =')]
        self._name = name
        return name

    def music(self):
        """
        Return the content of the music expression,
        i.e. without declaration and closing line.
        :return: string list
        """
        return self.content[1:-1]

    def roman_index(self):
        """
        Return the integer representation of the roman numeral name
        or -1 if name is no roman numeral
        :return: Integer
        """
        return -1

    def name(self):
        """
        Name of the segment as per the variable name in the input file
        :return: String
        """
        return self._name if self._name else self._get_name()

    def read_content(self, content):
        """
        Extract the first music variable from the content
        and "return" the remainder of the string list.
        This doesn't do any interpretation of the content.
        :param content: String list
        :return: String lists
        """

        def find_declaration(start):
            """
            Return the line index of the first variable definition
            after the given start index.
            Returns -1 if none is found
            :param start:
            :return: Integer
            """
            i = start
            while i < len(content):
                if re.match(".* = {", content[i]):
                    return i
                i += 1
            return -1

        def find_closing(first):
            """
            Return the line index of the closing bracket of the
            variable definition, after the starting index.
            Returns -1 if the variable is not finished.
            Add lines to content
            :param first:
            :return: Integer
            """
            result = []
            i = first
            while i < len(content):
                if content[i].strip() == "}":
                    return i
                i += 1
            return -1

        # Determine the line indices of the
        # opening and closing of the first music variable,
        # and the opening of the next one

        first = find_declaration(0)
        if first == -1:
            # No opening found, return empty lists
            return [], []
        last = find_closing(first)

        if last == -1:
            raise Exception("Unfinished segment in line {}: \"{}\"".format(first, content[first]))

        next = find_declaration(last)
        # if there is no 'next' declaration, return an empty list for remainder
        remainder = content[next:] if next >= 0 else []

        return content[first:last+1], remainder


class Segments(object):
    """
    Represents a string of segments
    """

    def __init__(self, voice):
        self.voice = voice

        # Template file that will later be patched with the empty segments' contents
        self._cell_template = celltemplate.CellTemplate(
            os.path.join(voice._root_dir, voice['project']['paths']['cell_template'])
        )

        self._segments_list = []
        self._segments = {}

        # Read contents of empty segments from template file
        self.read_empty_segments(
            os.path.join(voice._root_dir, voice['project']['paths']['segment_templates'])
        )

    def __getitem__(self, segment_name):
        """Return Segment object by its name - as if Segments were a dict object"""
        return self._segments[segment_name]

    def __iter__(self):
        """Iterator to yield Segment objects in their real order"""
        for s in self._segments_list:
            yield self._segments[s]

    def add_segment(self, segment):
        """Add a segment to the internal list and dictionary."""

        if segment.name() in self._segments_list:
            raise Exception("Segment {} already defined".format(segment.name()))
        # we don't need to carry this along with us any further
        segment.remaining_content = []

        # store the segment and its name
        self._segments_list.append(segment.name())
        self._segments[segment.name()] = segment

    def parse_segments(self):
        result = {}

    def read_empty_segments(self, filename):
        """
        Read the templates from disk,
        then extract the segment contents to individual objects.
        :param filename:
        :return:
        """

        try:
            f = open(filename)
            content = f.readlines()
            f.close()
        except:
            # for now simply re-throw the exception
            raise

        # Parse the file, slicing the music expressions / variables into an object list
        while content:
            segment = Segment(content)
            content = segment.remaining_content
            self.add_segment(segment)
