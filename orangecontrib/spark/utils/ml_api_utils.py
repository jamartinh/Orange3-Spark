import inspect
from collections import OrderedDict

from pyspark import SparkConf, SparkContext


def get_object_info(obj, sc = None):
    """
    Ugly code, please help in cleaning and optimizing it!
    :param obj: object to inspect
    :param sc:  an optional spark (initialized) context
    :return: all the info of the object to display an create the object.
    """

    if not sc:
        conf = SparkConf().setAppName('dummy_local').setMaster('local[1]')
        sc = SparkContext(conf = conf)

    # is_transform = 'transform' in dir(obj)
    # is_estimator = 'fit' in dir(obj)
    is_model = 'java_model' in inspect.getargspec(obj).args

    # ml_api_obj_type = 'Transformer' if is_transform else 'Estimator' if has_fit else None

    obj_name = str(obj).split("'")[1]
    obj_doc = str(inspect.getdoc(obj).split('>>>')[0]).strip()

    parameters = OrderedDict()
    sig = inspect.signature(obj)
    full_description = obj_name + str(sig)

    for name, p in sig.parameters.items():
        parameters[name] = [p.default]

    if not is_model:
        params = obj().params
        for p in params:
            parameters[p.name] += [p.doc]
        full_description += str(obj().explainParams())

    return obj_name, obj_doc, parameters, full_description


def get_models(module):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if 'transform' in dir(c) and not inspect.isabstract(c) and 'java_model' not in inspect.getargspec(c).args }


def get_transformers(module):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if 'transform' in dir(c) and not inspect.isabstract(c) }


def get_estimators(module):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if 'fit' in dir(c) and not inspect.isabstract(c) }


def get_ml_modules():
    from pyspark.ml import feature, classification, clustering, recommendation, regression, tuning, evaluation

    modules = [feature, classification, clustering, recommendation, regression, tuning, evaluation]
    return { m.__name__: [m, str(inspect.getdoc(m)).split('>>>')[0].strip()] for m in modules }


def get_module_info(module):
    return str(inspect.getdoc(module)).split('>>>')[0].strip()


if __name__ == '__main__':

    modules = get_ml_modules()
    name, doc_module = list(modules.items())[0]
    module, doc = doc_module

    print(name)
    print(doc)

    transformers = get_transformers(module)
    estimators = get_estimators(module)

    # filter objects by Estimator or Transformer


    if len(transformers):
        ml_api_obj_type, obj_name, obj_doc, dict_doc, full_description = get_object_info(estimators[6])
        print(ml_api_obj_type)
        print(obj_name)
        print(obj_doc)
        print(dict_doc)
        print(full_description)
