__author__ = 'brandon'
#This file is to be used to generate the Leave one out cross validation formulas for calculating the IDW.
import math

def loocv(i_vals=[], o_vals=[], n=1.0):
    e_vals=[]
    for I, O in zip(i_vals, o_vals):
        error = math.abs(I-O)/O
        e_vals.append(error)
