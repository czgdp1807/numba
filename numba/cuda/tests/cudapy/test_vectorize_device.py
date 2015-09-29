from __future__ import absolute_import, print_function, division
from numba import vectorize
from numba import cuda, float32
import numpy as np
from numba import unittest_support as unittest
from numba.cuda.testing import skip_on_cudasim


@cuda.jit(float32(float32, float32, float32), device=True)
def cu_device_fn(x, y, z):
    return x ** y / z


def cu_ufunc(x, y, z):
    return cu_device_fn(x, y, z)


@skip_on_cudasim('ufunc API unsupported in the simulator')
class TestCudaVectorizeDeviceCall(unittest.TestCase):
    def test_cuda_vectorize_device_call(self):
        ufunc = vectorize([float32(float32, float32, float32)], target='cuda')(
            cu_ufunc)

        N = 100

        X = np.array(np.random.sample(N), dtype=np.float32)
        Y = np.array(np.random.sample(N), dtype=np.float32)
        Z = np.array(np.random.sample(N), dtype=np.float32) + 0.1

        out = ufunc(X, Y, Z)

        gold = (X ** Y) / Z

        self.assertTrue(np.allclose(out, gold))


if __name__ == '__main__':
    unittest.main()