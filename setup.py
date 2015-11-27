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
        'Spark Data = orangecontrib.spark.widgets.data',
        'Spark ML = orangecontrib.spark.widgets.ml',
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
                    'orangecontrib.spark.widgets',
                    'orangecontrib.spark.widgets.data',
                    'orangecontrib.spark.widgets.ml'],
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
