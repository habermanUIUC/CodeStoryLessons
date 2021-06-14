#
# common code given to the students
# only edit the source, this gets copied into distribution
#
import random as r
import numpy as np
class RandomData(object):

    def __init__(self, n=50, cat_count=3):
        r.seed(101)
        np.random.seed(101)
        self.x = np.random.randn(n) # norm dist, mean 0; var: 1
        self.y = np.random.randn(n)
        self.c = np.random.choice(cat_count, n)
        self.n = np.array([x for x in range(0, n)])
        self.xy = np.array([self.x, self.y])

        # generate a 15x15 bivaraient
        #mean = (0,0)
        #cov = [[1,1],[0,0]]
        #x = np.random.multivariate_normal(mean,cov, (15,15))
        #print(x.size, x.shape)
        # not work x = x.reshape(15,15)
        #x = x[:, :, 0]

class RandomPetData(object):

    def __init__(self, n=50, cat_count=3):
        r.seed(101)
        np.random.seed(101)
        self.x = np.random.randn(n) # norm dist, mean 0; var: 1
        self.y = np.random.randn(n)
        self.pet = np.random.choice([  'dog', 'cat', 'fish', 'n/a'], size=n,
                                    p=[0.35, 0.25, 0.10, 0.30])
