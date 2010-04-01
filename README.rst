Welcome to gitrecipe doc page

Usage
-----

Recipe clones git repository and checkouts to revision, if it is provided 
in configuration. You can use recipe like this: ::

    [buildout]
    parts = data
    
    [data]
    recipe = gitrecipe
    repository = git://example.com/my-git-repo.git
    rev = origin/redevlop-branch

Options
-------

*repository* - repository url

*ref* of *rev* - git reference_ wich you want to checkout

\*Note:* rev option leaved for compatibility with zerokspot.recipe.git.
It is better to use *ref* parameter, because it corresponds Git terminology\

Note
````

\While I haven't uploaded recipe to PYPI_ you should 
put code into some directory and add tell zc.buildout treat this path as develop eggs dir. 
For example: \ 

Directory structure: ::

    ~/myproject/
        bootstrap.py
        buildout.cfg
        gitrecipe/
            README.rst
            recipe.py
            setup.py

And buildout config: ::

    [buildout]
    develop = gitrecipe
    parts = data
    
    [data]
    recipe = gitrecipe
    repository = git://example.com/my-git-repo.git


About
-----

I've used recipe ``zerokspot.recipe.git``, but as for me, it too complex and has some disadvantages:

- it does not allow commit from the source folder, default remote is local copy in downloads
- it does not allow to specify the tag or branch of the repository, only revision hash

So I wrote my own git recipe with compatible options. You can choose this or that.


.. _PYPI: http://pypi.python.org/pypi
.. _reference: http://book.git-scm.com/7_git_references.html 
