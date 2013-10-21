from math import sqrt

def mae(i_vals=[], o_vals=[], n=1.0):
	"""
	Calculates Mean Absolute Error

	Keyword arguments:
	i_vals -- the list of interpolated values (default [])
	o_vals -- the list of original values (default [])
	n -- the number of observations (default 1.0)

	"""
	value_sum = sum([abs(I - O) for I, O in zip(i_vals, o_vals)]) # calculates the numerator from the formula
	return float(value_sum/n)


def mse(i_vals=[], o_vals=[], n=1.0):
	"""
	Calculates Mean Squared Error

	Keyword arguments:
	i_vals -- the list of interpolated values (default [])
	o_vals -- the list of original values (default [])
	n -- the number of observations (default 1.0)
	
	"""
	value_sum = sum([(I - O)**2 for I, O in zip(i_vals, o_vals)]) # calculates the numerator from the formula
	return float(value_sum/n)

def rmse(i_vals=[], o_vals=[], n=1.0):
	"""
	Calculates Root Mean Squared Error

	Keyword arguments:
	i_vals -- the list of interpolated values (default [])
	o_vals -- the list of original values (default [])
	n -- the number of observations (default 1.0)
	
	"""
	return sqrt(mse(i_vals, o_vals, n)) # returns the square root of the MSE algorithm

def mare(i_vals=[], o_vals=[], n=1.0):
	"""
	Calculates Mean Absolute Relatvie Error

	Keyword arguments:
	i_vals -- the list of interpolated values (default [])
	o_vals -- the list of original values (default [])
	n -- the number of observations (default 1.0)
	
	"""
	value_sum = sum([abs(I - O) / O for I, O in zip(i_vals, o_vals)]) # calculates the numerator from the formula
	return float(value_sum/n)