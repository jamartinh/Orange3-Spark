__author__ = "Jose Antonio Martin H."
__copyright__ = "Copyright 2015, Jose Antonio Martin H."
__credits__ = ["The Orange Machine Learning Project, Jose Antonio Martin H. "]
__license__ = "Apache License 2.0"
__maintainer__ = "JOse Antonio Martin H."
__email__ = "xjamartinh@gmail.com"


class SharedSparkContext:
    _sc = None
    _hc = None

    @property
    def sc(self):
        return SharedSparkContext._sc

    @sc.setter
    def sc(self, val):
        SharedSparkContext._sc = val

    @property
    def hc(self):
        return SharedSparkContext._hc

    @hc.setter
    def hc(self, val):
        SharedSparkContext._hc = val
