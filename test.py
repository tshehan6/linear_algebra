"""
Linear Algebra Library - A side-effect free matrix class, written in python
Copyright (C) 2012 - 2013 Tom Shehan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact Information:
-------------------
- Email: tshehan6 _a_t_ gmail dot com

"""


import unittest
from matrix import *


class MatrixInitFromMalformed(unittest.TestCase):
	def setUp(self):
		a = [['a','b','c'],['d','e','f']]

		b = [[1,2,3],['a','b','c'],[6,7,8]]

		c = [[1,2,3],[4,5],[6,7,8]]

		d = [[1,2,3],[4,5,6],[7,8,9,10]]

		e = []

		self.malformed_matrices = [a,b,c,d,e]

	def test_raises_exception(self):
		for malformed in self.malformed_matrices:
			self.assertRaises(MatrixMalformedError, Matrix, malformed)


class MatrixInitFromBadString(unittest.TestCase):
	def setUp(self):
		a = """abc"""
		b = """!@#$%^&*()"""
		c = """1 ' 2 ' 3 '"""
		d = """1;2;3"""
		self.bad_strings = [a,b,c,d]

	def test_raises_exception(self):
		for bad in self.bad_strings:
			self.assertRaises(MatrixBadStringError, Matrix, bad)


class MatrixInverseOfSingular(unittest.TestCase):
	def setUp(self):
		self.singular = Matrix("""	1  0 0
						-2 0 0
						4  6 1""")
	def test_raises_exception(self):
		self.assertRaises(MatrixSingularError, Matrix.inverse, self.singular)

class MatrixNonNaturalIdentitySize(unittest.TestCase):
	def test_negative_raises_exception(self):
		self.assertRaises(MatrixInvalidSizeError, Matrix.identity,-5)
	def test_float_raises_exception(self):
		self.assertRaises(MatrixInvalidSizeError, Matrix.identity,2.3)

class MatrixAdditionMismatch(unittest.TestCase):
	def setUp(self):
		self.a = Matrix("""
				1 0 0
				0 1 0
				0 0 1
				""")
		self.b = Matrix("""
				1 0
				0 1
				0 0
				""")
		self.c = Matrix("""
				0 1 0
				0 0 1
				""")

	def test_different_columns_raises_exception(self):
		self.assertRaises(MatrixDimensionMismatchError, self.a.add,self.b)
	def test_different_rows_raises_exception(self):
		self.assertRaises(MatrixDimensionMismatchError, self.a.add,self.c)
	def test_different_rows_and_columns_raises_exception(self):
		self.assertRaises(MatrixDimensionMismatchError, self.b.add,self.c)



if __name__ == '__main__':
	unittest.main()
