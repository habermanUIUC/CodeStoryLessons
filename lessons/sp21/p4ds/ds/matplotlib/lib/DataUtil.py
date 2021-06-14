import random as r
import collections


# this is an example of using Python to build your
# own types.  Do not worry about the syntax.
# In the advanced class we will start to create our own
# data types to make data processing much easier and allow
# software to easily be shared

class Dice(object):

    def __init__(self, roll_count):

        r.seed(101)
        # generate some data
        # generate a sum of rolling two dice roll_count
        MAX_DIE = 6
        MIN_SUM = 2
        MAX_SUM = MAX_DIE * 2
        rolls = [r.randint(1, MAX_DIE) + r.randint(1, MAX_DIE) for i in range(0, roll_count)]

        labels = ["{}".format(i) for i in range(MIN_SUM, MAX_SUM + 1) if i in rolls]

        # loaded dice
        # loaded = [2 + r.randint(1,3) for i in range(0, roll_count)]

        roll_map = collections.Counter(rolls)

        # different views of the data
        self.in_order = sorted(roll_map.most_common(12),
                               key=lambda t: t[0])
        self.x = [d[0] for d in self.in_order]
        self.y = [d[1] for d in self.in_order]
        self.rolls = list(roll_map.elements())
        self.roll_map = roll_map

        # the following is an example of an algorithm
        # to use for cumulative sums that we could have
        # used numpy instead.

        # the following data is for the stacked area chart
        # rolled two dice 6 times:
        # roll:  1  2  3  4  5  6
        # what you rolled:
        #        2, 3, 2, 4, 3, 2

        # 2 map: [1, 1, 2, 2, 2, 3]
        # 3 map: [0, 1, 1, 1, 2, 2]
        # 4 map: [0, 0, 0, 1, 1, 1]
        #        ==================
        #         1  2  3  4  5  6  totals

        zeros = [0 for i in range(0, roll_count)]
        sums = [zeros.copy() for i in range(0, MAX_SUM + 1)]
        for i, roll in enumerate(rolls):
            sums[roll][i] = 1

        # now do a cumulative sum for each dice sum
        from itertools import accumulate
        for i, s in enumerate(sums):
            sums[i] = list(accumulate(s))

        # remove those that have all zeros
        final = []
        cnt = len(sums[0])
        for s in sums:
            if s[cnt - 1] > 0:
                final.append(s)

        sums = final
        # sums = sums[2:] # remove the first 2 (can't roll a 0 or 1)

        self.sums = sums
        self.sum_labels = labels


'''
x_max = 5
x_values = [ x + y/(x_max-1) for x in range(0,x_max) for y in range(0, x_max-1) ]
x_values.append(x_max)
'''