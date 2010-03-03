# -*- coding: utf-8 -*-
import logging, os, zc.buildout, subprocess


class GitRecipe(object):
    '''Simple recipe for fetch code form remote repository, using system git'''
    def __init__(self, buildout, name, options):
        self.options, self.buildout = options, buildout

        if 'repository' not in self.options:
            raise zc.buildout.UserError('Repository url must be provided')
        self.url = options['repository']

        # determine repository name
        repo_path = self.url.rsplit('/', 1)[1]
        if '.git' in repo_path:
            repo_path = repo_path.rsplit('.git', 1)[0]
        self.repo_path = os.path.join(buildout['buildout']['parts-directory'], repo_path)
        return super(GitRecipe, self).__init__()

    def git(self, operation, args):
        command = ['git'] + [operation] + ['-q'] + args
        status = subprocess.call(' '.join(command), shell=True)
        if status != 0:
            raise zc.buildout.UserError('Error while executing %s' % ' '.join(command))

    def install(self):
        '''Clone repository and checkout to version'''
        # go to parts directory
        os.chdir(self.buildout['buildout']['parts-directory'])

        try:
            # first, fetch code from remote repository
            self.git('clone', [self.url, ])
            # if revision is given, checkout to revision 
            if 'rev' in self.options:
                os.chdir(self.repo_path)
                self.git('checkout', [self.options['rev'], ])
        except zc.buildout.UserError:
            # should manually delete files because buildout thinks that no files created
            from shutil import rmtree
            rmtree(self.repo_path)
            raise

        # return to root directory
        os.chdir(self.buildout['buildout']['directory'])

        return self.repo_path

    def update(self):
        '''Update repository rather than download it again'''
        # go to parts directory
        os.chdir(self.repo_path)
        self.git('fetch', ['origin', ])
        # if revision is given, checkout to revision 
        if 'rev' in self.options:
            self.git('checkout', [self.options['rev'], ])
        # return to root directory
        os.chdir(self.buildout['buildout']['directory'])

        return self.repo_path
