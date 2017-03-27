#!/usr/bin/python
import random
import scipy.optimize as optimize
import scipy.special as special
import math
import cPickle
from stochastic import bisection, newton, heuristic, secant
from lfit import LinearFit
import cProfile

def sigmoid(x, a, b):
    if a * x > 500.0:
        return 1.0
    if a * x < -500.0:
        return 0.0
    return 1.0/(1.0+math.exp(-a*(x-b)))

def linear(x, a, b):
    return a * (x - b)

def erf(x, a, b):
    return special.erf(a * (x-b))

def cauchy(x, a, b):
    return 1.0/math.pi * math.atan((x-b)*a) + 0.5

def bordel(x):
    if x < 3:
        return 0.07 * x
    if x > 8:
        return 0.3 * x - 1.6
    return 0.118 * (x - 3) + 0.07 * x

def sgn(x):
    if x < 0:
        return -1.0
    else:
        return 1.0

global minx, maxx
minx, maxx = -20, 20

def initialize(functions):
    for f in functions:
        f.root = optimize.brentq(lambda x: f(x), minx, maxx)

def measure(function):
    def m(x):
        if 2 * random.random() < (1.0 + function(x)):
            return 1
        else:
            return -1
    return m


def testuj(functions, alghoritms, d, displ, steps, prec):
    a = lambda k : d * (-displ -  k * (1.0 - 2*displ) / prec)
    (1.0 - 2*displ) / prec
    initialize(functions)
    result = [
        [
            [
                j(measure(i), (a(k), a(k) + d), steps)
                for k in xrange(prec)
            ]
            for i in functions
        ] 
        for j in alghoritms
    ]
    return {
            'algs'   : len(alghoritms),
            'funcs'  : len(functions),
            'prec'   : prec,
            'steps'  : steps,
            'result' : result,
    }



testSet = [
    lambda x: linear(x, 1.0, 0),
    lambda x: x**3,
    lambda x: 2 * sigmoid(x, 1.0, 0.0) - 1.0,
    lambda x: erf(x, 1.0, 0),
    lambda x: 2 * cauchy(x, 1.0, 0) - 1.0,
    lambda x: sgn(x),
]




algs = [
    bisection,
    lambda f, interval,  n: 
        newton(f, interval,  n, lambda x: x**0.5 + 1),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.5 + 1),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 1.3**x),
        ]


"""d = 1024.0
for i in xrange(14):
    result = testuj(testSet, algs, d, 0.1, 128, 1000)
    f = open('vystup_' + str(i) + '.bc', 'wb')
    pickle.dump((result, d), f)
    f.close()
    d /= 2.0
"""
newtonovia = [
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: 1),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.1),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.2),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.3),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.4),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.5),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.6),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.7),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.8),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.9),
        ]
secantovia = [
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 1.1**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 1.3**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 1.7**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 2.2**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 2.8**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 3.5**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 4.0**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 4.5**x),
    lambda f, interval,  n: 
        secant(f, interval,  n, lambda x: 5**x),
        ]
def mymain():
    #for i in [0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0]:
        f = open('AllFunctions', 'wb')
        d = 5.0
        funkcia = lambda x: i * sgn(x)
        result = testuj(testSet, algs, d, 0.1, 1200, 1000)
        cPickle.dump((result, d), f)
        f.close()

mymain()
#cProfile.run('mymain()', 'profileinfo')
