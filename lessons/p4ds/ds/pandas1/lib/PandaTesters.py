#
# common code given to the students
# only edit the docker source, this gets copied into distribution
#
import os

import pandas as pd
import numpy as np
import math
import re




class PandaTester(object):

    def __init__(self, name, path, answers=[]):
        # print(pd.__version__)

        # self.df = pd.read_csv(path, skiprows=1, delimiter=';')
        self.name = name
        self.df = pd.read_csv(path, delimiter=';')
        self.answers = answers

    def get_answers_only(self):
        return [t[1] for t in self.answers]

    def test_set(self, q_set, do_print=False):
        count = 0
        for q in q_set:
            count += self.test_question(q, return_pass_fail=True)
        return count

    def test_question(self, questionfn, return_pass_fail=False):

        df = self.df.copy()
        q_name = questionfn.__name__
        numbers = re.findall(r'([0-9]+)', q_name)
        num = int(numbers[0])

        tup = self.answers[num]
        name   = tup[0]
        answer = tup[1]
        result = questionfn(df)

        valid = math.fabs(answer - result) < 0.01
        if return_pass_fail:
            return valid

        if valid:
            msg = "{} Passed".format(q_name)
        else:
            msg = "{} Failed".format(q_name)
            msg += "\n{} vs {}".format(answer, result)
        return msg

        """
        correct = 0
        incorrect = 0
        for idx, q in enumerate(self.questions):
            result = q(df)
            print("Testing {}".format(idx))
            if math.fabs(answers[idx] - result) < 0.01:
                correct += 1
            else:
                print("wanted", answers[idx], 'vs', result)
                incorrect += 1
        print("Correct:", correct, "Wrong", incorrect)
        return correct
        """
