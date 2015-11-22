#!/usr/bin/env python

from setuptools import setup

ENTRY_POINTS = {
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
        'exampletutorials = orangecontrib.spark.tutorials',
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/spark/widgets/__init__.py
        'Spark = orangecontrib.spark.widgets',
    ),

    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.spark.widgets:WIDGET_HELP_PATH',)
}

KEYWORDS = (
    # [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
    # can be installed using the Orange Add-on Manager
    'orange3 add-ons',
)

if __name__ == '__main__':
    setup(
        name = "Orange3-spark",
        version='0.1.1',
        author = 'Jose Antonio Martin H',
        author_email = 'xjamartinh@gmail.com',
        url = 'https://github.com/jamartinh/Orange-Spark',
        description = 'A series of Widgets for Orange3 to work on a Spark Cluster',
        packages = ['orangecontrib',
                    'orangecontrib.spark',
                    'orangecontrib.spark.base',
                    'orangecontrib.spark.utils',
                    'orangecontrib.spark.tutorials',
                    'orangecontrib.spark.widgets'],
        package_data = {
            'orangecontrib.spark': ['tutorials/*.ows'],
            'orangecontrib.spark.widgets': ['icons/*'],
        },
        install_requires = ['Orange', 'pandas'],
        entry_points = ENTRY_POINTS,
        keywords = KEYWORDS,
        namespace_packages = ['orangecontrib'],
        include_package_data = True,
        zip_safe = False,
    )

"""
name	name of the package	short string	(1)
version	version of this release	short string	(1)(2)
author	package author’s name	short string	(3)
author_email	email address of the package author	email address	(3)
maintainer	package maintainer’s name	short string	(3)
maintainer_email	email address of the package maintainer	email address	(3)
url	home page for the package	URL	(1)
description	short, summary description of the package	short string
long_description	longer description of the package	long string	(5)
download_url	location where the package may be downloaded	URL	(4)
classifiers	a list of classifiers	list of strings	(4)
platforms	a list of platforms	list of strings
license	license for the package	short string
"""
