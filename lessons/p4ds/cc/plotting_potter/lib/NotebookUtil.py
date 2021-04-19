
import requests
import urllib.parse
import urllib.request
import os

def is_ipython(text):
    return text is not None and text.find('{"nbformat') == 0

def validate_notebook_id(notebook_id):
    import re
    regex = re.compile(r'/?[A-Za-z0-9_-]{20,}')
    ids = regex.findall(notebook_id)
    if len(ids) == 0:
        return None
    return ids[0].strip('/')

def install_gd_file(doc_id, filename=None):

    #
    # possible 403 if attempt is made too many times to download?
    # seems to be temporary -- don't fire off too many requests
    #
    baseurl = "https://docs.google.com/uc"
    baseurl = "https://drive.google.com/uc"

    #
    # can help by switching the baseurl
    #

    params = {"export": "download", "id": doc_id}
    url = baseurl + "?" + urllib.parse.urlencode(params)

    try:

        def v2():
            #r = requests.get(baseurl, params)
            r = requests.get(url)
            r.encoding = 'utf-8'
            if r.status_code != 200:
                print('bad request:', r.status_code)
                print('headers:', r.headers)
                print(r.status_code, "unable to download google doc with id:", doc_id)
                return None
            return r.text

        text = v2()
        if filename is not None and text is not None and len(text) > 0:
            with open(filename, 'w') as fd:
                fd.write(text)
        else:
            print("Unable to write file", filename, len(text))

        return text

    except Exception as e:
        print("unable to load notebook at", url, str(e))
        return None

def mount_notebook(doc_url, silent=True, idx=None):
    import CodeCleaners
    import Notebook
    import Extractor

    doc_id = validate_notebook_id(doc_url)
    text = install_gd_file(doc_id, 'nb.py')

    #text = open(name, 'r').read()

    cleaner = CodeCleaners.CodeCleaner()
    story = Notebook.StoryNotebook(text)

    code = cleaner.clean(story)
    filename = 'lesson.py'
    module = 'lesson'
    if idx is not None:
        filename = "lesson{:d}.py".format(idx)
        module = "lesson{:d}".format(idx)

    Extractor.create_module(code=code, file_out=filename, hide_imports=False)

    try:
        import importlib
        lesson = importlib.import_module(module)
        #import os
        #os.remove(filename)
        return True
    except Exception as e:
        print('Exception ', e)
        return False

