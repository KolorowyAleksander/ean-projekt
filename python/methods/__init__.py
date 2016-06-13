#!/usr/bin/env python2
"""Module for the functions themselves"""
from math import fabs
from interval import interval
from interval import imath
from interval import fpu
from interval import inf

class MyError(Exception):
    """Exception for passing message"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

@interval.function
def iabs(c):
    """absolute value"""
    if 0 in interval([c.inf, c.sup]):
        return interval([0, fpu.max((fabs(c.inf), fabs(c.sup)))])
    else:
        return interval([fpu.min((fabs(c.inf), fabs(c.sup))), fpu.max((fabs(c.inf), fabs(c.sup)))])

def newton(x,
           epsilon,
           max_iterations,
           function,
           function_coefficient_list=None,
           function_derivative_coefficient_list=None
          ):
    """Newton method"""
    if max_iterations < 1:
        raise MyError("Iterations lesser than 0")
    else:
        i = 0
        while i != max_iterations:
            i += 1
            x_i = x
            x = x-function(x, function_coefficient_list)\
                /function(x, function_derivative_coefficient_list)
            x_abs = fabs(x)
            x_i_abs = fabs(x_i)
            if x_abs < x_i_abs:
                x_abs = x_i_abs
            if (x_abs == 0) or (fabs(x-x_i)/x_abs <= epsilon):
                break
        return x

def newton_interval(x,
                    epsilon,
                    max_iterations,
                    function,
                    function_coefficients=None,
                    function_derivative_coefficients=None
                   ):
    """Newton interval method"""
    x = interval.cast(x)
    epsilon = interval.cast(epsilon)
    function_coefficient_list = []
    function_derivative_coefficient_list = []
    for number in function_coefficients:
        function_coefficient_list.append(interval.cast(number))
    for number in function_derivative_coefficients:
        function_derivative_coefficient_list.append(interval.cast(number))
    if max_iterations < 1:
        raise MyError("Iterations lesser than 0")
    else:
        i = 0
        while i != max_iterations:
            i += 1
            x_i = x
            if 0 in function(x, function_derivative_coefficient_list):
                raise MyError("Division by interval with 0 inside")
            x = x-function(x, function_coefficient_list)\
                /function(x, function_derivative_coefficient_list)
            x_abs = iabs(x)
            x_i_abs = iabs(x_i)
            if x_abs < x_i_abs:
                x_abs = x_i_abs
            if (0 in x_abs) or (iabs(x-x_i)/x_abs <= epsilon):
                break
        return x


def regula_falsi(a, b, function, function_coefficient_list=None):
    """function taking float parameters returns the floating value"""
    if a >= b:
        raise MyError("A greater than B")
    else:
        a_value = function(a, function_coefficient_list)
        if a_value < 0:
            a_sign = -1
        elif a_value == 0:
            a_sign = 0
        else:
            a_sign = 1
        b_value = function(b, function_coefficient_list)
        if a_sign * b_value > 0:
            raise MyError("A and B are on the same side of 0")
        else:
            x = b - b_value*(b-a)/(b_value - a_value)
            while (a < x) and (x < b):
                x_value = function(x, function_coefficient_list)
                if x_value < 0:
                    sign_value = -1
                elif x_value == 0:
                    sign_value = 0
                else:
                    sign_value = 1
                if a_sign == sign_value:
                    a = x
                    a_value = x_value
                else:
                    b = x
                    b_value = x_value
                x = b - b_value*(b-a)/(b_value-a_value)
            return x

def regula_falsi_interval(a, b, function, function_coefficients=None):
    """same but with intervals"""
    a = interval.cast(a)
    b = interval.cast(b)
    function_coefficient_list = []
    for number in function_coefficients:
        function_coefficient_list.append(interval.cast(number))
    if a >= b:
        raise MyError("A greater than B")
    else:
        a_value = function(a, function_coefficient_list)
        print a_value
        if a_value < interval.cast(0):
            a_sign = -1
        elif a_value == interval.cast(0):
            a_sign = 0
        else:
            a_sign = 1
        b_value = function(b, function_coefficient_list)
        if interval.cast(a_sign) * b_value > interval.cast(0):
            raise MyError("A and B are on the same side of 0")
        else:
            if 0 in b_value - a_value:
                raise MyError("Division by interval with 0 inside")
            x = b - b_value*(b-a)/(b_value - a_value)
            while (a < x) and (x < b):
                x_value = function(x, function_coefficient_list)
                if x_value < interval.cast(0):
                    sign_value = -1
                elif x_value == interval.cast(0):
                    sign_value = 0
                else:
                    sign_value = 1
                if a_sign == sign_value:
                    a = x
                    a_value = x_value
                else:
                    b = x
                    b_value = x_value
                if 0 in b_value - a_value:
                    raise MyError("Division by interval with 0 inside")
                x = b - b_value*(b-a)/(b_value-a_value)
            return x

if __name__ == '__main__':
    pass
