import numpy
import pprint
from scipy import misc
import pyprind
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Process, Manager
import _thread
import threading


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


def img_complement(a, b):
    for i, row in enumerate(a):
        for j, value in enumerate(row):
            if not ((value[0] < 128 and value[1] < 128 and value[2] < 128) and (b[i][j][0] > 128 and b[i][j][1] > 128 and b[i][j][2] > 128)):
                value[0] = value[1] = value[2] = 255
    return a


def img_union(a, b):
    if b.any():
        for i, row in enumerate(a):
            for j, value in enumerate(row):
                if ((value[0] > 128 and value[1] > 128 and value[2] > 128) and (
                            b[i][j][0] < 128 and b[i][j][1] < 128 and b[i][j][2] < 128)):
                    value[0] = value[1] = value[2] = 0
    return a


def intersection(a, b):
    counter = 0
    for i, row in enumerate(a):
        for j, value in enumerate(row):
            if value[0] == b[i][j][0] and value[1] == b[i][j][1] and value[2] == b[i][j][2]:                    #  if value[0] == b.item(i, j, 0) and value[1] == b.item(i, j, 1):  # if numpy.array_equal(value, b[i][j]):
                counter += 1
    return counter


def similarity(a, b, alpha, beta):
    inter = intersection(a, b)
    return inter / (inter + alpha * complement(a, b) + beta * complement(b, a))


def similarity2(a, b):
    _union = len(b) * len(b[0]) + len(a) * len(a[0])
    _intersection = intersection(a, b)
    _union -= _intersection
    return _intersection / _union


def make_black_or_white(img):
    for i, row in enumerate(img):
        for j, value in enumerate(img):
            if img[i][j][0] < 128 and img[i][j][1] < 128 and img[i][j][2] < 128:
                img[i][j][0] = img[i][j][1] = img[i][j][2] = 0
            else:
                img[i][j][0] = img[i][j][1] = img[i][j][2] = 255
    return img

test_nr = 7
for x in range(1, 7):
    image_name = '{}.png'.format(x)
    path = '../res/2x1/{}/{}'.format(test_nr, image_name)
    img = misc.imread(path)
    img = make_black_or_white(img)
    answer_images.append(img)

for x in ['a', 'b', 'c']:
    image_name = '{}.png'.format(x)
    path = '../res/2x1/{}/{}'.format(test_nr, image_name)
    img = misc.imread(path)
    img = make_black_or_white(img)
    images[x] = img


values = ['', '', 0]

leng = len(images['a'])


def x(image, transforms, name):
    transform = {
        'image': image,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    }

    bar = pyprind.ProgBar(leng//1)
    for i in range(0, leng, 8):
        for j in range(0, leng, 8):
            rolled = numpy.roll(transform['image'], i, axis=0)
            rolled = numpy.roll(rolled, j, axis=1)
            sim = similarity2(rolled, images['b'])
            # print('transform={}, i={}, j={}, sim={}'.format(transform, i, j, sim))
            if transform['best_similarity'] < sim:
                transform['best_similarity'] = sim
                transform['i'] = i
                transform['j'] = j
        bar.update()
    image = numpy.roll(numpy.roll(transform['image'], transform['i'], axis=0), transform['j'], axis=1)
    # misc.toimage(image).show()
    transform['similarity']['a1b1'] = similarity(image, images['b'], 1, 1)
    transform['similarity']['a1b0'] = similarity(image, images['b'], 1, 0)
    transform['similarity']['a0b1'] = similarity(image, images['b'], 0, 1)
    transforms[name] = transform


if __name__ == '__main__':
    manager = Manager()
    datapro = manager.dict()
    datas = []
    jobs = []

    identity = images['a']
    mirror = transformations['mirror'](images['a'])  # numpy.fliplr(images['a'])
    flip = transformations['flip'](images['a'])  # numpy.flipud(images['a'])
    rot90 = transformations['rot90'](images['a'])  # numpy.rot90(images['a'], 1)
    rot180 = transformations['rot180'](images['a'])
    rot270 = transformations['rot270'](images['a'])

    p = Process(target=x, args=(identity, datapro, 'identity', ))
    p.daemon = True
    p.start()

    p1 = Process(target=x, args=(mirror, datapro, 'mirror', ))
    p1.daemon = False
    p1.start()

    p2 = Process(target=x, args=(rot90, datapro, 'rot90', ))
    p2.daemon = False
    p2.start()

    p3 = Process(target=x, args=(rot180, datapro, 'rot180', ))
    p3.daemon = False
    p3.start()

    p4 = Process(target=x, args=(rot270, datapro, 'rot270', ))
    p4.daemon = False
    p4.start()

    p5 = Process(target=x, args=(flip, datapro, 'flip', ))
    p5.daemon = False
    p5.start()

    p.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    for key in data.keys():
        data[key] = datapro[key]
        if data[key]['similarity']['a1b1'] > values[2]:
            values[0] = key
            values[1] = 'a1b1'
            values[2] = data[key]['similarity']['a1b1']
        if data[key]['similarity']['a1b0'] > values[2]:
            values[0] = key
            values[1] = 'a1b0'
            values[2] = data[key]['similarity']['a1b0']
        if data[key]['similarity']['a0b1'] > values[2]:
            values[0] = key
            values[1] = 'a0b1'
            values[2] = data[key]['similarity']['a0b1']
    pp.pprint(values)

    guess = numpy.roll(numpy.roll(transformations[values[0]](images['c']), data[values[0]]['i'], axis=0), data[values[0]]['j'], axis=1)
    # misc.toimage(guess).show()

    if values[1] == 'a1b0':
        _X = img_complement(images['b'], images['a'])
    elif values[1] == 'a0b1':
        _X = img_complement(images['a'], images['b'])
    else:
        _X = None

    # misc.toimage(_X).show()

    misc.toimage(img_union(guess, _X)).show()

    guess = img_union(guess, _X)

    answer_sim = []

    for i, answer in enumerate(answer_images):
        sim = similarity2(guess, answer)
        answer_sim.append([i+1, sim])
    pp.pprint(answer_sim)
    # max_sim = max(answer_sim, key=lambda item: answer_sim[1])
    max_sim_val = 0
    max_sim_nr = None
    for sim in answer_sim:
        if sim[1] > max_sim_val:
            max_sim_val = sim[1]
            max_sim_nr = sim[0]
    print('max_sim={}'.format(max_sim_nr))
    misc.toimage(answer_images[max_sim_nr-1]).show()

    # pp.pprint(data)



