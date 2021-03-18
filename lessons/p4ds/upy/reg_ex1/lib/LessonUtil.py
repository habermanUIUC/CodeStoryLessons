#
# reg_ex1 LessonUtil
# soft link doesn't work for asset copy
#
import os

import AutoGrader as AG

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

def get_uniq_set(t):
    return set(sorted(set([x.lower() for x in t])))


import string
import re


def read_huck():
    return read_data_file('huck.txt')

sample0 = "He pulled the lever all the way down to where it said full steam ahead. A bell rang. The motors made a grinding sound and the ferry began to move. The passengers were surprised because the captain was still on deck taling to the Man in the Yellow Hat. Who was running the boat? It was George!!!\nI had 20 dollars and george, $25.00!!! Even CHAPTERS can help us"

sample1 = '''
Miss Watson would say,"Don't put your feet up there, Huckleberry;" and "Don't scrunch up like that, Huckleberry--set up straight;" and pretty soon she would say, "Don't gap and stretch like that, Huckleberry--why don't you try to behave?"  Then she told me all about the bad place,
'''

sample2 = 'Apples--app_les! I love apples'
sample3 = "Richmond............... Mr. Kean."


# used to help develop the lesson
class HuckFinnDemo(AG.AutoGrader):

    def __init__(self):
        super().__init__('huck', read_huck())

        r1 = self.run_pattern(r'[A-Za-z]+', None, False)
        print('1', len(r1))

        # 5983
        r2 = self.run_pattern(r'[A-Za-z]+', None, True)
        print('2', len(r2))

        # 5991
        r3 = self.run_pattern(r'[0-9A-Za-z]+', None, True)
        print('3', len(r3), r3 - r2)

        # 6326
        r6 = self.run_pattern(r"['0-9A-Za-z]+", None, True)
        print('6', len(r6))

        # words with hyphens are good
        p1 = r"['0-9A-Za-z]+-?['0-9A-Za-z]+"

        r7 = self.run_pattern(p1, None, True)
        print('7', len(r7))

        p2 = r"['\da-z]+-?['\da-z]+"
        r7b = self.run_pattern(p2, re.IGNORECASE, True)
        print('7b', len(r7b))

        # italized
        p2 = r"_['A-Za-z0-9]+_"
        r8 = self.run_pattern(p2, None, True)
        print('8', len(r8))


class HuckFinnAutoTester(AG.AutoGrader):

    def __init__(self):
        super().__init__('huck', read_huck())
        self.tests = [
            ('0', [5960]),
            ('1', [3]),
            ('2', [8]),
            ('3', [1]),
            ('4', [763]),
            ('5', [74]),
            ('6', [7]),
            ('7', [34]),
            ('8', [103]),
            ('9', [2110]),
            ('10',[43]),

            # uncomment if want to test extra credit
            ('11', [2]),
            ('12', [19]),
            ('13', [2]),
        ]

# clean and split example
# util.old_school(util.read_huck())
# demo = util.HuckFinnDemo()
class old_school(object):

    def __init__(self, text):
        # before split, pre_clean it to remove -- etc,
        t1_clean = self.pre_clean(text)
        t1 = t1_clean.split()

        print("total", len(t1), "uniq", len(set(t1)))
        t1_lower = [x.lower() for x in t1]
        print("after lower")
        print("uniq", len(set(t1_lower)))

    def pre_clean(self, t):
        black = string.punctuation
        black = black.replace('\'', "")  # keep single quote
        for r in black:
            t = t.replace(r, ' ')
        return t

