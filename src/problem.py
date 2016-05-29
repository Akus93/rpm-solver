import json
from .image import Image

problems_config = {
    '2x1': {
        'answers': [str(x) + '.png' for x in range(1, 9)],
        'data': ['a.png', 'b.png', 'c.png'],
        'full': 'full.png',
        'info': 'info.json',
    },
    '2x2': {

    },
    '3x3': {

    }
}


class Problem:

    def __init__(self, _type, _number):
        self.type = _type
        self.number = _number
        self.path = '../res/{}/{}/'.format(self.type, self.number)
        self.config = problems_config[self.type]
        self.correct_answer = self.get_correct_answer()
        self.answer_images = []
        self.data_images = []

        self._get_answer_images()
        self._get_data_images()

    def get_correct_answer(self):
        info = None
        with open(self.path + self.config['info']) as info_file:
            info = json.load(info_file)
        return info['answer']

    def _get_answer_images(self):
        for name in self.config['answers']:
            self.answer_images.append(Image(self.path + name))

    def _get_data_images(self):
        for name in self.config['data']:
            self.data_images.append(Image(self.path + name))


problem = Problem('2x1', '1')
for ans_id, answer in enumerate(problem.answer_images, 1):
    print('Image {}: path({})'.format(ans_id, answer.path))
    for obj_id, obj in enumerate(answer.objects, 1):
        print('\t Object {}: shape: {}, Area: {}, aspect_ratio: {}, filled: {}, height: {},'' width: {}, center: {}'
              .format(obj_id, obj.shape, obj.area, obj.aspect_ratio, obj.filled, obj.height, obj.width, obj.center))
    print()


