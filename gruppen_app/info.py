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
Information about the Gruppen application and scripts.
"""

from __future__ import unicode_literals

# these variables are also used by the distutils setup
name = "gruppen"
version = "ToBeDone (retrieve from Git)"
description = "LilyPond Project Management"
long_description = \
    "Gruppen is an application and a set of tools to manage collaborative edition " \
    "projects with LilyPond. It is centered around a concept of splitting an " \
    "(orchestral) score into a segment grid. Features include generation of parts " \
    "and score files, management of annotations and tasks."
maintainer = "Urs Liska"
maintainer_email = "ul@openlilylib.org"
domain = "git.ursliska.de/openlilylib/gruppen"
url = "https://{0}/".format(domain)
license = "GPL"

# this one is used everywhere in the application
appname = "Gruppen"
