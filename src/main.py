import numpy
import pprint
from scipy import misc
from PIL import Image

pp = pprint.PrettyPrinter(indent=4)

answer_images = []
images = {}

data = {
    'identity': {
        'image': None,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    },
    'mirror': {
        'image': None,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    },
    'flip': {
        'image': None,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    },
    'rot90': {
        'image': None,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    },
    'rot180': {
        'image': None,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    },
    'rot270': {
        'image': None,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    }
}

transformations = {
    'identity': lambda x: x,
    'mirror': numpy.fliplr,
    'flip': numpy.flipud,
    'rot90': lambda x: numpy.rot90(x, 1),
    'rot180': lambda x: numpy.rot90(x, 2),
    'rot270': lambda x: numpy.rot90(x, 3),
}


def reshape(array, x, y):
    array.reshape((x, -1))
    for i, val in enumerate(array):
        array[i].reshape((y, -1))
    return array


def complement(a, b):
    a = list(numpy.array(a).tolist())
    return len(a) * len(a[0]) - intersection(a, b)


def intersection(a, b):
    a = list(numpy.array(a).tolist())
    b = list(numpy.array(b).tolist())
    counter = 0
    for i, row in enumerate(a):
        for j, value in enumerate(row):
            if value == b[i][j]:
                counter += 1
    return counter


def similarity(a, b, alpha, beta):
    inter = intersection(a, b)
    return inter / (inter + alpha * complement(a, b) + beta * complement(b, a))


def similarity2(a, b):
    a = list(numpy.array(a).tolist())
    b = list(numpy.array(b).tolist())
    _union = len(b) * len(b[0]) + len(a) * len(a[0])
    _intersection = intersection(a, b)
    _union -= _intersection
    # print('union={} intersection={}'.format(union, intersection))
    return _intersection / _union


for x in range(1, 7):
    image_name = '{}.png'.format(x)
    path = '../res/2x1/1/{}'.format(image_name)
    img = misc.imread(path)
    answer_images.append(img)

for x in ['a', 'b', 'c', 8]:
    image_name = '{}.png'.format(x)
    path = '../res/2x1/1/{}'.format(image_name)
    img = misc.imread(path)
    images[x] = img

data['identity']['image'] = images['a']
data['mirror']['image'] = numpy.fliplr(images['a'])
data['flip']['image'] = numpy.flipud(images['a'])
data['rot90']['image'] = numpy.rot90(images['a'], 1)
# data['rot180']['image'] = numpy.rot90(images['a'], 2)
data['rot180']['image'] = transformations['rot180'](images['a'])
data['rot270']['image'] = transformations['rot270'](images['a'])


# rolled = numpy.roll(a_mirror, 60, axis=0)
# rolled = numpy.roll(rolled, 100, axis=1)
# misc.toimage(data['rot180']['image']).show()
# misc.toimage(a_mirror).show()
# misc.toimage(a_rot180).show()

# print(similarity(a_mirror, images['b']))list(numpy.array(a).tolist())
# print(len(a_mirror))
# pp.pprint(a_mirror.reshape((184, -1)).reshape((184, -1)))

# pp.pprint(reshape(a_mirror, 184, 184))

# print(similarity2(a_mirror, images['b']))

values = ['', '', 0]

for transform in data.keys():
    for i in range(5):  # range(len(data['identity']['image'])):
        for j in range(20):  # range(len(data['identity']['image'][i])):
            rolled = numpy.roll(data[transform]['image'], i, axis=0)
            rolled = numpy.roll(rolled, j, axis=1)
            sim = similarity2(rolled, images['b'])
            print('transform={}, i={}, j={}, sim={}'.format(transform, i, j, sim))
            if data[transform]['best_similarity'] < sim:
                data[transform]['best_similarity'] = sim
                data[transform]['i'] = i
                data[transform]['j'] = j
    image = numpy.roll(numpy.roll(data[transform]['image'], data[transform]['i'], axis=0), data[transform]['j'], axis=1)
    # misc.toimage(image).show()
    data[transform]['similarity']['a1b1'] = similarity(image, images['b'], 1, 1)
    data[transform]['similarity']['a1b0'] = similarity(image, images['b'], 1, 0)
    data[transform]['similarity']['a0b1'] = similarity(image, images['b'], 0, 1)

    if data[transform]['similarity']['a1b1'] > values[2]:
        values[0] = transform
        values[1] = 'a1b1'
        values[2] = data[transform]['similarity']['a1b1']
    elif data[transform]['similarity']['a1b0'] > values[2]:
        values[0] = transform
        values[1] = 'a1b0'
        values[2] = data[transform]['similarity']['a1b0']
    elif data[transform]['similarity']['a0b1'] > values[2]:
        values[0] = transform
        values[1] = 'a0b1'
        values[2] = data[transform]['similarity']['a0b1']

guess = numpy.roll(numpy.roll(transformations[values[0]](images['c']), data[values[0]]['i'], axis=0), data[values[0]]['j'], axis=1)
misc.toimage(guess).show()
answer_sim = []

for i, answer in enumerate(answer_images):
    sim = similarity2(guess, answer)
    answer_sim.append([i+1, sim])

max_sim = max(answer_sim, key=lambda item: answer_sim[1])
misc.toimage(answer_images[max_sim[0]-1]).show()

pp.pprint(data)

