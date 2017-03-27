#!/usr/bin/python
import math
import collections
from lfit import LinearFit

def bisection(f, interval, n):
    a, b = float(interval[0]), float(interval[1])
    x = (a+b)/2
    stepsize = (b-a)
    positions = [x]
    for i in range(1, n + 1):
        x -= stepsize / i * f(x)
        x = sorted([a, x, b])[1]
        positions.append(x)
    return positions

def heuristic(f, interval, n, m):
    a, b = float(interval[0]), float(interval[1])
    x = (a+b)/2
    positions = [a, b, x]
    lfit = LinearFit()
    lfit.append(a, -1.0, 1)
    lfit.append(b, 1.0, 1)

    poped = 0
    prejdene = b - a
    sucval = 0
    for i in range(1, n + 1):
        value = float(f(x))
        sucval += abs(value)
        lfit.append(x, value)
        sklon = lfit.a
        if sklon <= 0 or math.isnan(sklon):
            sklon = abs(sucval / (b-a) / i)

        if abs(1.0 * value / sklon) > prejdene:
            sklon = abs(sucval / (b-a) / i)

        x -= 1.0 * value / sklon / i
        prejdene += abs(1.0 * value / sklon / i)


        x = sorted([a, x, b])[1]

        positions.append(x)

        if m(i) > poped:
            lfit.popleft()
            poped += 1

    return positions

def newton(f, interval, n, m):
    a, b = float(interval[0]), float(interval[1])
    x = (a+b)/2
    positions = [a, b, x]
    lfit = LinearFit()
    lfit.append(a, -1.0, 1)
    lfit.append(b, 1.0, 1)

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

def secant(f, interval, n, m):

    #m = lambda x: 5**x#1.3**x
    points = [[float(interval[0]), -1.0, 1000], [float(interval[1]), 1.0, 1000]]
    positions = [points[0][0], points[1][0]]

    def premeraj(j, k):
        if points[j][2] >= k:
            return 0

        suma = points[j][1] * points[j][2]
        pocmer = 0
        while points[j][2] < k:
            suma += float(f(points[j][0]))
            pocmer += 1
            points[j][2] += 1
        points[j][1] = suma / points[j][2]

        return pocmer
            

    c = 0
    i = 0
    step = 1
    while i <= n:
        i += premeraj(c, m(step))
        dalsi = 1 if points[c][1] < 0 else -1

        sused = c + dalsi

        while dalsi * points[c][1] < 0:
            c += dalsi
            i += premeraj(c, m(step))

        x2, y2 = points[c][0], points[c][1]
        x1, y1 = points[c - dalsi][0], points[c - dalsi][1]
        
        if y2 - y1 == 0:
            x = (x2+x1)/2
        else:
            x = x1 * y2 / (y2-y1) + x2 * y1 / (y1-y2)


        while len(positions) < i:
            positions.append(x)

        c = max(c, c-dalsi)
        points.insert(c, [x, 0.0, 0])
        step += 1



    return positions


