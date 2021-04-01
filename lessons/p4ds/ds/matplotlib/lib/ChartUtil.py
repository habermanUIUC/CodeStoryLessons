import matplotlib.pyplot as plt

"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def show():
  if matplotlib.get_backend() == 'agg':
    # replit
    plt.savefig(name_generator())
  else:
    #IPython
    plt.show()
  
def name_generator(preface='ex'):
  import os 
  count = 1
  while(True):
    name = "{}{}.png".format(preface, count)
    if os.path.isfile(name):
      count = count + 1
    else:
      print("file/tab is ", name)
      return name
"""


#
# simple charting library
#


def name_generator(preface='ex', unique=False):

    return "{}.png".format(preface)

    # needed for replit
    import os
    count = 1
    while (True):
        name = "{}{}.png".format(preface, count)
        if os.path.isfile(name):
            count = count + 1
        else:
            print("file is ", name)
            return name

def do_save(name):
    plt.savefig(name_generator(name))

def make_simple(x, y):
    fig, axes = plt.subplots()
    axes.axhline(y=2.0)
    axes.axvline(x=10.0)
    do_save('simple')
    return fig


def make_scatter(d):
    # since it's a collection of points
    # order does not matter
    x = d.keys()  # 2,3,4 .. 11, 12  (unordered)
    y = d.values()
    fig, axes = plt.subplots()
    axes.scatter(x, y)
    do_save('scatter')
    return fig


def make_lines(x, y):
    # need the x,y pairs in order
    fig, axes = plt.subplots()
    axes.plot(x, y)
    do_save('line')
    return fig


def make_bar(x, y):
    # need the x,y pairs in order
    fig, axes = plt.subplots()
    axes.bar(x, height=y)
    do_save('bar')
    return fig

    # VS axes.bar(x,y) ???
    # show barh(x,y)


def make_histogram(elements, centered=True):
    fig, axes = plt.subplots()
    low = min(elements)
    high = max(elements)
    bins = high - low + 1

    if centered:
        bins = [i - 0.5 for i in range(low, high + 2)]

    axes.hist(elements, density=True, bins=bins)
    do_save('histogram')
    return fig


def make_area(x, y):
    # need the x,y pairs in order
    fig, axes = plt.subplots()
    axes.fill_between(x, y)
    do_save('area')
    return fig

