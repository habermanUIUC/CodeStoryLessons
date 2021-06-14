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


#
# the modules lesson
#
def add(a, b):
    counters[add] += 1
    return a + b

def div(a, b):
    counters[div] += 1
    return a / b

def get_count(fn):
    return counters[fn]

# using functions as keys in a dictionary!
counters = {add: 0, div: 0}
def clear():
    for k in counters.keys():
        counters[k] = 0
