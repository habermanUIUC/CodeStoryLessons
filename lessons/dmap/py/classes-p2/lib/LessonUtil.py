#
# common code given to the students
# only edit the docker source, this gets copied into distribution
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

def plot_lines(lines):
  import matplotlib.pyplot as plt
  from matplotlib.ticker import MaxNLocator

  fig,axes = plt.subplots()
  colors = ['orange', 'b', 'y', 'b', 'g']
  for idx, line in enumerate(lines):
    # print(line.p1.x, line.p1.y, line.p2.x, line.p2.y)
    x = [line.p1.x, line.p2.x]
    y = [line.p1.y, line.p2.y]
    axes.plot(x,y, color = colors[idx%len(colors)])
  axes.set_ylim(-1,20)
  axes.set_xlim(-1,20)
  axes.grid()
  axes.yaxis.set_major_locator(MaxNLocator(integer=True))
  axes.xaxis.set_major_locator(MaxNLocator(integer=True))
  return fig