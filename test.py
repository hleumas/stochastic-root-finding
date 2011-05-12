#!/usr/bin/python
import search
import math
import scipy.special as special
import scipy.optimize as optimize
import collections
import random
import openopt

class LinearFit2:
    def __init__(self):
        self.points = collections.deque()
        self.a      = float('nan')
        self.b      = float('nan')
    

    def _entropy(self, x):
        a, b = x
        if a < 0:
            return float('inf')
        suma = 0
        pos = [i[0] for i in self.points]
        l = min(pos)
        r = max(pos)
        if a * (r-l) > 1:
            return 1000

        for i in self.points:
            if i[1]:
                if a * i[0] + b <= 0:
                    #return float('inf')
                    return 1000
                if a * i[0] + b < 1:
                    suma += math.log(a * i[0] + b)
                else:
                    return 1000
            else:
                if a * i[0] + b >= 1:
                    #return float('inf')
                    return 1000
                if a * i[0] + b > 0:
                    suma += math.log(1 - a*i[0] - b)
                else:
                    return 1000

        return -suma

    def _recalculate(self):
        if len(self.points) == 0:
            return
        #self.a, self.b = #optimize.anneal(self._entropy, [0,0])[0]
        pos = [i[0] for i in self.points]
        l = min(pos)
        r = max(pos)
        if r != l:
            bb = min([1.0/(r-l), 10])
        else:
            bb = 10
        p = openopt.GLP(self._entropy, lb = [0,-10], ub = [bb,10], maxIter=1e5,
                maxFunEvals=1e4, maxNonSuccess = 500, iprint=-1)
        r = p.solve('galileo')
        self.a, self.b = r.xf

    def append(self, x, y, weight = 1):
        self.points.append((x, y))
        self._recalculate()

    def popleft(self):
        self.points.popleft()
        self._recalculate()

class LinearFit:
    def __init__(self):
        self.count  = 0.0
        self.sumx   = 0.0
        self.sumy   = 0.0
        self.sumx2  = 0.0
        self.sumxy  = 0.0
        self.points = collections.deque()
        self.a      = float('nan')
        self.b      = float('nan')

    def _append(self, x, y, weight=1.0):
        self.count += weight
        self.sumx  += x * weight
        self.sumy  += y * weight
        self.sumx2 += x**2 * weight
        self.sumxy += x * y * weight

        det = self.sumx2 * self.count - self.sumx**2
        apart = self.sumxy * self.count - self.sumy * self.sumx
        bpart = self.sumx2 * self.sumy - self.sumxy * self.sumx

        if det == 0:
            if apart == 0:
                self.a = float('nan')
            else:
                self.a = float('inf')
            if bpart == 0:
                self.b = float('nan')
            else:
                self.b = float('inf')
        else:
            self.a = apart / det
            self.b = bpart / det

    def append(self, x, y, weight=1.0):
        x, y, weight = float(x), float(y), float(weight)
        self._append(x, y, weight)
        self.points.append((x, y, weight))

    def appendleft(self, x, y, weight=1.0):
        x, y, weight = float(x), float(y), float(weight)
        self._append(x, y, weight)
        self.points.appendleft((x, y, weight))

    def popleft(self):
        point = self.points.popleft()
        #print point
        self._append(point[0], point[1], -point[2])

    def trypop(self):
        if self.count < 2:
            return
        nsx = (self.sumx - self.points[0][0]) / math.sqrt(self.count - 1)
        nsx2 = self.sumx2 - self.points[0][0]**2
        err = 1.0 / math.sqrt(nsx2 - nsx**2)
        point = self.points[0]
        a = self.a
        self.popleft()
        if abs(a - self.a) / err < 2 * math.log(self.count):
            self.appendleft(*point)
        

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

testSet = [
    lambda x: linear(x, 1, 0),
    lambda x: linear(x, 0.2, 0),
    lambda x: sigmoid(x, 0.2, 0),
    lambda x: erf(x, 1, 0),
    lambda x: cauchy(x, 0.5, 0),
]

linearSet = [
        lambda x: linear(x, 1, 0),
        ]
cauchySet = [
        lambda x:cauchy(x, 1, 0),
        ]
sigmoidSet = [
        lambda x:sigmoid(x, 1, 0),
        ]
