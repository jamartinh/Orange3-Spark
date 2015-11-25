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
    del_sc = False
    if not sc:
        conf = SparkConf().setAppName('dummy_local').setMaster('local[1]').set('spark.app.id', 'dummy')
        sc = SparkContext(conf = conf)
        del_sc = True

    # is_transform = 'transform' in dir(obj)
    # is_estimator = 'fit' in dir(obj)
    is_model = 'java_model' in inspect.getargspec(obj).args

    # ml_api_obj_type = 'Transformer' if is_transform else 'Estimator' if has_fit else None

    obj_name = str(obj).split("'")[1]
    obj_doc = str(inspect.getdoc(obj).split('>>>')[0]).strip()
    sig = inspect.signature(obj)

    parameters = OrderedDict()

    for name, p in sig.parameters.items():
        parameters[name] = [len(parameters), p.default]

    full_description = "<!DOCTYPE html><html><body>"
    full_description += "<h4>" + obj_name + str(sig) + "</h4>"

    full_description += "<p>" + str(inspect.getdoc(obj)).split('>>>')[0].strip() + "</p>"

    if not is_model:
        full_description += "<h6> Parameters: </h6>"
        full_description += "<ul>"
        params = obj().params

        for p in sorted(filter(lambda p: p.name in parameters, params), key = lambda p: parameters[p.name][0]):
            parameters[p.name] += [p.doc]
            full_description += "<li>" + p.doc + "</li>"

        # for line in obj().explainParams().split('\n'):
        full_description += "</ul>"
        full_description += "</body></html>"

    if del_sc:
        sc.stop()

    return obj_name, obj_doc, parameters, full_description


def get_models(self = None, module = None):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if
             'transform' in dir(c) and not inspect.isabstract(c) and 'java_model' not in inspect.getargspec(c).args and not name.startswith('Java') }


def get_evaluators(self = None, module = None):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if
             'evaluate' in dir(c) and not inspect.isabstract(c) and 'java_model' not in inspect.getargspec(c).args and not name.startswith('Java') and name != 'Evaluator' }


def get_transformers(self = None, module = None):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if 'transform' in dir(c) and not inspect.isabstract(c) and not name.endswith('Model') and not name.startswith('Java') }


def get_estimators(self = None, module = None):
    members = inspect.getmembers(module, inspect.isclass)
    return { name: c for name, c in members if 'fit' in dir(c) and not inspect.isabstract(c) and not name.startswith('Java') }


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
        ml_api_obj_type, obj_name, obj_doc, dict_doc, full_description = get_object_info(estimators[0])
        print(ml_api_obj_type)
        print(obj_name)
        print(obj_doc)
        print(dict_doc)
        print(full_description)
