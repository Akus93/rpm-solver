import numpy
import pprint
from scipy import misc
import pyprind
from multiprocessing.pool import ThreadPool as Pool
from multiprocessing import Process, Manager


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
        b = list(numpy.array(b).tolist())
        b = img_grey(b)
        for i, row in enumerate(a):
            for j, value in enumerate(row):
                if b[i][j][0] < 128 and b[i][j][1] < 128 and b[i][j][2] < 128:
                    value[0] = value[1] = value[2] = 0
    return a


def img_grey(a):
    for i, row in enumerate(a):
        for j, value in enumerate(row):
            if j % 2 and i % 2:
                value[0] = value[1] = value[2] = 255
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
            if img[i][j][0] < 230 and img[i][j][1] < 230 and img[i][j][2] < 230:
                img[i][j][0] = img[i][j][1] = img[i][j][2] = 0
            else:
                img[i][j][0] = img[i][j][1] = img[i][j][2] = 255
    return img


test_nr = 1
for x in range(1, 7):
    image_name = '{}.png'.format(x)
    path = 'res/2x1/{}/{}'.format(test_nr, image_name)
    img = misc.imread(path)
    img = make_black_or_white(img)
    answer_images.append(img)

for x in ['a', 'b', 'c']:
    image_name = '{}.png'.format(x)
    path = 'res/2x1/{}/{}'.format(test_nr, image_name)
    img = misc.imread(path)
    img = make_black_or_white(img)
    images[x] = img


values = ['', '', 0, '']

leng = len(images['a'])


def transformation(image, transforms, name):
    step = 25
    transform = {
        'image': image,
        'i': None,
        'j': None,
        'best_similarity': 0,
        'similarity_b': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        },
        'similarity_c': {
            'a1b1': None,
            'a1b0': None,
            'a0b1': None,
        }
    }

    for i in range(0, leng, step):
        for j in range(0, leng, step):
            rolled = numpy.roll(transform['image'], i, axis=0)
            rolled = numpy.roll(rolled, j, axis=1)
            sim_b = similarity2(rolled, images['b'])
            sim_c = similarity2(rolled, images['c'])
            # print('transform={}, i={}, j={}, sim_b={}'.format(transform, i, j, sim_b))
            if transform['best_similarity'] < sim_b:
                transform['best_similarity'] = sim_b
                transform['i'] = i
                transform['j'] = j
            if transform['best_similarity'] < sim_c:
                transform['best_similarity'] = sim_c
                transform['i'] = i
                transform['j'] = j
    image = numpy.roll(numpy.roll(transform['image'], transform['i'], axis=0), transform['j'], axis=1)
    # misc.toimage(image).show()
    transform['similarity_b']['a1b1'] = similarity(image, images['b'], 1, 1)
    transform['similarity_b']['a1b0'] = similarity(image, images['b'], 1, 0)
    transform['similarity_b']['a0b1'] = similarity(image, images['b'], 0, 1)

    transform['similarity_c']['a1b1'] = similarity(image, images['c'], 1, 1)
    transform['similarity_c']['a1b0'] = similarity(image, images['c'], 1, 0)
    transform['similarity_c']['a0b1'] = similarity(image, images['c'], 0, 1)

    transforms[name] = transform

    print('Zakończono transformacje {}'.format(name))


if __name__ == '__main__':
    manager = Manager()
    process_data = manager.dict()

    identity = images['a']
    mirror = transformations['mirror'](images['a'])  # numpy.fliplr(images['a'])
    flip = transformations['flip'](images['a'])  # numpy.flipud(images['a'])
    rot90 = transformations['rot90'](images['a'])  # numpy.rot90(images['a'], 1)
    rot180 = transformations['rot180'](images['a'])
    rot270 = transformations['rot270'](images['a'])

    p = Process(target=transformation, args=(identity, process_data, 'identity',))
    p.daemon = True
    p.start()

    p1 = Process(target=transformation, args=(mirror, process_data, 'mirror',))
    p1.daemon = False
    p1.start()

    p2 = Process(target=transformation, args=(rot90, process_data, 'rot90',))
    p2.daemon = False
    p2.start()

    p3 = Process(target=transformation, args=(rot180, process_data, 'rot180',))
    p3.daemon = False
    p3.start()

    p4 = Process(target=transformation, args=(rot270, process_data, 'rot270',))
    p4.daemon = False
    p4.start()

    p5 = Process(target=transformation, args=(flip, process_data, 'flip',))
    p5.daemon = False
    p5.start()

    p.join()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    for key in data.keys():
        data[key] = process_data[key]
        if data[key]['similarity_b']['a1b1'] > values[2]:
            values[0] = key
            values[1] = 'a1b1'
            values[2] = data[key]['similarity_b']['a1b1']
            values[3] = 'b'
        if data[key]['similarity_b']['a1b0'] > values[2]:
            values[0] = key
            values[1] = 'a1b0'
            values[2] = data[key]['similarity_b']['a1b0']
            values[3] = 'b'
        if data[key]['similarity_b']['a0b1'] > values[2]:
            values[0] = key
            values[1] = 'a0b1'
            values[2] = data[key]['similarity_b']['a0b1']
            values[3] = 'b'
        if data[key]['similarity_c']['a1b1'] > values[2]:
            values[0] = key
            values[1] = 'a1b1'
            values[2] = data[key]['similarity_c']['a1b1']
            values[3] = 'c'
        if data[key]['similarity_c']['a1b0'] > values[2]:
            values[0] = key
            values[1] = 'a1b0'
            values[2] = data[key]['similarity_c']['a1b0']
            values[3] = 'c'
        if data[key]['similarity_c']['a0b1'] > values[2]:
            values[0] = key
            values[1] = 'a0b1'
            values[2] = data[key]['similarity_c']['a0b1']
            values[3] = 'c'
    pp.pprint(values)

    if values[3] == 'b':
        guess = numpy.roll(numpy.roll(transformations[values[0]](images['c']), data[values[0]]['i'], axis=0), data[values[0]]['j'], axis=1)
        if values[1] == 'a1b0':
            _X = img_complement(images['b'], images['a'])
        elif values[1] == 'a0b1':
            _X = img_complement(images['a'], images['b'])
        else:
            _X = None
    else:
        guess = numpy.roll(numpy.roll(transformations[values[0]](images['b']), data[values[0]]['i'], axis=0),data[values[0]]['j'], axis=1)
        if values[1] == 'a1b0':
            _X = img_complement(images['c'], images['a'])
        elif values[1] == 'a0b1':
            _X = img_complement(images['a'], images['c'])
        else:
            _X = None

    guess = img_union(guess, _X)

    misc.toimage(guess).show()

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



