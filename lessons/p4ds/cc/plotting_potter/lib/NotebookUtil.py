import requests
import urllib
import json

#
# no need to change anything in this module
#

def read_remote(url):
    with requests.get(url) as response:
        response.encoding = 'utf-8'
        if response.status_code == requests.codes.ok:
            # that is 200
            return response.text
        else:
            print('invalid read', response.status_code, url)
    return None

#
# replit does NOT allow editing of files
# that are created at runtime
#
C_URL = 'https://raw.githubusercontent.com/habermanUIUC/DMAPTester/master/src/tf/notebook/SourceCleaner.py'
P_URL = 'https://raw.githubusercontent.com/habermanUIUC/DMAPTester/master/src/tf/notebook/Parser.py'

def mount_notebook(d_id, name='notebook.py', force=False):

    import os

    if os.path.exists(name) and not force:
        print(name, "already mounted")
        return True

    try:
        import Parser
        import SourceCleaner
    except ImportError as e:
        prep_remote('SourceCleaner.py', C_URL)
        prep_remote('Parser.py', P_URL)

    import Parser
    import SourceCleaner

    url = build_google_drive_url(d_id)
    code = read_remote(url)

    try:
        py_code = Parser.NBParser().parse_code(code)
        with open(name, 'w') as fd:
            fd.write(py_code[0])

        code = SourceCleaner.CodeCleaner().clean(py_code[0])
        with open(name, 'w') as fd:
            fd.write(code)

        # os.remove('SourceCleaner.py')
        # os.remove('Parser.py')
        return True

    except json.decoder.JSONDecodeError as e:
        print("notebook is not readable", str(e))
        return False
    except Exception as e:
        print("notebook is not cleaned", str(e))
        return False

def prep_remote(fn, url):
    code = read_remote(url)
    with open(fn, 'w') as fd:
        fd.write(code)

def build_google_drive_url(doc_id):
    URL_1 = "https://drive.google.com/uc"
    URL_2 = "https://docs.google.com/uc"

    baseurl = URL_1
    params = {"export": "download",
              "id": doc_id}
    url = baseurl + "?" + urllib.parse.urlencode(params)
    return url

