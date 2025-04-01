"""This module computes Bell polynomials."""

import numpy as np
import scipy.special as sc


class Bell:
    """A class for complete Bell polynomials."""

    def compute(self, x):
        """Method to compute Bell polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials. The first element of `x`, that is, `x[0]`, must be zero.

        Returns:
            A :obj:`numpy.array` containing the Bell polynomials for the input `x` up to order \
            equal to the index of the last element of `x`.

        """

        assert x[0] == 0
        result = np.zeros(len(x))
        result[0] = 1
        for m in range(len(x) - 1):
            for i in range(m + 1):
                result[m + 1] += sc.binom(m, i) * result[m - i] * x[i + 1]
        return result

    def invert(self, b):
        """Method to invert Bell polynomials, that is, to find the x elements that will give the \
        input Bell polynomials.

        Args:
            ``b`` (:obj:`list` or :obj:`numpy.array`): An array containing the Bell polynomials.\
            The first element, `b[0]`, must equal 1.

        Returns:
            A :obj:`numpy.array` containing the x's giving rise to the input polynomials.

        """
        x = np.array([0])
        for n in range(len(b) - 1):
            my_sum = b[n + 1]
            for i in range(n):
                my_sum -= sc.binom(n, i) * b[n - i] * x[i + 1]
            x = np.append(x, my_sum)
        return x


class PartialBell:
    """A class for partial Bell polynomials."""

    def compute(self, x):
        """Method to compute partial Bell polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials.  The first value, `x[0]`, must equal zero.

        Returns:
            A 2-d :obj:`numpy.array` containing the partial Bell polynomials B\\ :sub:`n,k`. \
            `n` equals the largest index of the input `x` array.  `k` ranges from 0 to `n`.

        """

        assert x[0] == 0

        b = np.zeros([len(x), len(x)])
        b[0, 0] = 1

        for n in range(1, len(x)):
            for k in range(1, len(x)):
                for i in range(1, n - k + 2):
                    b[n, k] += sc.binom(n - 1, i - 1) * x[i] * b[n - i, k - 1]

        return b

    def invert(self, pb):
        """Method to invert the partial Bell polynomials, that is, to find the x elements \
        that will give the input Bell polynomials.

        Args:
            ``pb`` (:obj:`numpy.array`): A 2-d array giving the partial Bell \
             polynomials B\\ :sub:`n,k`

        Returns:
            A :obj:`numpy.array` containing the input *x* values that give the input \
            partial Bell polynomials.

        """

        x = np.zeros(pb.shape[0])
        x[0] = 0

        for n in range(1, len(x)):
            x[n] = pb[n, 1]

        return x
