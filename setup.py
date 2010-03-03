# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="gitrecipe",
    entry_points={'zc.buildout': ['default = recipe:GitRecipe']},
    )
