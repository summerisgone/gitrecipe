# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="gitrecipe",
    version='0.0.2',
    description='Simple buildout recipe for downloading git repositories. It uses system git command and its syntax',
    author='Ivan Gromov',
    author_email='summer.is.gone@gmail.com',
    url='http://github.com/summerisgone/gitrecipe',
    download_url='http://github.com/summerisgone/gitrecipe/zipball/0.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Natural Language :: Russian',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.5',
        'Topic :: Software Development :: Version Control',
    ],
    namespace_packages=['recipe'],
    packages=find_packages(),
    install_requires=['setuptools', 'zc.recipe.egg'],
    entry_points={'zc.buildout': ['default = recipe.git:GitRecipe']},
    zip_safe=False,
    long_description=open('README.rst').read(),
)
