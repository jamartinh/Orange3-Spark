# Orange-Spark
A set of widgets for Python's Orange Machine Learning to work over Apache Spark ML (Machine Learnint) API

The main Orange proyect is hosted at https://github.com/biolab/orange3


Please follow the instruction to install Orange first.

Then simply run python setup.py to test the Add on.

If install is Ok, you will see a new section in Orange ML containing a series of widgets from Spark ML API.

It includes:
  * A Spark Context.
  * A Hive Table.
  * A Dataframe from an SQL Query.
  * A Dataset Builder, basically a call to VectorAssembler, this is usefull before sending data to Estimators.
  * Transformers from the feature module.
  * Estimators from classification module.
  * Estimators from regression module.
  * Estimators from clustering module.
  * Evaluation from evaluator module.
  * A PySpark script executor + PySparl console.
  * DataFrame transformes for Pandas and Orangle Tables
