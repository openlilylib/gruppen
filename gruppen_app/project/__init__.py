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
Project properties
"""
import os
import json
import codecs
import vcs
import status

# Project object
class Project(object):
    """Properties of the LilyPond project."""
    def __init__(self, args):
        
        self.properties = {
            'paths': {}}
        self.modified = False
        
        # determine project root directory
        directory = args['directory']
        if not directory:
            directory = os.getcwd()
        elif not os.path.isabs(directory):
            directory = os.path.join(os.getcwd(), directory)
        self.properties['paths']['root'] = os.path.normpath(directory)

        # check if we're in a VCS repository and create VCS object
        self.vcs = vcs.open(self.properties['paths']['root'])
        
        # set/determine information on the project directory structure.
        # If the file project/properties.json is present it is parsed,
        # otherwise default values are used.
        
        self.properties_file = args['properties_file'] if args['properties_file'] else os.path.join(
                               self.properties['paths']['root'], 'project', 'properties.json')
        if os.path.isfile(self.properties_file):
            try:
                self.read_properties_from_json()
            except Exception as e:
                print ("{}\n" +
                       "Setting project structure to default values.").format(e)
                self.set_defaults()
        else:
            self.set_defaults()
        
        self.status = status.Status(self)
        
    def __getitem__(self, property):
        """Return project property - as if Project were a dict object"""
        return self.properties[property]
        
    def init_segment_names(self, segs):
        """Populate the list of segment names.
        'segs' can be a callable that returns a list
        with segment names. Some possible functions are defined
        in the class."""
        self.properties['segment_names'] =  [s for s in segs()] if callable(segs) else segs

    def _segment_names_as_int_range(self, upper, digits= 0 , zero_based = True):
        """Return a list of normalized integer segment names.
        'upper' is treated in the pythonic way (up to but not including).
        names are padded with zeroes either to the length of the highest value
        or using the digits argument (if that's present and high enough)."""
        lower = 0 if zero_based else 1
        max_digits = max(digits, len(str(upper-1)))
        pad = '0' + str(max_digits)
        return [format(i, pad) for i in range(lower, upper)]
        
        
    def init_voice_names(self, voices):
        """Populate the list of voice names.
        'voices' can be a callable that returns a list
        with voice names. Some possible functions are defined
        in the class."""
        self.properties['voice_names'] =  [v for v in voices()] if callable(voices) else voices
    
    def _voice_names_by_dirlist(self):
        """Return a list of directories under ['music'] path."""
        base = self['paths']['music']
        dir = os.listdir(base)
        dir.sort()
        return [entry for entry in dir if os.path.isdir(os.path.join(base, entry))]
        
    def read_properties_from_json(self):
        """Read a JSON file containing project properties."""
        try:
            f = codecs.open(self.properties_file, 'r', 'utf-8')
            self.properties = json.loads(f.read())
        except Exception as e:
            raise Exception("Error reading properties file: {}".format(e))

    def read_voices(self):
        """Add all voices from the properties to the segment grid."""
        self.status.grid().add_voices(self['voice_names'])
        
    def rel_path(self, path_property):
        """Return the path of a property relative to root."""
        if not path_property in self['paths']:
            raise KeyError('Unknown path property {}'.format(path_property))
        return self['paths'][path_property][len(self['paths']['root'])+1:]
        
    
    def segment_count(self):
        """Return the number of segments per row"""
        return len(self['segment_names'])
        
    def set_defaults(self):
        """Set default values to project configuration variables
        if they can't be read from project/structure.json"""
        
        # set path to project description file
        self.properties['description_file'] = os.path.join(self.properties['paths']['root'], 'project', 'description.json')
        
        # set paths (stored as absolute paths)
        self.properties['paths']['project_info'] = os.path.join(self.properties['paths']['root'], 'project')
        self.properties['paths']['music'] = os.path.join(self.properties['paths']['root'], 'music')
        self.properties['paths']['status_output'] = os.path.join(self.properties['paths']['root'], 'status')
        
    def set_path(self, path, value):
        """Set a path property and set self.modified to False if property has changed.
        Throws a KeyError if the path property doesn't exist."""
        try:
            old = self.properties['paths'][path]
        except KeyError:
            raise KeyError("Project doesn't have a path property {}".format(property))
        if old != value:
                self.modified = True
                self.properties['paths'][path] = value
        
    def set_property(self, property, value):
        """Set a property and set self.modified to False if property has changed.
        Throws a KeyError if the property doesn't exist"""
        try:
            old = self.properties[property]
        except KeyError:
            raise KeyError("Project doesn't have a property {}".format(property))
        if old != value:
                self.modified = True
                self.properties[property] = value
        
    def write_properties_to_json(self, ):
        """Write the project properties to a JSON file."""
        try:
            if self.modified:
                if not os.path.isdir(self['paths']['project_info']):
                    os.mkdir(self['paths']['project_info'])
                
                f = codecs.open(self.properties_file, 'w', 'utf-8')
                f.write(json.dumps(self.properties))
                f.close()
        except OSerror as e:
            raise OSError("Error writing project properties to JSON file: {}".format(e))
        
