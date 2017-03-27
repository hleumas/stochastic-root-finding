#!/usr/bin/python
#
# Josh Lifton 2004
#
# Permission is hereby granted to use and abuse this document
# so long as proper attribution is given.
#
# This Python script demonstrates how to use the numarray package
# to generate and handle large arrays of data and how to use the
# matplotlib package to generate plots from the data and then save
# those plots as images.  These images are then stitched together
# by Mencoder to create a movie of the plotted data.  This script
# is for demonstration purposes only and is not intended to be
# for general use.  In particular, you will likely need to modify
# the script to suit your own needs.
#

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt   # For plotting graphs.
import numpy as np
import subprocess                 # For issuing commands to the OS.
import os
import sys                        # For determining the Python version.

#
# Print the version information for the machine, OS,
# Python interpreter, and matplotlib.  The version of
# Mencoder is printed when it is called.
#
print 'Executing on', os.uname()
print 'Python version', sys.version
print 'matplotlib version', matplotlib.__version__

not_found_msg = """
The mencoder command was not found;
mencoder is used by this script to make an avi file from a set of pngs.
It is typically not installed by default on linux distros because of
legal restrictions, but it is widely available.
"""

try:
    subprocess.check_call(['mencoder'])
except subprocess.CalledProcessError:
    print "mencoder command was found"
    pass # mencoder is found, but returns non-zero exit as expected
    # This is a quick and dirty check; it leaves some spurious output
    # for the user to puzzle over.
except OSError:
    print not_found_msg
    sys.exit("quitting\n")


#
# First, let's create some data to work with.  In this example
# we'll use a normalized Gaussian waveform whose mean and
# standard deviation both increase linearly with time.  Such a
# waveform can be thought of as a propagating system that loses
# coherence over time, as might happen to the probability
# distribution of a clock subjected to independent, identically
# distributed Gaussian noise at each time step.
#

print 'Initializing data set...'   # Let the user know what's happening.

# Initialize variables needed to create and store the example data set.
xbound = [-3, 3]
xsample = 1000
fileid = 0
mean = -6                 # Initial mean of the Gaussian.
numberOfTimeSteps = 10
stddev = 0.2              # Initial standard deviation.
meaninc = 0.1             # Mean increment.
stddevinc = 0.1           # Standard deviation increment.
points = []
ybound = [-1,1]
# Create an array of zeros and fill it with the example data.

#
# Now that we have an example data set (x,y) to work with, we can
# start graphing it and saving the images.
#

def labels():
    global plt
    plt.xlabel('time (ms)')
    plt.ylabel('probability density function')
    plt.title(r'$\cal{N}(\mu, \sigma^2)$', fontsize=20)

def draw(count=1):
    global xbound, ybound, plt, points
    x = np.arange(xbound[0], xbound[1], float(xbound[1]-xbound[0])/xsample)
    plt.axis((x[0],x[-1],ybound[0],ybound[1]))
    plt.plot(x, fn2(x), '-', linewidth=3)

    for i in points:
        plt.plot(*i)

    for i in xrange(count):
        save()
    plt.clf()



def save():
    global fileid, plt
    filename = str('%03d' % fileid) + '.png'
    plt.savefig(filename, dpi=100)
    fileid += 1
    print 'Writing file ' + filename

def fn(x):
    return x-np.sin(x) 
def fn2(x):
    a = []
    for i in x:
        if i < -np.pi / 2:
            a.append(0)
        elif i > np.pi /2:
            a.append(1)
        else:
            a.append(np.sin(i)/2 + 0.5)
            
    return np.array(a)

def getybound(xbound):
    ybound = [min(fn2(xbound)), max(fn2(xbound))]
    margin = float(ybound[1] - ybound[0]) * 0.1
    return [ybound[0] - margin, ybound[1] + margin]

ybound = getybound(xbound)

def blik(point):
    point[2] = 'ro'
    draw(3)
    point[2] = 'go'
    draw(3)

def zoom(newxbound, steps):
    global xbound, ybound
    stepx = [float(newxbound[i] - xbound[i])/steps for i in range(2)]
    for i in xrange(steps):
        xbound = [xbound[i] + stepx[i] for i in range(2)]
        ybound = getybound(xbound)
        draw()



scale = 0.8
xb, xe = [xbound[i] * scale for i in xrange(2)]
#points.append([xb, fn(xb), 'go'])
#points.append([xe, fn(xe), 'go'])
def bisection(points, steps):
    if steps < 0:
        return
    c = float(points[0][0] + points[1][0]) / 2.0
    points.insert(1, [c, fn(c), 'go'])
    blik(points[1])
    blik(points[1])
    print fn(c)
    if fn(c) < 0:
        points.pop(0)
    else:
        points.pop(2)
    draw(4)
    margin = float(points[1][0] - points[0][0]) / scale / 2
    zoom([points[0][0] - margin, points[1][0] + margin], 10)
    draw(4)
    bisection(points, steps-1)


#bisection(points, 5)
zoom([-0.05, 0.05], 100)
zoom([-100, 100], 200)
#
# Now that we have graphed images of the dataset, we will stitch them
# together using Mencoder to create a movie.  Each image will become
# a single frame in the movie.
#
# We want to use Python to make what would normally be a command line
# call to Mencoder.  Specifically, the command line call we want to
# emulate is (without the initial '#'):
# mencoder mf://*.png -mf type=png:w=800:h=600:fps=25 -ovc lavc -lavcopts vcodec=mpeg4 -oac copy -o output.avi
# See the MPlayer and Mencoder documentation for details.
#

command = ('mencoder',
           'mf://*.png',
           '-mf',
           'type=png:w=800:h=600:fps=10',
           '-ovc',
           'lavc',
           '-lavcopts',
           'vcodec=mpeg4',
           '-oac',
           'copy',
           '-o',
           'output.avi')

#os.spawnvp(os.P_WAIT, 'mencoder', command)

print "\n\nabout to execute:\n%s\n\n" % ' '.join(command)
subprocess.check_call(command)

print "\n\n The movie was written to 'output.avi'"

print "\n\n You may want to delete *.png now.\n\n"


