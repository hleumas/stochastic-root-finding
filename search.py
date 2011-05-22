#!/usr/bin/python
import random
import scipy.optimize as optimize
import scipy.special as special
import math
import Gnuplot
import pickle
from stochastic import bisection, newton, heuristic, secant
from lfit import LinearFit

def sigmoid(x, a, b):
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
g = Gnuplot.Gnuplot()
g('set log xy')

def initialize(functions):
    for f in functions:
        f.root = optimize.brentq(lambda x: f(x), minx, maxx)

def measure(function, x):
    if 2 * random.random() < (1.0 + function(x)):
        return 1
    else:
        return -1


def stdev(f, alg, d, n, m, randomness = 100.0):
    F = lambda x: measure(f, x)
    s = [0.0 for i in range(n)]
    for j in range(m):
        #a = d/4.0*(-1.0 - 2.0 * j / m)
        #b = d/4.0*(3.0 - 2.0 * j / m)
        a = -0.005 * d
        b = 0.995 * d
        result = alg(F, (a,b), n)
        s = [s[i] + (result[i]-f.root)**2 for i in range(n)]
    return [math.sqrt(s[i]/m) for i in range(n)]

def testuj(functions, alghoritms, d, steps, prec, randomness = 100.0):
    initialize(functions)
    return [
        [
            stdev(i, j, d, steps, prec, randomness) 
            for i in functions
        ] 
        for j in alghoritms
    ]

def basicPlot(data):
    for i in range(len(data[0])):
        grafdata = []
        for j in range(len(data)):
            grafdata.append(Gnuplot.Data(range(0, len(data[j][i])), data[j][i]))
            apply(g.plot, grafdata)
        raw_input("Press Enter to continue")

def averageData(data):
    average = []
    for alg in data:
        sum = [0.0 for func in alg[0]]
        for func in alg:
            for k, v in enumerate(func):
                sum[k] += v / len(alg)
        average.append(sum)

    return average

def averagePlot(data):
    average = averageData(data)

    grafdata = []
    for alg in average:
        grafdata.append(Gnuplot.Data(range(0, len(alg)), alg))
        apply(g.plot, grafdata)
    raw_input('Press Enter to continue...')

def sklon(data):
    lfit = LinearFit()
    for i, j in enumerate(data):
        lfit.append(math.log(i+1), math.log(j))
    return lfit.a


testSet = [
#    lambda x: linear(x, 1.0, 0),
#    lambda x: x**3,
    lambda x: 2 * sigmoid(x, 3.0, 0.0) - 1.0,
#    lambda x: 2 * erf(x, 1.0, 0) - 1.0,
#    lambda x: 2 * cauchy(x, 1.0, 0) - 1.0,
]



algs = [
#    bisection,
#    lambda f, interval,  n: 
#        newton(f, interval,  n, lambda x: x**0.5 + 1),
    lambda f, interval,  n: 
        heuristic(f, interval,  n, lambda x: x**0.5 + 1),
    secant 
        ]

result = testuj(testSet, algs, 1000.0, 256, 100, 1.0)
#f = open('vystup1l1', 'wb')
#pickle.dump(result, f)
#f.close()
#f = open('vystup10l100', 'rb')
#result = pickle.load(f)

#average = averageData(result)
#for i in average:
    #print round(-sklon(i) * 100)
averagePlot(result)
basicPlot(result)


#sigmoska = lambda x: measure(lambda y: 2 * sigmoid(y, 6.0, 0.0)-1.0, x)

#print secant(sigmoska, [-5.0, 1000], 100)
