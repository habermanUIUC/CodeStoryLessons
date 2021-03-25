#
# reg_ex1 AutoGrader
# soft link me
#
import os

def get_uniq_set(t):
    return set(sorted(set([x.lower() for x in t])))


import string
import re

class AutoGrader(object):

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.tests = []

    def run_pattern(self, pattern, flag=None, do_uniq=False, use_split=False):

        if flag is not None:
            regex = re.compile(pattern, flag)
        else:
            regex = re.compile(pattern)

        if use_split:
            result = regex.split(self.data)
        else:
            result = regex.findall(self.data)

        if do_uniq:
            result = set([x.lower() for x in result])

        return result

    def get_question(self, q_fn):
        q_name = q_fn.__name__
        numbers = re.findall(r'([0-9]+)', q_name)
        num = int(numbers[0])

    def _build_test(self, q_fn):
        q_name = q_fn.__name__
        numbers = re.findall(r'([0-9]+)', q_name)
        num = int(numbers[0])

        results = self.tests[num]
        options = {}
        if len(results) == 2:
            # test_name = results[0]
            result_set = results[1]
        else:
            # test_name = results[0]
            result_set = results[1]
            options    = results[2]

        return [q_name, q_fn, result_set, options]

    def _build_tests(self, q_set):
        tests = []
        for q_fn in q_set:
            test = self._build_test(q_fn)
            tests.append(test)
        return tests

    def test_question(self, q_fn, show_result_count=5, data=None):
        try:
            test = self._build_test(q_fn)
            label = test[0]
            r, w = self.run([test], show_result_count, data)
            if r == 1:
                return "{}: correct".format(label)
            else:
                return "{}: wrong".format(label)
        except Exception as e:
            return 'unable to test: ' + str(e)

    def test_all(self, q_set):
        tests = self._build_tests(q_set)
        return self.run(tests, show_result_count=0, data=self.data)

    def run(self, tests, show_result_count=5, data=None):

        if data is None:
            data = self.data

        pass_count = 0
        fail_count = 0
        for i, test in enumerate(tests):
            print("--" * 5)
            label, q_fn, answer_set, options = test

            use_split = options.get('use_split', False)
            do_uniq = options.get('uniq', False)

            regex = q_fn()
            if use_split:
                result = regex.split(data)
            else:
                result = regex.findall(data)

            if do_uniq:
                result = sorted(set([x.lower() for x in result]))

            if answer_set is None:
                pass
            else:
                if len(result) in answer_set:
                    print("Test {} PASS ({} found)".format(label, len(result)))
                    pass_count += 1
                else:
                    found = len(result)
                    print("Test {} FAIL".format(label), end=' ')
                    if len(answer_set) == 0:
                        print("(no answer key)")
                    else:
                        print("")
                    print("Test {} returned {} values (wanted {})".format(i, found, answer_set))
                    print("Test {} regex {}".format(label, regex))
                    fail_count += 1

            n = min(show_result_count, len(result))
            if n > 0:
                print("Top {} found:".format(n))
                for i in range(0, n):
                    r = result[i].replace('\n', '\\n').strip()
                    msg = r[0:30]
                    if len(r) > 30:
                        f = r[0:15]
                        l = r[-15:]
                        msg = "{} .. {}".format(f, l)
                    print(i, msg)

        if pass_count > 0 or fail_count > 0:
            print("\n{} correct; {} incorrect".format(pass_count, fail_count))

        return pass_count, fail_count


class SampleTester(AutoGrader):
    def __init__(self, test_fn, data, top=5):
        super().__init__('sample', data)
        self.test_question(test_fn, show_result_count=top, data=data)

