#
# common code given to the students
# only edit the source, this gets copied into distribution
#

import re
import sys
import os

'''
import importlib
importlib.reload(Util)
'''

'''
the following regular expression tokenize's the text: 
['A-Za-z0-9]+-?['A-Za-z0-9]+ 
Note that this regular expression will
skip single letter words (and numbers)
not match double hyphenated words (Aunt--Poly) (it will be two matches)
keep single hyphenated words (e.g. iron-will)
include the apostrophe in all of its possible uses. 
Make sure you understand why the given regular expression 
has those limitations.
how to treat: you-did-I-didn't
'''

def read_data_file(fn):
    fq = os.path.dirname(os.path.abspath(__file__))
    fq_path = "{:s}/../data/{:s}".format(fq, fn)
    with open (fq_path, 'r') as fd:
        return fd.read()


def clean_chapter(chapter):
    c = chapter.replace("\n", " ")
    pattern = r"[A-Za-z0-9']+-?[A-Za-z0-9']+"
    # pattern = r"[A-Za-z0-9']+"
    regex = re.compile(pattern)
    tokens = regex.findall(c)

    # remove leading and trailing single quotes
    t = [t.strip("'") for t in tokens]
    return " ".join(t).strip()


def clean_chapters(chapters):
    out = []
    for i, c in enumerate(chapters):
        c = clean_chapter(c)
        if len(c) > 0:
            out.append(c)
    return out


def split_into_chapters(data):
    pattern = r'^CHAPTER\s[A-Z\s]+\.?$'
    # pattern = r'CHAPTER\s[A-Z\s]+'
    regex = re.compile(pattern, re.M)
    return [d.strip() for d in regex.split(data) if len(d.strip()) > 0]
    #return regex.split(data)


'''
normalize the tokens
Then for each of the returned tokens (from using the regular expression)
strip off any leading and trailing apostrophes
keep the internal ones
do NOT change the case of the word
you will need to use the powerful string methods you learned in the bootcamp
'''

def split_into_tokens(data, normalize=True, min_length=0):
    tokens = data.split()
    if normalize:
        tokens = [t.lower() for t in tokens if len(t) > min_length]
    return tokens


def print_tfidf(tfidf, top_n=10):
    for d_idx, _tfidf in enumerate(tfidf):
        top_10 = _tfidf.most_common(top_n)
        print("Document: {}".format(d_idx+1))
        for word, score in top_10:
            print(" Word: {:14.12} TF-IDF: {:10.5f}".format( str(word), round(score, 5)))


def load_stopwords():
    return ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']