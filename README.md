Orange3-Spark
==================

A set of widgets for Python's Orange Machine Learning to work over Apache Spark ML (Machine Learnint) API



Requirements:
-----------------

 - Python >=3.4
 
 - Pandas
 
 - Orange3

Please follow the instruction to install Orange3 first.
The main Orange proyect is hosted at: https://github.com/biolab/orange3






It includes:
-------------------

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

Installing:
---------------

pip install Orange3-spark

or from the Orange3 add-on menu.

If install is Ok, you will see a new section in Orange ML containing a series of widgets from Spark ML API.

