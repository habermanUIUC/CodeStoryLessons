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
# need this for finding characters
# as well as huck.txt
#
def load_stop_words():
    return ['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as',
            'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't",
            'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during',
            'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having',
            'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how',
            "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its',
            'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on',
            'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't",
            'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's",
            'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd",
            "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very',
            'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when',
            "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't",
            'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself',
            'yourselves']



import NotebookUtil as NB

def mount_notebook(url):
    return NB.mount_notebook(url)


if __name__ == "__main__":
    url ='https://drive.google.com/file/d/1hIgIEubGmRKNSJoaIFmxNHRTX2lB3Bec/view?usp=sharing'
    if mount_notebook(url):
        import re
        import collections

        import lesson

        text = "Hello Dr. Phil. How are you Mr. Roberts?"
        ans = lesson.find_characters_v3(text)
        print(ans)
    else:
        print('unable to mount notebook')
