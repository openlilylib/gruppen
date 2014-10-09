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
Version control tools.
Currently only Git is supported, but it should be designed to be easily
complemented with other implementations.
"""

import os
from abc import ABCMeta, abstractmethod

class VCSError(OSError):
    pass

class VCSRepo(object):
    """
    Interface for classes managing VCS repositories.
    Currently we only support Git, but this level of
    abstraction is intended to offer an interface to
    add other VCS comparably easily.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self._deletions = {}

    @abstractmethod
    def _run_command(self, cmd, args = []): 
        """
        run a VCS command and return its output
        as a string list.
        Raise an exception if it returns an error.
        - cmd is the VCS command (without 'git' etc.)
        - args is a string or a list of strings
        """
        pass

    @abstractmethod
    def branches(self, local=True):
        """
        Returns a string list of branch names.
        The currently checked out branch will have a
        leading '* '.
        If local == False also return 'remote' branches.
        """
        pass

    @abstractmethod
    def checkout(self, branch):
        """
        Try to checkout a branch.
        """
        pass
        
    @abstractmethod
    def current_branch(self):
        """Return the name of the currently checked-out branch."""
        pass

    @abstractmethod
    def contributors(self):
        """Return a list with all committers with their number of commits.
        Merge committers with the same name but different email address."""
        pass
        
    @abstractmethod
    def deleted_files_with_deleters(self):
        """Return a list of deleted files with
        - author name of commit
        - files deleted by the commit
        - trailing empty line
        per commit."""

    def deletions(self):
        """Return a dictionary of all files
        together with their deleters."""
        
        # definition in subclasses!
        import __main__
        start_dir = __main__.project.rel_path('music') + '/'
        lines = self.deleted_files_with_deleters(start_dir)
        
        # preset name of commit author
        deletor = ''
        for line in lines:
            if line.startswith('parts/'):
                basepath, sink = os.path.splitext(line)
                voice, segment = os.path.split(basepath)
                voice = voice[len(start_dir):]
                
                # if part is met for the first time:
                if not voice in self._deletions:
                    self._deletions[voice] = {}
                
                # assing the author to the deleted segment
                self._deletions[voice][segment] = deletor
            elif not line:
                # Empty lines don't count
                continue
            else:
                # set author of next commit
                deletor = line
        return self._deletions 

        
    @abstractmethod
    def last_commit(self):
        """Return a short log entry for the last commit."""
        pass

    @abstractmethod
    def total_commits(self):
        """Return the number of commits leading to the current state."""
    pass

    def who_deleted(self, part, segment):
        #TODO: This has to be generalized together with
        #generalizing the repo structure itself
        """Return the name of the committer who deleted a file.
        The list is generated only once and then cached."""
        
        # if we're running for the first time generate the dictionary
        if not self._deletions:
            self._deletions = self.deletions()
            
        # validation check if we're requesting an invalid file
        if (not part in self._deletions) or (not segment in self._deletions[part]):
            return 'Not a deleted file: {}/{}'.format(part, segment)
        
        # look up the author of the deletion
        return self._deletions[part][segment]



def open(repository):
    """Determine if the given directory is a repository
    of a supported VCS tool and return a corresponding
    VCSRepo subclass object."""
    
    if not os.path.isdir(repository):
        raise VCSError("Error opening directory {}.\nDoes not exist.".format(repository))
    for t in repo_test_functions:
        repo_object = repo_test_functions[t](repository)
        if repo_object:
            return repo_object
    raise VCSError("Error opening directory {}.\n" +
                   "Is not a repository of a supported VCS")


# functions to test for repositories of supported VCSs
def test_git(directory):
    """Return a GitRepo object if directory is a Git repository"""
    if os.path.isdir(os.path.join(directory, '.git')):
        import git
        return git.GitRepo(directory)

repo_test_functions = {
    'Git': test_git}
    
