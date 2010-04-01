# -*- coding: utf-8 -*-
import logging, os, zc.buildout, subprocess


class GitRecipe(object):
    '''Simple recipe for fetch code form remote repository, using system git'''
    def __init__(self, buildout, name, options):
        self.options, self.buildout = options, buildout

        if 'repository' not in self.options:
            raise zc.buildout.UserError('Repository url must be provided')
        self.url = options['repository']
        # ref option overrides rev
        if 'rev' in options:
            self.ref = options.get('rev', 'origin/master')
        if 'ref' in options:
            self.ref = options.get('ref', 'origin/master')

        # determine repository name
        repo_path = self.url.rsplit('/', 1)[1]
        if '.git' in repo_path:
            repo_path = repo_path.rsplit('.git', 1)[0]
        self.options['location'] = os.path.join(buildout['buildout']['parts-directory'], repo_path)

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
                os.chdir(self.options['location'])
                self.git('checkout', [self.ref, ])
        except zc.buildout.UserError:
            # should manually delete files because buildout thinks that no files created
            from shutil import rmtree
            rmtree(self.options['location'])
            raise

        # return to root directory
        os.chdir(self.buildout['buildout']['directory'])

        return self.options['location']

    def update(self):
        '''Update repository rather than download it again'''
        # go to parts directory
        os.chdir(self.options['location'])
        self.git('fetch', ['origin', ])
        # if revision is given, checkout to revision 
        if 'rev' in self.options:
            self.git('checkout', [self.ref, ])
        # return to root directory
        os.chdir(self.buildout['buildout']['directory'])

        return self.options['location']

