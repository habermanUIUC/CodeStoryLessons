#
# common code given to the students
# only edit the docker source, this gets copied into distribution
#
import os


def ensure_path():
    fq = os.path.dirname(os.path.abspath(__file__))
    d_dir = "{:s}/../data".format(fq)
    if os.path.isdir(d_dir):
        return d_dir
    d_dir = "{:s}/data".format(fq)
    if os.path.isdir(d_dir):
        return d_dir

    print('unable to find data directory')
    return ''

DATA_DIR = ensure_path()


def path_for_data(filename):
    base = os.path.basename(filename)
    return "{:s}/{:s}".format(DATA_DIR, base)


def read_data_file(filename):
    fn = path_for_data(filename)
    with open(fn, 'r') as fd:
        return fd.read()

import numpy as np
class Point2D(object):

    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def to_array(self):
        return np.array([self.x, self.y])

    def __repr__(self):
        # self.x is now using the getter
        return "x:{:.2f}, y:{:.2f}".format(self.x, self.y)

class GeneralLine(object):
    def __init__(self, p1, p2):
        self.A = p2.y - p1.y
        self.B = -(p2.x - p1.x)
        self.C = p1.y * p2.x - p1.x * p2.y

        self.slope = (-self.A / self.B)
        self.y0 = (-self.C / self.B)

        self.p1 = p1
        self.p2 = p2

    def get_slope(self):
        return self.slope

    def get_y0(self):
        return self.y0

    def __repr__(self):
        # self.x is now using the getter
        # y = mx + b
        return "y = {:.2f}x + {:.2f}".format(self.slope, self.y0)



import pandas as pd
def xy_from_file(p, x, y, show=False):
  df = pd.read_csv(p)
  if show:
    df['XY'] = df[x] * df[y]
    print(df.head())
  x_values = df[x].values
  y_values = df[y].values
  return x_values, y_values