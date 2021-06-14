#
# Cleaning Notebook Code
# should not have any dependencies .. can be used on the server side as well
#

import ast
import astunparse
import re


MAGIC = ['!', '%', '<']
MAGIC_MARKER = '%'
# print calls don't need to be run
scope0_print_regex   = re.compile(r'^print\s*\(')
scope0_fn_call_regex = re.compile(r'^([a-z_][.a-z0-9_]*)\s*\([^:]+$', re.IGNORECASE)
any_print_regex      = re.compile(r'^\s*print\s*\(')
INDENT_REGEX = re.compile(r'^(\s*)[^\s]')

def is_scope0_print(text):
    return scope0_print_regex.match(text)

def is_any_print(text):
    return any_print_regex.match(text)

def is_scope0_non_print(text):
    is_scope0 = scope0_fn_call_regex.match(text)
    is_print = scope0_print_regex.match(text)
    return is_scope0 and not is_print

def is_scope0_call(text):
    return scope0_fn_call_regex.match(text)


def comment_out(line):

    # note, we append 'pass' to the line to keep it in the source code
    # if you just commented it out, it could be removed or lead to invalid python

    # if something:
    #    print('made it')
    # if something:
    #    pass #print('made it')

    # respects the current indentation level
    clean = line.rstrip()
    m = INDENT_REGEX.match(clean)
    # print('found space', m.start(1), m.end(1))
    total = m.end(1) - m.start(1)
    new_line = " " * total + 'pass #' + line.lstrip()
    return new_line


def single_line_matches(line, options):
    if len(options) > 0:
        clean = line.rstrip()
        for fn in options:
            if fn(clean):
                #print('found pattern:', clean + ':')
                return True
    return False


def magic_block(line):
    # %%html
    clean = line.lstrip()
    return len(clean) > 0 and clean[0] == MAGIC_MARKER


def magic_line(line):

    clean = line.lstrip()
    return len(clean) > 0 and clean[0] in ['!', '%', '<']


def has_ipython_import(line):

    bad_news = ['from notebook', 'import notebook',
                'from google',   'import google',
                'from IPython',  'import IPython']
    clean = line.lstrip()
    remove_me = False
    for b in bad_news:
        if clean.find(b) >= 0:
            remove_me = True
            break

    return remove_me


class FunctionReplacer(ast.NodeTransformer):
    def __init__(self, function_name, new_node):
        self.node = new_node
        self.function_name = function_name

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.function_name:
            return self.node
        return node


class FunctionFinder(ast.NodeVisitor):
    def __init__(self, name):
        self.node = None
        self.function_name = name

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.name == self.function_name:
            self.node = node

        # this call is not needed, since we are done visiting
        # self.generic_visit(node)


class IDECodeReplacer(object):

    def __init__(self):

        self.node = None
        self.replace_org =\
'''
def install_ide(*args):
    class Nop(object):
        def __init__(self, e): self.e = e
        def nop(self, *args, **kw): return ("unable to test:" + self.e, None)
        def __getattr__(self, _): return self.nop
    class IDE():
        tester = Nop("")
        reader = Nop("")
        def __getattr__(self, _):
            return Nop("")
    return IDE()
'''

        self.replace =\
'''
def install_ide(*args):
    from unittest.mock import Mock
    class MyMock(Mock):
        def __repr__(self):
            return ''
    return MyMock()
'''
        self.function_name = 'install_ide'
        tree = ast.parse(self.replace)
        finder = FunctionFinder(self.function_name)
        finder.visit(tree)
        self.node = finder.node

    def replace_function(self, code):

        if self.node is None:
            print('unable to transform')
            return code

        tree = ast.parse(code)
        cleaner = FunctionReplacer(self.function_name, self.node)
        clean = cleaner.visit(tree)
        return astunparse.unparse(clean)


#
# prepares code to be run in the sandbox (server side)
#
from enum import Enum

class Level(Enum):

    RAW = 0
    REMOVE_MAGIC = 1
    REPLACE_IDE  = 2

    # these are policies
    AS_IS      = 2
    IPY_REMOVE = 5
    SCOPE0_NON_PRINT = 10  # any scope0 call (besides print)
    SCOPE0_CALL = 20       # any scope0 call
    ANY_PRINT = 30         # any print
    DEFAULT = 50

    @staticmethod
    def get_strategies(level):

        if level.value <= Level.IPY_REMOVE.value:
            return []

        basic = [has_ipython_import, is_any_print, is_scope0_call]
        if level == Level.DEFAULT:
            return basic

        if level == Level.SCOPE0_CALL:
            return [has_ipython_import, is_scope0_call]

        if level == Level.SCOPE0_NON_PRINT:
            return [has_ipython_import, is_scope0_non_print]

        print('unknown parsing strategy', level)
        return basic

    @staticmethod
    def get_level(v_str):
        if v_str is None:
            return Level.DEFAULT

        if isinstance(v_str, dict):
            keys = list(v_str.keys())
            if len(keys) == 0:
                return Level.DEFAULT
            if len(keys) > 1:
                print("invalid parse keys", v_str)
                return Level.DEFAULT
            k = keys[0]
            v_str = k

        # map from user defined values
        # to parsing strategies
        if v_str == 'raw':
            return Level.RAW
        if v_str == 'as_is':
            return Level.AS_IS
        if v_str == 'keep_scope0_print':
            return Level.SCOPE0_NON_PRINT
        if v_str == 'keep_scope1_print':
            return Level.SCOPE0_CALL

        print('unknown parse level', v_str)
        return Level.DEFAULT

class CodeCleaner(object):

    def clean(self, story_nb, options=None):

        level = Level.get_level(options)

        # print(options)
        #print('Level', level)

        if level == Level.RAW:
            code = ''
            for cell in story_nb.code_cells:
                for s in cell:
                    code += s.rstrip() + '\n'
            # return '\n'.join(story_nb.code_cells).strip()
            return code

        # Two pass through code
        # pass 1
        # process at the cell block level
        #    remove whole cells based on if they are magic or not
        #    or if everything in that cell is illegal
        #
        # pass 2
        # process line level
        #     a full AST parse, replace the IDE,
        #     comment out print statements
        #
        lines = []
        remove_cell_if_all_magic = True
        for cell in story_nb.code_cells:
            code = '\n'.join(cell).strip()
            if len(code) == 0 or magic_block(code):
                continue

            cell_code = []
            invalid_count = 0
            for line in cell:
                if magic_line(line):
                    invalid_count += 1
                    line = comment_out(line)
                else:
                    # line is fine
                    pass

                # line could be empty
                cell_code.append(line.rstrip())

            if remove_cell_if_all_magic:
                if len(cell_code) == invalid_count:
                    cell_code = []

            lines.extend(cell_code)

        code = '\n'.join(lines).strip()

        # pass 2
        # replace IDE,
        # remove module level function calls
        # remove print calls
        # comment out invalid notebook imports (code will most likely fail)
        # this does a full ast parse, unparse SO
        # any code that is commented out will be removed
        # you could avoid this by pre-processing
        # if line = ^# ... --> ^pass # <previous line>
        cleaner = IDECodeReplacer()
        code = cleaner.replace_function(code)
        if level == Level.REPLACE_IDE or level == Level.AS_IS:
            return code

        # full magic cells have been removed
        # but not any specific ! do_some_command line
        do_match = Level.get_strategies(level)
        lines = code.split("\n")
        clean = []
        for line in lines:
            if single_line_matches(line, do_match):
                line = comment_out(line)
            clean.append(line)
        return '\n'.join(clean)

