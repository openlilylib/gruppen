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
import script
import voice
from report import *


def add_commandline_args():
    """
    Add script specific command line arguments
    """

    commandline.required_named.add_argument(
        '-b',
        '--basename',
        required=True,
        help=("Directory/voice name for the generated voice"))

    commandline.required_named.add_argument(
        '-n',
        '--name',
        required=True,
        help=("Display name for the generated voice (used in score)"))

    commandline.required_named.add_argument(
        '-s',
        '--short_instrument_name',
        required=True,
        help=("Short instrument name for subsequent systems")
    )

    commandline.parser.add_argument(
        '-c',
        '--clef',
        help=("Default clef for voice.\nDefaults to treble clef.")
    )

    commandline.parser.add_argument(
        '-t',
        '--transpose',
        help=("Transposition for the voice (if any). Will be considered relative to 'c'. " +
            "'a' => '\\transpose a c'")
    )
    commandline.parser.add_argument(
        '-k',
        '--key',
        help=("Initial key signature (if needed by the voice. " +
            "Uppercase results in major, lowercase in minor")
    )

def get_voice_props(args):
    """
    retrieve the properties of the to-be-generated voice
    from the command line arguments.
    """

    def get_transpose(transposition):

        result = "\\transpose {} c".format(transposition) if transposition else ''
        return result

    result = {
        'basename': args['basename'],
        'display_name': args['name'],
        'short_instrument_name': args['short_instrument_name'],
        'clef': args['clef'],
    }

    if args['transpose']:
        result['transpose'] = "\\transpose {} c".format(args['transpose'])
    result['transpose'] = args['transpose'] if args['transpose'] else 'c'
    key = args['key']
    if key:
        mode = '\\minor' if key.islower() else '\\major'
        result['key'] = '\\key {} {}'.format(key.lower(), mode)

    return result

def main():
    info('Gruppen - generate-voice\n')
    info('Generate voice')

    # add script specific options to the command line parser
    add_commandline_args()

    # read and interpret options
    args = commandline.parse()
    voice_props = get_voice_props(args)

    # open target repository
    proj = script.open_project(args)

    # create a new Voice object for the project
    new_voice = voice.Voice(proj, voice_props)
    new_voice.print_props()

    info('Writing {} segments to {}'.format(
        len(new_voice.segments._segments_list),
        os.path.join(
            proj['paths']['root'],
            new_voice.music_dir)))
    new_voice.segments.write_segments()

# ####################################
# Finally launch the program
if __name__ == "__main__":
    main()

