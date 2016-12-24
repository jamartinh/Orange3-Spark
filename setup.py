#!/usr/bin/env python

from setuptools import setup

ENTRY_POINTS = {
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
        'exampletutorials = orangecontrib.spark.tutorials',
    ),
    'orange.addons': (
        'Spark = orangecontrib.spark',
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/spark/widgets/__init__.py
        'Spark Data = orangecontrib.spark.widgets.data',
        'Spark ML = orangecontrib.spark.widgets.ml'
    ),

    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.spark.widgets:WIDGET_HELP_PATH'
    )
}

NAMESPACES = ["orangecontrib"]
KEYWORDS = (
    # [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
    # can be installed using the Orange Add-on Manager
    'orange3 add-ons',
    'Spark',
    'Spark ML',
    'Machine Learning'
)

LONG_DESCRIPTION = open('README.md').read()
LICENSE = open('LICENSE').read()

if __name__ == '__main__':
    setup(
        name="Orange3-spark",
        version='0.2.6',
        author='Jose Antonio Martin H.',
        author_email='xjamartinh@gmail.com',
        url='https://github.com/jamartinh/Orange-Spark',
        description='A series of Widgets for Orange3 to work with Spark ML',
        long_description=LONG_DESCRIPTION,
        license=LICENSE,
        packages=['orangecontrib',
                  'orangecontrib.spark',
                  'orangecontrib.spark.base',
                  'orangecontrib.spark.utils',
                  'orangecontrib.spark.tutorials',
                  'orangecontrib.spark.widgets',
                  'orangecontrib.spark.widgets.data',
                  'orangecontrib.spark.widgets.ml'],
        package_data={
            'orangecontrib.spark': ['tutorials/*.ows'],
            'orangecontrib.spark.widgets': ['icons/*'],
        },
        install_requires=[
            'Orange3',
            'pandas',
            'py4j',
            'sqlparse'

        ],
        extras_require={
            'pyspark': [],

        },
        entry_points=ENTRY_POINTS,
        keywords=", ".join(KEYWORDS),
        namespace_packages=['orangecontrib'],
        include_package_data=True,
        zip_safe=False,
    )
