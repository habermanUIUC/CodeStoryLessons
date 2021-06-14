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
def generate_dates(size):
    years = ['1946', '1950', '1970', '1960', '1955']
    months = [x for x in range(1, 13)]
    days = [x for x in range(1, 30)]
    dates = []
    y = np.random.choice(years, size)
    m = np.random.choice(months, size)
    d = np.random.choice(days, size)
    for i in range(0, size):
        dates.append('{:02d}/{:02d}/{}'.format(m[i], d[i], y[i]))
    return dates

import PandaTesters as PT
class RestaurantTester(PT.PandaTester):

    def __init__(self):
        super().__init__('data', path_for_data('data.csv'))

        self.answers = [
            ('0', 901.39, {}),
            ('1', 33,  {}),
            ('2', 407.98, {}),
            ('3', 5.14, {}),
            ('4', 2.40, {}),
            ('5', 33.0, {}),
            ('6', 35.12, {}),
            ('7', 10.0, {}),
            ('8', 4.0, {}),
            ('9', 434.98, {}),
            ('10', 170.93, {}),
            ]

