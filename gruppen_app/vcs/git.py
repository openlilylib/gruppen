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

import os
import subprocess

import __main__
import vcs


class GitError(vcs.VCSError):
    pass

class GitRepo(vcs.VCSRepo):
    
    def __init__(self, directory):
            
        if not os.path.isdir(directory):
            raise vcs.VCSError("Error opening repository {}: Does not exist.".format(directory))
        self.root = directory
        # test if Git is installed
        try:
            self.version = ''.join(self._run_command('--version'))
        except:
            raise vcs.VCSError("Git is not installed")
        
        super(GitRepo, self).__init__()
    
    def _run_command(self, cmd, args = []): 
        """
        run a git command and return its output
        as a string list.
        Raise an exception if it returns an error.
        - cmd is the git command (without 'git')
        - args is a string or a list of strings
        """
        cmd = ['git', cmd]
        if isinstance(args, str) or isinstance(args, unicode):
            cmd.append(args)
        else:
            cmd.extend(args)
        pr = subprocess.Popen(' '.join(cmd), cwd = self.root, 
                              shell = True, 
                              stdout = subprocess.PIPE, 
                              stderr = subprocess.PIPE)
        (out, error) = pr.communicate()
        if error:
            raise GitError(str(error))
        result = str(out).split('\n')
        if result[-1] == '':
            result.pop()
        return result
        
    def branches(self, local=True):
        """
        Returns a string list of branch names.
        The currently checked out branch will have a
        leading '* '.
        If local == False also return 'remote' branches.
        """
        args = [] if local else ['-a']
        args.append('--color=never')
        return [line.strip() for line in self._run_command('branch', args)]

    def checkout(self, branch):
        """
        Tries to checkout a branch.
        Add '-q' option because git checkout will
        return its confirmation message on stderr.
        May raise a GitError exception"""
        self._run_command('checkout', ['-q', branch])
        
    def current_branch(self):
        """Return the name of the currently checked-out branch."""
        branch_ref = ''.join(self._run_command('symbolic-ref -q HEAD'))
        return branch_ref[branch_ref.rfind('/')+1:]
    
    def contributors(self):
        """Return a list with all committers with their number of commits.
        Merge committers with the same name but different email address."""
        names = self._run_command('log --all --format=\'%cN\' | sort -u')
        result = {}
        for i in range(len(names)):
            try:
                name = names[i].decode()
            except:
                name = 'EncodingError'
            result[name] = str(
                result.get(name, 0) + 
                int(''.join(self._run_command(
                    'log --pretty=oneline --author=\"{}\" | wc -l'.format(name)))))
        return result
        
    def deleted_files_with_deleters(self, start_dir):
        """Return a list of deleted files with
        - author name of commit
        - files deleted by the commit
        - trailing empty line
        per commit."""
        if not os.path.isdir(start_dir):
            raise vcs.VCSError("Starting directory for determining deleted files\n" +
                           "doesn't exist: {}".format(start_dir))
        return self._run_command('log  --diff-filter=DR --pretty=format:\'%an\' --name-only {start}'.format(start = start_dir))

    def last_commit(self):
        """Return a short log entry for the last commit."""
        return ''.join(self._run_command('log -1 --pretty=oneline --abbrev-commit'))

    def total_commits(self):
        """Return the number of commits leading to the current state."""
        return self._run_command('log --oneline | wc -l')