errtest = [
        lambda x:erf(x, 1, 0)
        ]

bordelset = [bordel]

def bisection(function, start1, start2, n):
    start = (float(start1) + float(start2)) / 2
    stepsize = (start2 - start1) / 2
    "Klesa s odmocninou z n"
    stepsize = float(stepsize)
    positions = [start]
    for i in range(1, n + 1):
        start += stepsize / i * (0.5 - search.measure(function, start))
        positions.append(start)
    return positions

def newton(function, start1, start2, n, fitmethod=LinearFit, typ=0):
    start1, start2 = float(start1), float(start2)
    start = (start1 + start2) / 2
    positions = [start1, start2, start]
    lfit = fitmethod()
    lfit.append(start1, 0, 1)
    lfit.append(start2, 1, 1)
    j = 1
    k = 1
    sm = 0
    hm = 1
    for i in range(1, n + 1):
        m = search.measure(function, start)
        lfit.append(start, m, 1.0)
        a = lfit.a
        if a <= 0:
            a = 1.0 / (start2 - start1)
        start += 1.0 * (0.5 - m) / a / i
        if start < start1:
            start = start1
        if start > start2:
            start = start2
        positions.append(start)
        sm += 1.0/i
        #if a < 0.001:
            #print (i, a)
            #print lfit.points
        if typ == 0:
            if math.log(i, 1.9) > j + 0:
       # if i**0.5 > j + 1:
                j += 1
                lfit.popleft()
        elif typ == 1:
            if i**0.4 > j + 1:
                lfit.popleft()
                j += 1
            #if math.sqrt(lfit.sumx2 - lfit.sumx**2/lfit.count) + math.log(j) > j * (start2 - start1):
            #    j += 1
            #    lfit.popleft()
            #lfit.trypop()
        elif typ == 2:
            if sm / math.log(1.88) > hm + 1: #1.4 * hm byvalo fajn
                hm += 1.0#/k
                lfit.popleft()
                k += 1
        else:
            if sm - 1.0/k > 2.5:
                    sm -= 1.0/k
                    k += 1
                    lfit.popleft()
    return positions

def linapp(function, start1, start2, n):
    start1, start2 = float(start1), float(start2)
    start = (start1 + start2) / 2
    positions = [start1, start2, start]
    lfit = LinearFit2()
    lfit.append(start1, 0, 1)
    lfit.append(start2, 1, 1)
    j = 1

    for i in range(1, n + 1):
        m = search.measure(function, start)
        lfit.append(start, m, 1.0)

        a = lfit.a
        if lfit.a <= 0:
            a = 1.0 / (start2 - start1)
        start = ((0.5 - lfit.b) / a + (i-1) * start) / i
        if start < start1:
            start = start1
        if start > start2:
            start = start2
        positions.append(start)

        if math.log(i, 2) > j + 1:
            j += 1
            lfit.popleft()

    return positions



algs = [
    lambda f,n: bisection(f, f.lbound * (random.random() + 0.5), f.ubound *
        (random.random() + 0.5), n),
    lambda f,n: newton(f, f.lbound * (random.random() + 0.5), f.ubound *
        (random.random() + 0.5), n),
    lambda f,n: linapp(f, f.lbound * (random.random() + 0.5), f.ubound *
        (random.random() + 0.5), n),
]

algs2 = [
    lambda f,n: bisection(f, -800, 3, n),
    lambda f,n: newton(f, -800, 3, n),
    lambda f,n: newton(f, -800, 3, n, typ=1),
#    lambda f,n: newton(f, -80, 3, n, typ=2),
#    lambda f,n: newton(f, -10, 20, n, typ=3),
    #lambda f,n: newton(f, -80, 30, n, LinearFit2),
    #lambda f,n: linapp(f, -5, 10, n),
]

#search.initialize(testSet)
#print testSet[1].lbound
#print testSet[1].ubound
#print newton(testSet[1], testSet[1].lbound, testSet[1].ubound, 100)
#print linapp(testSet[2], 0, 100)
#print bisection(testSet[1], 0, 1, 10000)
#print testSet[1].root
#search.test(bordelset, algs2, 100, 1000)
#raw_input()
#search.test(sigmoidSet, algs2, 100, 1000)
#raw_input()
search.test(sigmoidSet, algs2, 100, 1000)
raw_input()
