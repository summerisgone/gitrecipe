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

Notes
`````

*rev* option leaved for compatibility with ``zerokspot.recipe.git``.
It is better to use *ref* parameter, because it corresponds Git terminology

Since 0.0.2 recipe do check existing repository while install and update.
Repository origin url must be the same as given in **rev** option.
Otherwise repository will be deleted and cloned again.


About
-----

I've used recipe ``zerokspot.recipe.git``, but as for me, it too complex and has some disadvantages:

- it does not allow commit from the source folder, default remote is local copy in downloads
- it does not allow to specify the tag or branch of the repository, only revision hash

So I wrote my own git recipe with compatible options. You can choose this or that.


.. _PYPI: http://pypi.python.org/pypi
.. _reference: http://book.git-scm.com/7_git_references.html 
