


import json

'''

The metadata of these notebooks get generated
The notebook should run on any platform that supports ipynb files

'''

class StoryNotebook(object):

    def __init__(self, ipynb):

        obj = json.loads(ipynb)

        content = obj.get('ipynb', None)
        if content is not None:
            obj = content

        meta = obj.get('metadata', {})
        colab = meta.get('colab', {})
        items = colab.get('provenance', [])

        story = meta.get('story', {})
        self.story = story
        self.tag   = story.get('tag', None)
        self.token = story.get('token', None)
        self.root  = story.get('root', None)
        self.name  = story.get('name', self.tag)

        # code, and user info change
        self.code_cells = []
        min_time, max_time, user = self._parse_code(obj, self.code_cells)
        self.user = user
        self.min_time = min_time
        self.max_time = max_time

    def get_raw_metadata(self):
        return self.story

    def __repr__(self):
        git = "r: {}:s lr: {:s} name: {:s} tag:{:s}".format(self.root, self.lesson_root, self.name, self.tag)
        return "tag: {:s} token:{:s} user:{:s}".format(git, self.token, self.user)

    def _parse_code(self, code, code_cells):

        min_time = 0
        user = None
        max_time = min_time
        for cell in code['cells']:

            if cell['cell_type'] == 'code':
                meta = cell.get('metadata', {})
                info = meta.get('executionInfo', {})

                ts = int(info.get('timestamp', 0))
                tz = int(info.get('user_tz', 0))  # minutes off UTC
                milli = 0  # (tz * 60) * 1000
                ts = (ts - milli) / 1000.0

                if ts != 0 and (ts < min_time or min_time == 0):
                    min_time = ts
                if ts > max_time:
                    max_time = ts
                    # print('new max', ts)

                user_info = info.get('user', None)
                if user is None and user_info is not None:
                    user = {'name': user_info['displayName'],
                            'id': user_info['userId']}

                code_cells.append(cell['source'])

        return min_time, max_time, user

    def _parse_markdown(self, code):

        text = []
        for cell in code['cells']:
            if cell['cell_type'] == 'markdown':
                for l in cell['source']:
                    line = l.strip()
                    if len(line) > 0:
                        text.append(line.strip())

        return "\n".join(text)


