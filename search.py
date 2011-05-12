#!/usr/bin/python
import random
import scipy.optimize as optimize
import scipy.special as special
import math
import Gnuplot
import pickle
from stochastic import bisection, newton, heuristic
from lfit import LinearFit

def sigmoid(x, a, b):
    if (-a * (x-b)) > 100:
        return 1.0
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

global minx, maxx
minx, maxx = -20, 20
g = Gnuplot.Gnuplot()
g('set log xy')

def initialize(functions):
    for f in functions:
        f.root = optimize.brentq(lambda x: f(x), minx, maxx)
        #f.lbound = optimize.brentq(lambda x: f(x) - 0.1, minx, maxx)
        #f.ubound = optimize.brentq(lambda x: f(x) - 0.9, minx, maxx)

def measure(function, x):
    if 2 * random.random() < (1.0 + function(x)):
        return 1
    else:
        return -1


def stdev(f, alg, d, n, m, randomness = 100.0):
    F = lambda x: measure(f, x)
    s = [0.0 for i in range(n)]
    for j in range(m):
        a = d/4.0*(-1.0 - 2.0 * j / m)
        b = d/4.0*(3.0 - 2.0 * j / m)
        randfact = random.random() * randomness + 1/randomness
        alpha = (min(f(b), 1.0) - max(f(a), -1.0)) / d * randfact
        result = alg(F, (a,b), alpha, n)
        s = [s[i] + (result[i]-f.root)**2 for i in range(n)]
    return [math.sqrt(s[i]/m) for i in range(n)]

def testuj(functions, alghoritms, d, steps, prec):
    initialize(functions)
    return [
        [
            stdev(i, j, d, steps, prec) 
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


def test(functions, alghoritms, d, steps, prec):
    initialize(functions)
    for i in functions:
        for j in alghoritms:
            vysl = stdev(i, j, d, steps, prec)
            data.append(Gnuplot.Data(range(0, steps), vysl))
            apply(g.plot, data)
        raw_input("Press Enter to continue")


    apply(g.plot, data)


testSet = [
    lambda x: linear(x, 1, 0),
    lambda x: x**3,
    lambda x: sigmoid(x, 1, 0) - 0.5,
    lambda x: erf(x, 1, 0) - 0.5,
    lambda x: cauchy(x, 1, 0) - 0.5,
]


algs = [
    bisection,
    lambda f, interval, alpha, n: 
        newton(f, interval, alpha, n, lambda x: x**0.5 + 1),
    lambda f, interval, alpha, n: 
        heuristic(f, interval, alpha, n, lambda x: x**0.5 + 1),
        ]

result = testuj(testSet, algs, 100, 1000, 100)
#f = open('vystup', 'wb')
#pickle.dump(result, f)
#f.close()
#f = open('vystup', 'rb')
#result = pickle.load(f)

average = averageData(result)
for i in average:
    print round(-sklon(i) * 100)

averagePlot(result)
basicPlot(result)
