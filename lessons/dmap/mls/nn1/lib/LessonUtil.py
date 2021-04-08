#
# common code given to the students
# only edit the docker source, this gets copied into distribution
#
import os
import pandas as pd


def ensure_path(p_dir="data"):
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


def xy_from_file(p, x, y, show=False):
    df = pd.read_csv(p)
    if show:
        df['XY'] = df[x] * df[y]
        print(df.head())
    x_values = df[x].values
    y_values = df[y].values
    return x_values, y_values


import numpy as np


class BooleanPerceptron(object):

    def __init__(self, weights, threshold, debug=False):
        # weights is an array of size 2 [w1, w2]
        # threshold is a scalar

        self.weights = np.array(weights)
        self.threshold = threshold
        self.debug = debug

    def predict(self, inputs):
        s = np.dot(self.weights, np.array(inputs))
        if self.debug:
            print(s, s-self.threshold)
        if s - self.threshold >= 0:
            return 1
        return 0

def build_and_gate():
    return BooleanPerceptron([1,1], 2)

# def build_or_gate():
#     return BooleanPerceptron([1,1], 1)

def build_not_gate():
    return BooleanPerceptron([-1], 0)


def general_GD(x, yv, iterations=10000, tolerance=1e-10, learning_rate=0.001):

    # add a column of 1's (see notes below)
    x = np.c_[x, np.ones(len(x))]
    y = np.r_[yv]

    cols = x.shape[1]
    w = np.zeros(cols)

    # print(x)
    # print(yv)
    # print(w)
    # print(x.dot(w))
    # print('y\n', y)
    # print('x.T\n',x.T)

    '''
    for y = mx + b
    y = w1 * x1 + w2 * x2 where x2 is always 1
    f(x1,x2,x3) = ∑ (y_i - (w2x2_i + w1x1_i + w0x0_i))^2
  
    if the last x, x0 is always 1, then 
    df/dw   = 2 * (y_i - (w2x2_i + w1x1_i + w0x0_i))( 0 - (0 + 0 + 1))
      d/w2  = -2 * x2 * x.dot(w)
      d/w1  = -2 * x1 * x.dot(w)
      d/w0  = -2 * x0 * x.dot(w)
    '''

    mse_est = 2 ** 32  # super high value
    n = len(x)
    for i in range(0, iterations):

        y_hat = x.dot(w)  # x.T.dot(w)
        err = y - y_hat
        mse = np.sum(err * err) / n

        # print(mse)
        if abs(mse_est - mse) < tolerance:
            break
        mse_est = mse

        dy_dw = -2 / n * (x.T * (y - y_hat))

        # print(dy_dw)
        dy_dw = np.sum(dy_dw, axis=1)
        w = w - (learning_rate * dy_dw)
        # print(w)

    print("mse {} after {} iterations".format(mse_est, i))
    return w


