import os
import sys
from math import *

PI = 3.14159

# Unnecessary global variable
data = []

def badly_named_function(arg1, arg2):
    # No docstring
    sum = arg1 + arg2 # variable name 'sum' shadows built-in function
    print(sum)
    return sum

def calc_circle_area(radius):
    # Use of global variable instead of passing as a parameter
    data.append(radius)
    return PI * radius ** 2

# Unused function
def unused_function(x):
    return x * x

def main():
    # Hardcoding values
    radius = 5
    area = calc_circle_area(radius)
    print("Area of the circle:", area)
    
    # Magic numbers
    print(badly_named_function(3, 7))

# Not using the conventional entry point guard
main()
