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

import vcs
import script
from report import *

class GitError(vcs.VCSError):
    pass

class GitRepo(vcs.VCSRepo):
    
    def __init__(self, project):
        super(GitRepo, self).__init__(project)

        # test if Git is installed
        try:
            self.version = ''.join(self._run_command('--version'))
        except:
            raise vcs.VCSError("Git is not installed")
        
    
    def _run_command(self, cmd, args = [], raise_error = True): 
        """
        run a git command and return its output
        as a string list.
        - cmd is the git command (without 'git')
        - args is a string or a list of strings.
        When raise_error == True any output on the error stream
        will raise a GitError exception, otherwise it will be
        output as part of the result string list. (This is necessary
        because Git sometimes returns something on error that is not
        an exception but expected behaviour.)
        """
        cmd = ['git', cmd]
        if isinstance(args, str) or isinstance(args, unicode):
            cmd.append(args)
        else:
            cmd.extend(args)
        
        chat('Executing Git command: {}'.format(' '.join(cmd)))
        
        pr = subprocess.Popen(' '.join(cmd), cwd = self.root, 
                              shell = True, 
                              stdout = subprocess.PIPE, 
                              stderr = subprocess.PIPE)
        (out, error) = pr.communicate()
        if error:
            if raise_error:
                raise GitError(str(error))
            else:
                out.extend(error)
        result = out.decode('utf8').split('\n')
        if result[-1] == '':
            result.pop()
        chat(result)
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

    def changed_files(self, other_branch, start_dir = ''):
        """Return a list of files changed on a given branch.
        Relies on finding the common ancestor between the current HEAD and
        the other branch. This *may* return too few results when the current
        branch has been merged into the other branch in the meantime
        (usually merge of master into a working branch)."""
        merge_base = ''.join(self._run_command('merge-base HEAD {}'.format(other_branch)))
        return self._run_command('diff --name-only {m} {o} {d}'.format(
                                m = merge_base, 
                                o = other_branch, 
                                d = start_dir))
        
    def changed_segments(self, other_branch):
        """Return a list of changed segments in another branch.
        Uses changed_files but restricts to the project's music directory.
        Each segment is returned as a tuple (voice, segment)"""
        segments = self.changed_files(other_branch, self.project['paths']['music'])
        result = {}
        for s in segments:
            path, file = os.path.split(s[len(self.project['paths']['music'])+1:])
            if not path in result:
                result[path] = []
            result[path].append(os.path.splitext(file)[0])
            
        return result
        
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
                name = names[i].decode('utf8')
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
        if not os.path.isdir(os.path.join(script.proj['paths']['root'], start_dir)):
            raise vcs.VCSError("Starting directory for determining deleted files\n" +
                           "doesn't exist: {}".format(start_dir))
        return self._run_command('log  --diff-filter=DR --pretty=format:\'%an\' --name-only {start}'.format(start = start_dir))

    def exec_(self, cmd, args = [], raise_error = True):
        """Execute arbitrary Git commands,
        public interface to _run_command()"""
        return self._run_command(cmd, args, raise_error)
        
    def is_clean(self):
        """Return True if the repository is clean"""
        if self._run_command('status --porcelain'):
            return False
        else:
            return True
        
    def last_commit(self):
        """Return a short log entry for the last commit."""
        return ''.join(self._run_command('log -1 --pretty=oneline --abbrev-commit'))

    def pull(self, remote = 'origin'):
        """Pull from origin or the given remote"""
        cmd = 'pull {}'.format(remote)
        return self._run_command(cmd)
        
    def review_branches(self):
        """Return a list with all (remote) branches ready for review."""
        return [branch[branch.find('origin'):] for branch in self._run_command('branch -a | grep origin/review')]
        
    def stash(self):
        """Save the working tree to a stash.
        Return True if actually something has been stashed.
        (If not and you stash_pop afterwards, *another* stash is applied,
        which usually doesn't work and is definitely not what you want."""
        
        # determine the position (committish) of the existing stash
        old_stash = self._run_command('rev-parse -q --verify refs/stash')[0]
        debug('Old stash: ' + old_stash)
        
        # do stash
        self._run_command('stash save')
        
        # determine the new stash position
        new_stash = self._run_command('rev-parse -q --verify refs/stash')[0]
        debug('New stash: ' + new_stash)
        
        # if the two states are identical we didn't actually stash anything.
        result = new_stash != old_stash
        debug('Has stashed: {}'.format(result))
        return result
    
    def stash_pop(self):
        """Reapply stashed changes and drop the stash"""
        return self._run_command('stash pop')
    
    def total_commits(self):
        """Return the number of commits leading to the current state."""
        return self._run_command('log --oneline | wc -l')
