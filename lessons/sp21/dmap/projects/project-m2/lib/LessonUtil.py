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


def get_email_from_submission(meta_data_file):
    import json
    with open(meta_data_file, 'r') as fd:
        obj = json.load(fd)
        users = obj['users']
        first = users[0]
        email = first['email'].strip()
        return email

