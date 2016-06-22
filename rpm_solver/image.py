from scipy import misc
from string import ascii_lowercase
from numpy import array


class Image:

    def __init__(self, path):
        self.path = path
        self.data = misc.imread(path)
        self.image_to_black_or_white()

    def get_name(self):
        return self.path.split('/')[-1][0]

    def get_type(self):
        if self.get_name() in ascii_lowercase:
            return 'question'
        return 'answer'

    def image_to_black_or_white(self):
        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                v = list(array(value).tolist())
                color = v[0] + v[1] + v[2]
                if color < 720:
                    self.data[i][j][0] = self.data[i][j][1] = self.data[i][j][2] = 0
                else:
                    self.data[i][j][0] = self.data[i][j][1] = self.data[i][j][2] = 255
