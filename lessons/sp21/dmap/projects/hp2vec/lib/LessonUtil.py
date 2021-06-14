#
# common code given to the students
# only edit the source, this gets copied into distribution
#


import requests
import urllib.parse
import urllib.request
import os
import gensim

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


tests = [
    (['mcgonagall'],                [], ['professor'], ),          # 0  .
    (['ron'],                       [], ['hermione', 'harry'], ),  # 1  .
    (['seeker', 'quidditch'],       [], ['team'], ),               # 2  .
    (['harry', 'potter', 'school'], [], ['hogwarts'], ),           # 3  .
    (['gryffindor'],                [], ['hogwarts', 'house'], ),  # 4  .
    (['ron', 'hermione'],           [], ['harry'], ),              # 5  .
    (['ron', 'woman'],         ['man'], ['hermione'], ),           # 6  .
    (['hagrid'],                    [], ['dumbledore'], ),         # 7  .
    (['wizard'],                    [], ['witch'], ),              # 8  .
    (['weasley'],                   [], ['george', 'percy'], ),    # 9  .
    (['ravenclaw'],                 [], ['hufflepuff'], ),         # 10  .
    (['muggle', 'magic'],           [], ['wizard'], ),             # 11  .
    (['wizard'],     ['witch', 'dark'], ['potter'], ),             # 12  .
    (['house'],                     [], ['gryffindor'], ),         # 13  .
    (['house', 'evil'],             [], ['slytherin'], ),          # 14  .
    (['voldemort'], ['evil'], ['dumbledore'],),                    # 15
    (['slytherin', 'good'], ['student'], ['malfoy', 'lucius'],),   # 16
    (['mcgonagall', 'good'], ['witch'], ['dumbledore']),           # 17
    (['harry', 'aunt'], [], ['petunia']),                          # 18
    (['you-know-who'], [], ['voldemort'])                          # 19
]


'''
note evil occurs 15 times
misses
    (['hermione', 'woman'],   ['evil'], ['mcgonagall'], ),         # 19
    (['voldemort'], ['evil'], ['neville'],),                       # 14
    (['malfoy'], [], ['snape'],),                                  # 10
    (['voldemort'], [], ['you-know'],),                            # 11
    (['slytherin', 'student'], [], ['malfoy', 'lucius'],),         # 3

possible
    (['escaped', "frightened", "curse"], [], ['voldemort']),
'''

from collections import namedtuple
class Config(namedtuple('Config', ['doc', 'size', 'window', 'min_count', 'sg', 'negative', 'iter', 'name'])):

    def __str__(self):
        # skip doc
        fmt = "doc_len:{}, size:{}, window:{}, min_count:{}, sg:{}, negative:{}, iter:{}"
        return fmt.format(len(self.doc), self.size,
                          self.window, self.min_count,
                          self.sg, self.negative, self.iter)

def build_config(doc, size=10, window=5, min_count=5, sg=0, negative=3, iter=25, name=''):
  return Config(doc=doc, size=size, window=window, min_count=min_count, sg=sg, negative=negative, iter=iter, name=name)

def build_model(config):

    # export PYTHONHASHSEED=1
    model = gensim.models.Word2Vec(
        sentences=config.doc[0:3],   # each sentence is a HP book
        size=min(config.size, 300),  # how big the output vectors (spacy == 300)
        window=config.window,        # size of window around the target word
        min_count=config.min_count,  # ignore words that occur less than 2 times
        sg=config.sg,                # 0 == CBOW (default) 1 == skip gram

        negative=config.negative,

        # hs=1,
        # negative=0,
        # keep these the same
        workers=1,  # threads to use
        # sample=1e-3,
        iter=min(config.iter, 100),
    )
    # model.train(doc, total_examples=len(doc), epochs=100)
    return model

def _do_find(result, expected, debug=False):
    for idx, r in enumerate(result):
        name = r[0].lower()  # r[1] is the simularity score
        for who in expected:
            if name.find(who.lower()) >= 0:   # "potter's".find("potter") allow
                if debug:
                    print('FOUND {} at position {}'.format(who, idx))
                return idx
    if debug:
        print('NOT FOUND', expected)
    return None

def get_tests():
    return tests

MAX_DIM = 300
TOP_N = 25

def find_in_model(model, pos=[], neg=[], expected=[], topn=TOP_N, debug=False):
    try:
        result = model.wv.most_similar(positive=pos, negative=neg, topn=topn)
        idx = _do_find(result, expected, debug)
    except KeyError as e:
        print('Model missing', str(e))
        idx = None
    return idx

def score_model(model, debug=True, topn=TOP_N):
    total_found = 0
    for t_idx, t in enumerate(tests):
        idx = find_in_model(model, pos=t[0], neg=t[1], expected=t[2], topn=topn, debug=debug)
        if idx is not None:
            total_found += 1
    return total_found
