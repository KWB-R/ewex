import numpy as np
import numpy.lib


class ArrayContainer(numpy.lib.mixins.NDArrayOperatorsMixin):
    attrs = []

    # def __init__(self, arr: np.ndarray, *args):
    #     self.arr = arr

    def __repr__(self):
        return f"{self.__class__.__name__}(array={self.arr})"

    def __len__(self):
        return len(self.arr)

    def __array__(self, dtype=None, copy=None):
        if copy is False:
            return self.arr.astype(dtype)
        return self.arr.copy().astype(dtype)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method == '__call__':
            inputs = tuple(x.arr if isinstance(x, self.__class__) else x for x in inputs)
            return self.__class__(ufunc(*inputs, **kwargs), *(getattr(self, attr) for attr in self.attrs))
        else:
            return NotImplemented(method)
