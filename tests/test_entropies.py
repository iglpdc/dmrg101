'''
File: test_entropies.py
Author: Ivan Gonzalez
Description: Tests for the entropy functions
'''
import numpy as np
import unittest
from nose.tools import assert_almost_equal, with_setup, assert_true, eq_
from math import log

from dmrg101.core.entropies import *

class TestEntropy(unittest.TestCase):

    def setUp(self):
        self.zeros=np.array([0.0, 0.0, 0.0])
        self.ones=np.array([1.0, 1.0, 1.0])
        self.negatives=np.array([-1.0, -1.0, -1.0])
        self.ok=np.array([0.5, 0.5])
        self.ok_2=np.array([1./3, 1./3, 1./3])
        self.ok_3=np.array([1./2, 1./4, 1./4])

    def test_calculate_entropy(self):
	assert_almost_equal(calculate_entropy(self.zeros), 0.0)
	assert_almost_equal(calculate_entropy(self.ones), 0.0)
	assert_almost_equal(calculate_entropy(self.negatives), 0.0)
	assert_almost_equal(calculate_entropy(self.ok), log(2))
	assert_almost_equal(calculate_entropy(self.ok_2), log(3))

    def test_even_probabilities(self):
	assert_almost_equal(calculate_renyi(self.ok, 2), log(2))
	assert_almost_equal(calculate_renyi(self.ok, 3), log(2))
	assert_almost_equal(calculate_renyi(self.ok, 9), log(2))

    def test_renyi_1_is_von_neumann(self):
	eq_(calculate_entropy(self.ok), calculate_renyi(self.ok, 1))
    
    def test_are_bounded(self):
	assert_true(calculate_entropy(self.ok) >= calculate_renyi(self.ok, 2))
	assert_true(calculate_renyi(self.ok, 2) >= calculate_renyi(self.ok, 3))
	assert_true(calculate_renyi(self.ok, 3) >= calculate_renyi(self.ok, 4))
	assert_true(calculate_entropy(self.ok_3) >= calculate_renyi(self.ok_3, 2))
	assert_true(calculate_renyi(self.ok_3, 2) >= calculate_renyi(self.ok_3, 3))
	assert_true(calculate_renyi(self.ok_3, 3) >= calculate_renyi(self.ok_3, 4))
