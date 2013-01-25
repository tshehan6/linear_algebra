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
import re
import copy

class MatrixMalformedError(Exception):
	pass
class MatrixBadStringError(Exception):
	pass
class MatrixInvalidSizeError(Exception):
	pass
class MatrixDimensionMismatchError(Exception):
	pass
class MatrixSingularError(Exception):
	pass
class MatrixNotSquareError(Exception):
	pass

# matrix
class Matrix:

	# get the identity matrix of size n
	def identity(n):

		# make sure n is a natural number
		if not(n >= 0 and n % 1 == 0):
			raise MatrixInvalidSizeError()

		# construct the matrix
		a = []
		for i in range(n):
			a.append([int(i==j) for j in range(n)])
		return Matrix(a)

	# constructor
	def __init__(self,m):
	
		def from_string(s):

			# make sure the string contains nothing but newline,colon,pipe,comma,space,period,number
			if not re.match('^[\n\r:\| \t,.0-9\\-]*$',s):
				raise MatrixBadStringError()

			m = []
			for row in iter(re.split('\n|\r|:|\|',s)):
				row = row.strip()
				if row == '':
					continue
	
				r = []
				for column in iter(re.split('[ \t,]*',row)):
					if column == '':
						continue
	
					r.append(float(column))
	
				m.append(r.copy())
			return m

		# convert from string to array if necessary
		if isinstance(m,str):
			m = from_string(m)

		# make sure there is atleast one element
		try:
			e = m[0][0]
		except:
			raise MatrixMalformedError()
		# make sure every row has the same number of columns and that all elements are numbers
		# this is not very elegant
		num_columns = len(m[0])
		if(num_columns == 0):
			raise MatrixMalformedError()
		for row in m:
			for element in row:
				if not(	hasattr(element,"__truediv__") and 
					hasattr(element,"__mul__") and 
					hasattr(element,"__add__")):

					raise MatrixMalformedError() 

			if(len(row) != num_columns):
				raise MatrixMalformedError() 

		# set the matrix
		self.m = m
	# get element by subscript 
	def __getitem__(self,i):
		return self.m[i]

	# set element by subscript
	def __setitem__(self,i, value):
		self.m[i] = value

	# get a string representation
	def __repr__(self):
		s = ''
		for row in self.m:
			for  item in row:
				if(item == 0.0):
					item = 0
				if(item % 1 == 0):
					item = round(item)
				s += str(round(item,3)) + ' '
			s += '\n'
		return s

	# get the matrix as a raw two dimensional list
	def get_list(self):
		return list(self.m)

	# get the matrix as a one dimensional list of row major elements
	def flatten(self):
		flat = []
		for i in range(self.num_rows()):
			for j in range(self.num_columns()):
				flat.append(self[i][j])
		return flat

	# get a deep copy of the matrix
	def copy(self):
		return copy.deepcopy(self)

	# get a row as a 1xn matrix
	def row(self,i):
		row = [self[i]]
		return Matrix(row)

	# get a column as a nx1 matrix
	def column(self,j):
		column = []
		for i in range(self.num_rows()):
			column.append([self[i][j]])
		return Matrix(column)

	# get the number of rows
	def num_rows(self):
		return len(self.m)

	# get the number of columns
	def num_columns(self):
		return len(self[0])

	# swap two rows
	def swap_rows(self,a,b):
		new = self.copy()
		for j in range(new.num_columns()):
			new[a][j],new[b][j] = new[b][j],new[a][j]
		return new
	
	# swap two columns
	def swap_columns(self,a,b):
		new = self.copy()
		for i in range(new.num_rows()):
			new[i][a],new[i][b] = new[i][b],new[i][a]
		return new

	# scale a row by a constant
	def scale_row(self,i,k):
		new = self.copy()
		for j in range(new.num_columns()):
			new[i][j] = new[i][j] * k
		return new

	# scale a column by a constant
	def scale_column(self,j,k):
		new = self.copy()
		for i in range(new.num_rows()):
			new[i][j] = new[i][j] * k
		return new

	# add a multiple of a row to another row
	def add_row_multiple(self,dest,source,k):
		new = self.copy()
		for j in range(new.num_columns()):
			new[dest][j] += new[source][j] * k
		return new

	# add a multiple of a column to another column
	def add_column_multiple(self,dest,source,k):
		new = self.copy()
		for i in range(new.num_rows()):
			new[i][dest] += new[i][source] * k
		return new

	# transpose matrix
	def transpose(self):
		b = [	[self[i][j] 
				for i in range(self.num_rows())] 
					for j in range(self.num_columns())]
		return Matrix(b)

	# matrix addition
	def add(self,other):

		if(self.num_rows() != other.num_rows() or self.num_columns() != other.num_columns() ):
			raise MatrixDimensionMismatchError()

		new = [	[self[i][j] + other[i][j] 
				for j in range(self.num_columns())] 
					for i in range(self.num_rows())]
		return Matrix(new)

	#  matrix subtraction
	def subtract(self,other):
		if(self.num_rows() != other.num_rows() or self.num_columns() != other.num_columns() ):
			raise MatrixDimensionMismatchError()

		new = [	[self[i][j] - other[i][j] 
				for j in range(self.num_columns())] 
					for i in range(self.num_rows())]
		return Matrix(new)
	
	# scalar multiplication
	def scalar_multiply(self,k):
		new = [	[self[i][j] * k 
				for j in range(self.num_columns())] 
					for i in range(self.num_rows())]
		return Matrix(new)

	# matrix multiplication
	def multiply(self,other):

		def dot_product(a,b):
			running_sum = 0
			for a,b in zip(a,b):
				running_sum += a*b
			return running_sum

		if(self.num_columns() != other.num_rows()):
			raise MatrixDimensionMismatchError()

		new =[[	dot_product(self.row(i).flatten(),other.column(j).flatten()) 
				for j in range(other.num_columns())]
					for i in range(self.num_rows())]
		return Matrix(new)

	# augmented matrix
	def augment(self,other):

		if self.num_rows() != other.num_rows():
			raise MatrixDimensionMismatchError()

		new = [  [self[i][j] for j in range(self.num_columns())] 
			+[other[i][j] for j in range(other.num_columns())]
			for i in range(self.num_rows())
		]
		return Matrix(new)

	# left n columns
	def left(self,n):
		# make sure n is a natural number
		if not n >=0 and n % 1 == 0 :
			raise MatrixInvalidSizeError()

		new = [self[i][:n] for i in range(self.num_rows())]
		return Matrix(new)

	# right n columns
	def right(self,n):
		# make sure n is a natural number
		if not n >=0 and n % 1 == 0 :
			raise MatrixInvalidSizeError()

		new = [self[i][n:] for i in range(self.num_rows())]
		return Matrix(new)

