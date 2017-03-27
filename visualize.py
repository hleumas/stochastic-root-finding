#!/usr/bin/python
#from search import testSet
import Gnuplot
import cPickle
import math
import sys

g = Gnuplot.Gnuplot()

def stdev(data, step=0, func=0):
    return math.sqrt(sum(x**2 for x in data) / len(data))

def devAll(data, method=stdev, params=[]):
    prec  = data['prec']
    steps = data['steps']
    result = [
        [
            [
                method([m[step] for m in func], step, i, *params)
                for step in xrange(steps)
            ]
            for (i, func) in enumerate(alg)
        ]
        for alg in data['result']
    ]
    return {
            'algs'  : data['algs'],
            'funcs' : data['funcs'],
            'prec'  : prec,
            'steps' : steps,
            'result': result,
           }

def confinter(data, step, func, percentil):
    zahod = int((1.0-percentil) * len(data) / 2)
    kern = sorted(data)[zahod:len(data)-zahod]
    return kern[-1] - kern[0]

def checkCost(d, f):
    a, b = max(-1.0, f(-0.5*d)), min(1.0, f(0.5*d))
    if a**2 == 0.0 or b**2 == 0.0:
        return float('inf')
    return 1.0 + (1 - a**2) / a**2 + (1-b**2) / b**2

def checkVsReal(data, step, func, percentil):
    inter = confinter(data, step, func, percentil)
    return float(step) / checkCost(inter, testSet[func])



def basicPlot(data, algs=None, funcs=None, save=None):
    result = data['result']
    if algs is None:
        algs = range(data['algs'])
    if funcs is None:
        funcs = range(data['funcs'])

    for i in funcs:
        grafdata = []
        for j in algs:
            grafdata.append(Gnuplot.Data(range(0, data['steps']), result[j][i]))
            print result[j][i][1000]
            apply(g.plot, grafdata)
        raw_input("Press Enter to continue")
        if save is not None:
            g.hardcopy(save + str(i), terminal='png')


def averageData(data):
    average = []
    for alg in data['result']:
        sum = [0.0 for i in xrange(data['steps'])]
        for func in alg:
            for k in xrange(data['steps']):
                sum[k] += func[k] / data['funcs']
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

def devplot(data, percentil, alg, func, step):
    res = [data['result'][alg][func][m][step] for m in xrange(data['prec'])]
    print gauss(res, 1-percentil)
    h = hist(res, 1-percentil)
    print '\n'.join(map(' '.join, zip(map(str, h[0]), map(str, h[1]))))
    #grafdata = [Gnuplot.Data(*hist(res, 1-percentil))]
    #grafdata.append(gauss(res, 1-percentil))
    #apply(g.plot, grafdata)
    #raw_input("Press Enter to continue")

def hist(data, p):
    zahod = int(p * len(data) / 2)
    if zahod != 0:
        kern = sorted(data)[zahod:-zahod]
    else:
        kern = sorted(data)
    pocint = int(math.sqrt(len(kern)))
    pocdat = len(kern) / pocint
    length = (kern[-1] - kern[0]) / pocint
    kern.append(float('inf'))
    j = 0
    xval, histogram = [], []
    for i in xrange(0, pocint):
        f, l = i * pocdat, (i+1) * pocdat
        av = sum(kern[f:l])  / pocdat
        xval.append(av)
        histogram.append(pocdat / (kern[l-1] - kern[f]) / len(kern))

    return (xval, histogram)

def gauss(data, p):
    zahod = int(p * len(data) / 2)
    #zahod = 10
    kern = sorted(data)[zahod:-zahod]
    dev = stdev(kern)
    amp = math.sqrt(0.5/math.pi) / dev
    #return Gnuplot.Func(str(amp) + '*exp(-' + str(1.0/(2*dev**2)) + '*x**2)')
    return dev

def sigmoid(x, a, b):
    if a * x > 500.0:
        return 1.0
    if a * x < -500.0:
        return 0.0
    return 1.0/(1.0+math.exp(-a*(x-b)))

    
testSet = [
    #lambda x: linear(x, 1.0, 0),
    #lambda x: x**3,
    lambda x: 2 * sigmoid(x, 1.0, 0.0) - 1.0,
    #lambda x: 2 * erf(x, 1.0, 0) - 1.0,
    #lambda x: 2 * cauchy(x, 1.0, 0) - 1.0,
    #lambda x: sgn(x),
]
    

f = open(sys.argv[1], 'rb')
data = cPickle.load(f)
#print data[1]
#devplot(data[0], float(sys.argv[2]), 0, 0, 100)
#g('set log xy')
#basicPlot(devAll(data[0], confinter, [float(sys.argv[2])]), None, None,
        #sys.argv[3])
x = devAll(data[0], confinter, [float(sys.argv[2])])
r = x['result']
for j in xrange(x['funcs']):
    f = open(sys.argv[j + 3], 'wt')
    plot = [i[j] for i in r]

    tostr = lambda x: map(str, x)
    bodky = map(' '.join,map(tostr, zip(*plot)))
    i = 1.0
    while i < len(bodky):
        print >> f, str(int(i)) + ' ' + bodky[int(i)]
        i *= 1.3

    f.close()
