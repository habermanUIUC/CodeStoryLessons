import os
import re

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
    return "{:s}/{:s}".format(DATA_DIR, filename)


def read_data_file(filename):
    fn = path_for_data(filename)
    with open(fn, 'r') as fd:
        return fd.read()

'''
def read_data_file(fn):
    fq = os.path.dirname(os.path.abspath(__file__))
    fq_path = "{:s}/../data/{:s}".format(fq, fn)
    with open(fq_path, 'r') as fd:
        return fd.read()
'''
