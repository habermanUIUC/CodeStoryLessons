#
# common code given to the students
# only edit the docker source, this gets copied into distribution
#
import os
import numpy as np

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


def read_data():
    names = ('U8', 'U50', 'U15', 'float', 'float', 'float')
    path = path_for_data('data.csv')
    data = np.genfromtxt(path,
                         delimiter=';',
                         names=True, dtype=names)
    return data


def read_data_v0():
    def datestr2num(s):
        s = s.decode('utf-8')
        # d = datetime.datetime.strptime(s, '%b %d %Y %I:%M%p')
        return s

    names = ('U8', 'U50', 'U15', 'float', 'float', 'float')
    data = np.genfromtxt('data.csv',
                         converters={'Date': datestr2num},
                         delimiter=';',
                         names=True, dtype=names)
    return data
