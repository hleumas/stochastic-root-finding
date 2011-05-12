#!/usr/bin/python
import math
import collections
from lfit import LinearFit

def bisection(f, interval, alpha, n):
    a, b = float(interval[0]), float(interval[1])
    x = (a+b)/2
    stepsize = 1.0/alpha
    positions = [x]
    for i in range(1, n + 1):
        x -= stepsize / i * f(x)
        x = sorted([a, x, b])[1]
        positions.append(x)
    return positions

def heuristic(f, interval, alpha, n, m):
    a, b = float(interval[0]), float(interval[1])
    x = (a+b)/2
    positions = [a, b, x]
    lfit = LinearFit()
    lfit.append(a, (a-b) * alpha / 2, 1)
    lfit.append(b, (b-a) * alpha / 2, 1)

    poped = 0
    prejdene = b - a
    sucval = 0
    for i in range(1, n + 1):
        value = float(f(x))
        sucval += abs(value)
        lfit.append(x, value)
        sklon = lfit.a
        if sklon <= 0 or math.isnan(sklon):
            #sklon = alpha
            sklon = abs(sucval / (b-a) / i)
#            x = a if value < 0 else b

        #else:
        #if 1.0 * value / sklon / i > b - a:
        if abs(1.0 * value / sklon) > prejdene:
            #sklon = abs(value) / i / prejdene
            sklon = abs(sucval / (b-a) / i)
            #sklon = alpha

        x -= 1.0 * value / sklon / i
        prejdene += abs(1.0 * value / sklon / i)


        x = sorted([a, x, b])[1]

        positions.append(x)

        if m(i) > poped:
            lfit.popleft()
            poped += 1

    return positions

def newton(f, interval, alpha, n, m):
    a, b = float(interval[0]), float(interval[1])
    x = (a+b)/2
    positions = [a, b, x]
    lfit = LinearFit()
    lfit.append(a, (a-b) * alpha / 2, 1)
    lfit.append(b, (b-a) * alpha / 2, 1)

    poped = 0
    for i in range(1, n + 1):
        value = float(f(x))
        lfit.append(x, value)
        sklon = lfit.a
        if sklon <= 0 or math.isnan(sklon):
            x = a if value < 0 else b

        else:
            x -= 1.0 * value / sklon / i
        x = sorted([a, x, b])[1]

        positions.append(x)

        if m(i) > poped:
            lfit.popleft()
            poped += 1

    return positions