#TODO:	Clean up the horrible mess below this line.

	# row echelon form
	def row_echelon(self):
		b = self.copy()
		for iteration_row in range(b.num_rows()):

			# find the first suitable pivot
			pivot_row = None ;
			for j in range(b.num_columns()):
				for i in range(iteration_row,b.num_rows()):
					if(b[i][j] != 0):
						pivot_row = i
						pivot_column = j
						break
				if(pivot_row != None):
					break

			# if no pivot was found, the algorithm has finished
			if(pivot_row == None):
				break

			# perform operations about the pivot
			b = b.swap_rows(pivot_row,iteration_row)
			b = b.scale_row(iteration_row, 1 / b[iteration_row][pivot_column] )
			for row in range(iteration_row+1,b.num_rows()):
				b = b.add_row_multiple(row, iteration_row, -b[row][pivot_column])

		return b

	# reduced row echelon form
	def reduced_row_echelon(self):
		new = self.row_echelon()
	
		for i in reversed(range(new.num_rows())):

			# find the leading non zero column in this row, or go to the next row
			leading_column = None
			for j in range(new.num_columns()):
				if new[i][j] !=  0:
					leading_column = j
					break
			if leading_column is None:
				continue

			# clear the column to zero in every row above this one, using row ops
			for row in range(i):
				if new[row][leading_column] != 0:
					new = new.add_row_multiple(row,i,-new[row][leading_column]/new[i][leading_column])
		return new

	# inverse matrix
	def inverse(self):

		# first make sure the matrix is square
		if self.num_rows() != self.num_columns():
			raise MatrixNotSquareError()
			

		i = Matrix.identity(self.num_rows())	
		b = self.augment(i)
		c = b.reduced_row_echelon()
		
		singularity_test = c.left(self.num_columns())
		for row in range(self.num_rows()):
			for column in range(self.num_columns()):
				if(i[row][column] != singularity_test[row][column]):
					raise MatrixSingularError()
		return c.right(self.num_rows())


############################
# Example use of the library
############################
'''
a = Matrix("""
	2 0  1
	2 3 -4
	3 2  2
	""")
b = Matrix("""5:7:3""")
c = Matrix("""|3,2,-1|2,0,-1|0,1,2|""")

print('a: ' + str(a))
print('b: ' + str(b))
print('c: ' + str(c))
print('')

print('a multiplied by c: ')
print(a.multiply(c))
print('')

print('solution to ax=b: ')
a_b = a.augment(b)
x = a_b.reduced_row_echelon() 
print(x)
print('')

print('product of a and c: ')
d = a.multiply(c)
print(d)
print('')

print('difference of a and b: ')
e = a.subtract(c)
print(e)
print('')

print('difference of b and a: ')
f = c.subtract(a)
print(f)
print('') '''
