"""This module computes various symmetric polynomials."""

import numpy as np
import scipy.special as sc


class Elementary:
    """A class for elementary homogeneous symmetric polynomials."""

    def compute(self, x, n):
        """Method to compute elementary homogeneous symmetric polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute the \
            polynomials.  The value must be less than or equal to the length of the input array.

        Returns:
            A :obj:`numpy.array` containing the elementary homogeneous symmetric polynomials.

        """
        assert 0 <= n <= len(x)
        result = np.array([1])
        y = x.copy()

        for _ in range(n):
            result = np.append(result, sum(y))
            for j in range(len(y)):
                y[j] = 0
                for k in range(j + 1, len(y)):
                    y[j] += x[j] * y[k]

        return result

    def compute_normalized(self, x, n):
        """Method to compute normalized elementary homogeneous symmetric polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements \
            from which to compute the polynomials.

            `n`` (:obj:`int`): A non-negative integer giving the order to which to compute \
            the polynomials.  The value must be less than or equal to the length of the input array.

        Returns:
            A :obj:`numpy.array` containing the elementary homogeneous symmetric polynomials \
            normalized by the number of terms in each polynomial.

        """
        result = self.compute(x, n)
        for i in range(len(result)):
            result[i] /= sc.binom(len(x), i)
        return result


class Complete:
    """A class for complete homogeneous symmetric polynomials."""

    def compute(self, x, n):
        """Method to compute complete homogeneous symmetric polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute \
            the polynomials.

        Returns:
            A :obj:`numpy.array` containing the complete homogeneous symmetric polynomials.

        """
        assert n >= 0
        result = np.array([1])
        y = x.copy()

        for _ in range(n):
            result = np.append(result, sum(y))
            for j in range(len(y)):
                my_sum = 0
                for k in range(j, len(y)):
                    my_sum += x[j] * y[k]
                y[j] = my_sum

        return result

    def compute_normalized(self, x, n, m=0):
        """Method to compute normalized complete homogeneous symmetric polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute \
            the polynomials.

            ``m`` (:obj:`int`, optional): A non-negative integer giving the normalization degree.  \
            This must be less than the length of *x*.

        Returns:
            A :obj:`numpy.array` containing the complete homogeneous symmetric polynomials \
            normalized by the number of terms in the polynomial.

        """
        assert len(x) > 0
        assert m <= len(x)
        result = self.compute(x, n)
        for i in range(len(result)):
            result[i] /= sc.binom(i + len(x) - m - 1, i)
        return result


class PowerSum:
    """A class for power sum polynomials."""

    def compute(self, x, n):
        """Method to compute power sum symmetric polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute the \
            polynomials.

        Returns:
            A :obj:`numpy.array` containing the power sum symmetric polynomials up to order `n`.

        """
        assert n >= 0
        result = np.array([1])
        y = x.copy()

        for _ in range(n):
            result = np.append(result, sum(y))
            for j in range(len(y)):
                y[j] *= x[j]

        return result

    def compute_normalized(self, x, n):
        """Method to compute normalized power sum symmetric polynomials.

        Args:
            ``x`` (:obj:`list` or :obj:`numpy.array`): An array containing the elements from which \
            to compute the polynomials.

            ``n`` (:obj:`int`): A non-negative integer giving the order to which to compute \
            the polynomials.

        Returns:
            A :obj:`numpy.array` containing the power sum polynomials up to order `n` normalized \
            by the number of terms in the polynomial.

        """
        result = self.compute(x, n)
        for i in range(1, len(result)):
            result[i] /= len(x)
        return result
