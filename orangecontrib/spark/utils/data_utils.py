'''
Created on 20/02/2014

@author: Jose Antonio Martin
'''

import csv
from collections import OrderedDict
from io import StringIO

import Orange
import numpy as np
import pandas as pd
import sqlparse


def format_sql(str_sql):
    return str(sqlparse.format(str_sql, reindent = True, keyword_case = 'upper'))


def pandas_to_orange(df):
    domain, attributes, metas = construct_domain(df)
    orange_table = Orange.data.Table.from_numpy(domain = domain, X = df[attributes].values, Y = None, metas = df[metas].values, W = None)
    return orange_table


def orange_to_pandas(dt):
    fileIO = StringIO()
    save_csv_IO(dt, fileIO, delimiter = ',')
    pandas_data_frame = pd.read_csv(fileIO)
    del fileIO
    return pandas_data_frame


def construct_domain(df):
    columns = OrderedDict(df.dtypes)
    attributes = OrderedDict()
    metas = OrderedDict()
    for name, dtype in columns.items():

        if issubclass(dtype.type, np.number):
            if len(df[name].unique()) >= 13 or issubclass(dtype.type, np.inexact):
                attributes[name] = Orange.data.ContinuousVariable(name)
            else:
                df[name] = df[name].astype(str)
                attributes[name] = Orange.data.DiscreteVariable(name, values = sorted(df[name].unique().tolist()))
        else:
            df[name] = df[name].values.astype(str)
            metas[name] = Orange.data.StringVariable(name)

    domain = Orange.data.Domain(attributes = attributes.values(), metas = metas.values())

    return domain, list(attributes.keys()), list(metas.keys())


def save_csv_IO(data, fileIO, delimiter = ','):
    writer = csv.writer(fileIO, delimiter = '')
    all_vars = data.domain.variables + data.domain.metas
    writer.writerow([v.name for v in all_vars])  # write variable names
    if delimiter == '\t':
        flags = ([''] * len(data.domain.attributes)) + \
                (['class'] * len(data.domain.class_vars)) + \
                (['m'] * len(data.domain.metas))

        for i, var in enumerate(all_vars):
            attrs = ["{0!s}={1!s}".format(*item).replace(" ", "\\ ")
                     for item in var.attributes.items()]
            if attrs:
                flags[i] += (" " if flags[i] else "") + (" ".join(attrs))

        writer.writerow([type(v).__name__.replace("Variable", "").lower()
                         for v in all_vars])  # write variable types
        writer.writerow(flags)  # write flags
    for ex in data:  # write examples
        writer.writerow(ex)


def load_csvIO(fileIO, domain):
    """ Load an Orange.data.Table from s csv file with specified domain.
    
    """
    delimiter = None
    quotechar = None
    escapechar = None
    skipinitialspace = None
    snifer = csv.Sniffer()
    sample = fileIO.read(10 * 2 ** 20)
    try:
        dialect = snifer.sniff(sample)
    except csv.Error:
        # try the default, hope the provided arguments are correct
        dialect = "excel"

    fileIO.seek(0)  # Rewind

    def kwparams(**kwargs):
        """Return not None kwargs.
        """
        return dict([(k, v) for k, v in kwargs.items() if v is not None])

    # non-None format parameters.
    fmtparam = kwparams(delimiter = delimiter,
                        quotechar = quotechar,
                        escapechar = escapechar,
                        skipinitialspace = skipinitialspace)

    reader = csv.reader(fileIO, dialect = dialect, **fmtparam)
    next(reader)

    data = list()
    map(data.append, reader)

    table = Orange.data.Table(domain, data)

    return table
