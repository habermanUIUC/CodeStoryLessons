#
# common code given to the students
# only edit the docker source, this gets copied into distribution
# all softlinks must be relative so autograder can see them
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


def read_10000():
  return read_data_file('10000.txt')


def get_uniq_set(t):
    return set(sorted(set([x.lower() for x in t])))


import AutoGrader as AG  # LessonUtil from reg_ex1
import re

class LessonDemo(AG.AutoGrader):

    def __init__(self):
        super().__init__('demo')
        self.huck = read_huck()

        s1 = self.run_pattern(r'[a-z]*[aeiou]{2}[a-z]*', self.huck, re.IGNORECASE, True)
        print('1', len(s1))

        s2 = self.run_pattern(r'[aeiou]{2}[a-z]*', self.huck, re.IGNORECASE, True)
        print('2', len(s2))

        s3 = self.run_pattern(r'\b[aeiou]{2}[a-z]*', self.huck, re.IGNORECASE, True)
        print('3', len(s3))

        s4 = self.run_pattern(r'\b_[aeiou]{2}.*_', self.huck, re.IGNORECASE, True)
        print('4', len(s4))

        s5 = self.run_pattern(r'\b[a-z]*[aeiou]{2}\b', self.huck, re.IGNORECASE, True)
        print('5', len(s5))

        # r'\b(she|he)\b'     2382 2
        # r'\s+(s?he)\s+'     2110 2 unique
        # s6 = self.run_pattern(r'\b(she|he)\b', self.huck,  re.IGNORECASE, False)
        # print('6', len(s6), len(get_uniq_set(s6)))


class HuckFinnAutoTester(AG.AutoGrader):

    def __init__(self):
        super().__init__('huck', read_huck())
        self.tests = [
            ('0', [65], {'uniq': True}),
            ('1', [18]),
            ('2', [994]),
            ('3', [3164]),
            ('4', [1094]),
        ]


class WordAutoTester(AG.AutoGrader):

    def __init__(self):
        super().__init__('10000', read_10000())
        self.tests = [
            ('0', [24]),
            ('1', [2]),  # check for \b
            ('2', [1443, 1426, 1425]),  # 1443 is wrong technically
            ('3', [7]),
            ('4', [1]),
        ]
