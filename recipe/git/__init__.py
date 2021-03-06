# -*- coding: utf-8 -*-
import logging, os, zc.buildout, subprocess, re, shutil


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
        match = re.search('\/(?P<repo_name>[a-zA-Z0-9-]*)(.git)?$', self.url)
        if match:
            repo_name = match.groupdict()['repo_name']
            self.repo_path = os.path.join(self.buildout['buildout']['parts-directory'], repo_name)
        else:
            raise zc.buildout.UserError('Can not find repository name')
        self.options['location'] = os.path.join(buildout['buildout']['parts-directory'], self.repo_path)

    def git(self, operation, args, quiet=True):
        if quiet:
            command = ['git'] + [operation] + ['-q'] + args
        else:
            command = ['git'] + [operation] + args

        proc = subprocess.Popen(' '.join(command), shell=True, stdout=subprocess.PIPE)
        status = proc.wait()
        if status:
            raise zc.buildout.UserError('Error while executing %s' % ' '.join(command))
        return proc.stdout.read()

    def check_same(self):
        old_cwd = os.getcwd()
        existing_repository = None

        if os.path.exists(self.repo_path) and os.path.exists(os.path.join(self.repo_path, '.git')):
            os.chdir(self.repo_path)
            origin = self.git('remote', ['show', 'origin'], quiet=False)
            existing_repository = re.findall('^\s*Fetch URL:\s*(.*)$', origin, flags=re.MULTILINE)[0]

        os.chdir(old_cwd)
        if existing_repository == self.url:
            return True

    def install(self):
        '''Clone repository and checkout to version'''
        # go to parts directory
        os.chdir(self.buildout['buildout']['parts-directory'])

        try:

            if os.path.exists(self.repo_path):
                if self.check_same():
                    # If the same repository is here, just fetch new data and checkout to revision
                    # aka update ;)
                    os.chdir(self.repo_path)
                    self.git('fetch', [self.url, ])
                    if 'rev' in self.options:
                        os.chdir(self.options['location'])
                        self.git('checkout', [self.ref, ])
                        # return to root directory
                        os.chdir(self.buildout['buildout']['directory'])
                        return self.options['location']

                else:
                    # if repository exists but not the same, delete all files there
                    shutil.rmtree(self.repo_path, ignore_errors=True)

            # in fact, the install
            os.chdir(self.buildout['buildout']['parts-directory'])
            self.git('clone', [self.url, ])
            # if revision is given, checkout to revision 
            if 'rev' in self.options:
                os.chdir(self.options['location'])
                self.git('checkout', [self.ref, ])

        except zc.buildout.UserError:
            # should manually clean files because buildout thinks that no files created
            shutil.rmtree(self.options['location'])
            raise

        # return to root directory
        os.chdir(self.buildout['buildout']['directory'])
        return self.options['location']

    def update(self):
        '''Update repository rather than download it again'''
        # go to parts directory
        if self.check_same():
            os.chdir(self.options['location'])
            self.git('fetch', ['origin', ])
            # if revision is given, checkout to revision
            if 'rev' in self.options:
                self.git('checkout', [self.ref, ])
        else:
            self.install()

        # return to root directory
        os.chdir(self.buildout['buildout']['directory'])
        return self.options['location']

