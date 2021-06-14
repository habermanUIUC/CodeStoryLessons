import ast
import astunparse
import re
import inspect

'''
Finds module level (column 0) variables

THIS will ignore module level function calls
print('this is it')
ide.tester.test('bob')
sns.plotall(x)
print(do_result(1))


* If the RHS includes a function call, we mark it as 'dangerous'
  we don't want to make those calls at module load time

* Any other LHS that uses a marked variable, gets marked as well

    all good
    a,b = 1,2
    a,b = t
    a=b = 1

    # RHS marked as dangerous (don't want to do it at load time)
    # any use of the LHS variable, needs to be marked as well

    fig = plt.figure()  fig is marked as invalid (function call)
    a = fig.axes        a is marked as invalid as well
'''


# https://greentreesnakes.readthedocs.io/en/latest/nodes.html#top-level-nodes
class VariableHoist(object):

    # move all variables, if possible to module level
    # assumes all nodes passed in are at the module level (col_number == 0)
    def __init__(self):
        # confirmed set of
        self.dangerous = set()
        self.debug = False

    def resolve(self, nodes):

        nodes_ok    = []
        nodes_notok = []
        for node in nodes:
            if not isinstance(node, ast.Assign):
                nodes_notok.append(node)
                continue

            rhs = astunparse.unparse(node.value).strip()
            # in the RHS, get the first variable (if any)
            # a,b = 1,(2+3)
            # fig = plt.figure()           # capture plt
            # stop = nltk.download('stop') # capture nltk
            rhs_vars = re.findall(r'([a-zA-Z][a-z_A-Z0-9]*)', rhs)

            # NOTE not all will have type ast.Call
            # requests.get(                    is an Attribute
            # some_dict.get(                   is a Call
            # friends = install_data()[:(- 1)] is an Subscript

            # TITLE.get('key', None) # could be okay if TITLE is been defined
            # requests.get(URL) is not allowed
            is_call = rhs.find('(') > 0
            if self.debug:
                print("RHS", is_call, rhs_vars)

            danger = False
            if isinstance(node.value, ast.Call) or is_call:
                if self.debug:
                    print('node has call', rhs)
                danger = True
            elif isinstance(node.value, ast.Attribute):
                if self.debug:
                    print('node has attribute', rhs)
                danger = True
            else:
                if self.debug:
                    pass
                    # print('WHAT', type(node.value))

            # left hand side
            # a = b = fig  both a and b will be marked as dangerous
            for n in node.targets:
                lhs = astunparse.unparse(n).strip()
                lhs_vars = re.findall(r'([a-zA-Z][a-z_A-Z0-9]*)', lhs)
                lhs_var = lhs_vars[0]
                if self.debug:
                    print("LHS", lhs, lhs_var)

                if danger:
                    self.dangerous.add(lhs_var)  # lhs

                '''
                apple = some_call()   # lhs apple is not allowed
                pear = apple['bob']   # rhs is found in dangerous, not allowed as well
                valid = 'apple_sauce' # allowed but apple is in apple_sauce
                
                # also need to check LHS
                num9 = 100
                songs = install_date()  songs is dangerous
                songs['year'] = num9     RHS is fine, but LSH is songs is in dangerous
                '''

                if self.debug:
                    print('check if RHS', rhs_vars, 'reference', self.dangerous)

                valid = True
                for d in list(self.dangerous):
                    if d in rhs_vars or d in [lhs_var]:
                        valid = False
                        self.dangerous.add(lhs_var)
                        # print('ADDING', lhs_var)

                # print('danger', self.dangerous)
                if valid and not danger:
                    # print('PASSED', lhs, rhs)
                    # self.valid_lines.append(lhs + ' = ' + rhs)
                    nodes_ok.append(node)
                else:
                    # self.invalid_lines.append(lhs + ' = ' + rhs)
                    nodes_notok.append(node)
        return nodes_ok, nodes_notok

class ModuleLevelScope(ast.NodeVisitor):

    def __init__(self):
        self.imports = []
        self.classes = []
        self.functions = []
        self.rest = []

    def resolve(self, hide_imports=True):

        class_defs = astunparse.unparse(self.classes).strip()
        function_defs = astunparse.unparse(self.functions).strip()
        imports = astunparse.unparse(self.imports).strip()

        # resolve all assignment statements
        # hoist the ones you can
        varh = VariableHoist()
        ok, not_ok = varh.resolve(self.rest)
        global_ = astunparse.unparse(ok).strip()
        protect = astunparse.unparse(not_ok).strip()

        header_def = \
"""
def module_code_load():
    pass
"""
        if hide_imports:
            for p in imports.split('\n'):
                header_def += '    ' + p + '\n'

        for p in protect.split('\n'):
            header_def += '    ' + p + '\n'

        main_def = \
"""

if __name__ == "__main__": 
    module_code_load()
"""

        output = global_ + '\n'
        if not hide_imports:
            output += imports

        output += '\n' + class_defs
        output += '\n' + function_defs
        output += '\n' + header_def
        output += '\n' + main_def

        return output

    def visit(self, node):

        if hasattr(node, 'col_offset') and node.col_offset == 0:

            if isinstance(node, ast.FunctionDef):
                self.functions.append(node)
            elif isinstance(node, ast.ClassDef):
                self.classes.append(node)
            elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                self.imports.append(node)
            elif isinstance(node, ast.Pass):
                pass
            else:
                self.rest.append(node)

            # do NOT visit the subtree, we are done
        else:
            self.generic_visit(node)

    '''
    def generic_visit(self, node):
        if node.col_offset == 0:
            print("found", type(node))
    '''


class VariableExplorer(ast.NodeVisitor):

    def visit_Name(self, node):
        if node.col_offset == 0:
            print('V', node.id, node.col_offset)
            if isinstance(node.ctx, ast.Load):
                print('load')
            if isinstance(node.ctx, ast.Store):
                print('store')

        self.generic_visit(node)

    def visit_Constant(self, node):
        print('C', node.value, node.col_offset)
        self.generic_visit(node)

    def visit_Num(self, node):
        print('N', node.n, node.col_offset)
        self.generic_visit(node)

    def visit_Str(self, node):
        print('S', node.s, node.col_offset)
        self.generic_visit(node)

    def visit_FormattedValue(self, node):
        print('F', node.value, node.col_offset)
        self.generic_visit(node)

    def visit_JoinedStr(self, node):
        print('J', node.value, node.col_offset)
        self.generic_visit(node)


def create_module(file_in=None, code=None, file_out='/tmp/clean.py', hide_imports=True, global_imports=[]):

    if file_in is not None:
        with open(file_in, 'r') as fd:
            code = fd.read()

    tree = ast.parse(code)
    v_finder = ModuleLevelScope()
    v_finder.visit(tree)
    out = v_finder.resolve(hide_imports=hide_imports)

    with open(file_out, 'w') as fd:
        for w in global_imports:
            fd.write(w)
            fd.write('\n')
        fd.write(out)
