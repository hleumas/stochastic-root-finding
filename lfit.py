#!/usr/bin/python
import collections

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
        self._append(point[0], point[1], -point[2])
        return point

    def pop(self):
        point = self.points.pop()
        self._append(point[0], point[1], -point[2])
        return point

