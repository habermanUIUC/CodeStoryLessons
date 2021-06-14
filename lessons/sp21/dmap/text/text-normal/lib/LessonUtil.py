#
# common code given to the students
# only edit the source, this gets copied into distribution
#

#
# LessonUtil can be at the top level or inside of tests
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
    return "{:s}/{:s}".format(DATA_DIR, filename)

def read_data_file(filename):
    fn = "{:s}/{:s}".format(DATA_DIR, filename)
    with open(fn, 'r') as fd:
        return fd.read()


