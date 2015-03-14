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
        self._properties = {}
        # Extract segment content and remainder from the content string list
        # the remainder is used to generate the next segment from
        self.content, self.remaining_content = self.read_content(content)
        self.parse_content()

    def __getitem__(self, property):
        """
        Return the requested property as if Segment were a dict
        """
        return self._properties[property]

    def roman_index(self):
        """
        Return the integer representation of the roman numeral name
        or -1 if name is no roman numeral
        :return: Integer
        """
        return -1

    def parse_content(self):
        """
        Parse content and retrieve properties of the music segment.
        """

        def is_barnumber_check(line):
            """
            Returns a bar number if the given line is a barnumber check
            or integer zero if not
            """
            match = re.search("(\\\\barNumberCheck *\#)([0-9]+)", line)
            return match.group(2) if match else 0

        def is_key_signature(line):
            """
            Returns a key signature string if the given line is a key signature
            or an empty string if not
            """
            match = re.search("(\\\\key *)([a-z]* *(\\\\major|\\\\minor))", line)
            return match.group(2) if match else ''

        def is_time_signature(line):
            """
            Returns a time signature string if the given line is a time signature
            or an empty string if not
            """
            match = re.search("(\\\\time *)([0-9]+/[0-9]+)", line)
            return match.group(2) if match else ''

        # read segment name from first content line
        line = self.content[0].strip()
        self._properties['name'] = line[:line.find(' =')]

        # read the body of the content, extracting and/or removing lines to properties
        first_content = False
        i = 1
        music = []
        while not i >= len(self.content) - 1:
            line = self.content[i]
            lstr = line.strip()

            # TODO: This is not really robust yet.
            # We're not handling multiline comments (or even Scheme) yet.

            # Check for line with "content"
            content = len(lstr) > 0 and not lstr.startswith('%')

            # Check for time signatures
            time_sig = is_time_signature(lstr)
            if time_sig:
                # set start/end time signatures.
                # remove content line for first
                if not first_content and not 'time_signature_start' in self._properties:
                    self._properties['time_signature_start'] = time_sig
                    self._properties['time_signature_end'] = time_sig
                    # flag to not set first_content to True
                    content = False
                    i += 1
                    continue
                else:
                    self._properties['time_signature_end'] = time_sig

            # Check for key signatures
            key_sig = is_key_signature(line)
            if key_sig:
                if not first_content and not 'key_signature_start' in self._properties:
                    self._properties['key_signature_start'] = key_sig
                    self._properties['key_signature_end'] = key_sig
                    # flag to not set first_content to True
                    content = False
                    i += 1
                    continue
                else:
                    self._properties['key_signature_end'] = key_sig

            # Check for barnumber checks
            barnumber_check = is_barnumber_check(line)
            if barnumber_check:
                if not first_content and not 'barnumber_start' in self._properties:
                    self._properties['barnumber_start'] = barnumber_check
                    # flag to not set first_content to True
                    content = False
                    i += 1
                    continue

            if not first_content and content:
                first_content = True

            music.append(line)
            i += 1


        #store the resulting music expression
        self._properties['music'] = sm = ['{']
        sm.extend(music)
        sm.append('}')

        print
        print self['name']
        print "barnumber start:", self._properties.get('barnumber_start', 'not defined')
        print "time start:", self._properties.get('time_signature_start', 'not defined')
        print "time end:", self._properties.get('time_signature_end', 'not defined')
        print "key start:", self._properties.get('key_signature_start', 'not defined')
        print "key end:", self._properties.get('key_signature_end', 'not defined')
        #print ''.join(self['music'])


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

        if segment['name'] in self._segments_list:
            raise Exception("Segment {} already defined".format(segment['name']))
        # we don't need to carry this along with us any further
        segment.remaining_content = []

        # store the segment and its name
        self._segments_list.append(segment['name'])
        self._segments[segment['name']] = segment

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
