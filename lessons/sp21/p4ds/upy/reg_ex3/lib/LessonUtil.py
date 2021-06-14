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

def read_huck():
  return read_data_file('huck.txt')


def read_story():
  return read_data_file('story.txt')


def get_uniq_set(t):
    return set(sorted(set([x.lower() for x in t])))


import AutoGrader as AG  # LessonUtil from reg_ex1
import re

class LessonAutoTester(AG.AutoGrader):
    def __init__(self):
        super().__init__('demo', read_story())
        self.tests = [
            ('0', [3]),
            ('1', [4], {'use_split': True}),
            ('2', [14]),
        ]

"""
        self.tests = [
            ('0', lesson.s_q0(),
             lesson.s_q0().findall(self.story),
             [3]),

            ('1', lesson.s_q1(),
             lesson.s_q1().split(self.story),
             [4]),

            ('2', lesson.s_q2(),
             lesson.s_q2().findall(self.story),
             [14]),
        ]
"""
