Orange3-Spark
=============

A set of widgets for Orange data mining suite to work with Apache Spark ML API.


Requirements
------------

 - Python >= 3.4
 - Pandas
 - Orange 3

Please follow the instruction to install Orange 3 first.

The main Orange project is hosted at: https://github.com/biolab/orange3
Download from: http://orange.biolab.si


Features
--------

  * A Spark Context.
  * A Hive Table.
  * A Dataframe from an SQL Query.
  * A Dataset Builder, basically a call to VectorAssembler, this is usefull before sending data to Estimators.
  * Transformers from the feature module.
  * Estimators from classification module.
  * Estimators from regression module.
  * Estimators from clustering module.
  * Evaluation from evaluator module.
  * A PySpark script executor + PySpark console.
  * DataFrame transformes for Pandas and Orangle Tables

... more coming soon!


Installing
----------

First, you need to have Apache Spark installed. Follow the instructions here:
http://spark.apache.org/docs/latest/

Then you can do:

    pip install Orange3-spark

or install the add-on from the Orange's Options | Add-ons menu. Note, if
installing from Add-ons menu, the installation may fail if not all requirements
are satisfiable.

If you require ODBC connectivity, you need to install `pyodbc`
(which requires `sql.h` available if built with `pip` –
that's `unixodbc-dev` package on Linux).

If install is ok, you should see a new section in Orange containing a series of widgets from Spark ML API.
