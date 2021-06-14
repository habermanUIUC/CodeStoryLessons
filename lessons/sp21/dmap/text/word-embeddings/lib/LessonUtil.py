#
# common code given to the students
# only edit the source, this gets copied into distribution
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


def load_model(use_large=False):
    import spacy
    import os

    def load_medium_model():
        try:
            print('loading model, please wait')
            import en_core_web_md as model
        except ImportError:
            print('need to download .. please wait')
            cmd = "python -m spacy download en_core_web_md"  # 100MB
            os.system(cmd)
            import en_core_web_md as model
        return model

    def load_large_model():
        try:
            print('loading large model, please wait')
            import en_core_web_lg as model
        except ImportError:
            print('need to download .. please wait')
            cmd = "python -m spacy download en_core_web_lg"  # 830MB (zipped up) !!!! (1340241)
            os.system(cmd)
            import en_core_web_lg as model
        return model

    try:
        import IPython
    except ImportError:
        use_large = False

    if use_large:
        model = load_large_model()
    else:
        model = load_medium_model()

    return model.load()